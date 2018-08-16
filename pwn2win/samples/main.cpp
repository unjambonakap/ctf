#include <opa/algo/base.h>
#include <opa/math/game/base.h>
#include <opa/utils/DataStruct.h>
#include <opa/utils/base.h>
#include <opa_common.h>
#include <yaml-cpp/yaml.h>

DEFINE_bool(only_edges, false, "");
DEFINE_bool(split_wells, false, "");
DEFINE_bool(extract_netlist, false, "");
DEFINE_bool(extract_wells_info, false, "");
DEFINE_bool(test, false, "");
DEFINE_string(params, "", "");

using namespace std;
using namespace opa;
/* cougar -> gdsii?
   osu magick, drill,
   */

using Box = math::game::BoxAASpec_Gen<2, IPos2, 9>;

const int oo = 1e9;

struct Entry {
  int type;
  int layer;
  Box box;
  std::string text;
  Box cover;
  int id;
  std::string cell_name;

  OPA_DECL_COUT_OPERATOR2(Entry, a.id, a.type, a.layer, a.box, a.cover, a.text, a.cell_name);
};

typedef std::vector<Entry> Layer;
typedef std::map<int, Layer> Layers;
char buf[256];

struct Stats {
  double ratio1 = 0;
  double ratio2 = 0;

  OPA_DECL_COUT_OPERATOR2(Stats, a.ratio1, a.ratio2);
};

struct Event {
  IPos2 pos;
  bool add;
  int tb_id;
  int tb_pos;

  OPA_DECL_LT_OPERATOR(Event, pos.x, add, tb_id, tb_pos);
  bool operator>(const Event &e) const { return e < *this; }
};

class SegmentTree {
public:
  struct Node {
    int T, H;
    Node *l = nullptr, *r = nullptr;
    std::set<Entry *> contained;
    std::set<Entry *> contains;

    void addrem(int low, int high, Entry *entry, bool add) {
      if (high < T || low > H) return;

      if (low <= T && H <= high) {
        if (add)
          contains.insert(entry);
        else
          contains.erase(entry);

      } else {
        if (add)
          contained.insert(entry);
        else
          contained.erase(entry);

        if (l) l->addrem(low, high, entry, add);
        if (r) r->addrem(low, high, entry, add);
      }
    }

    void collect(int low, int high, std::set<Entry *> &res) {
      if (high < T || low > H) return;

      for (auto &entry : contains) res.insert(entry);
      if (low <= T && H <= high) {
        for (auto &entry : contained) res.insert(entry);
      } else {
        if (l) l->collect(low, high, res);
        if (r) r->collect(low, high, res);
      }
    }
  };

  std::set<Entry *> collect(int low, int high) {
    std::set<Entry *> res;
    this->root->collect(low, high, res);
    return res;
  }

  void init(int n) { root = this->create(0, n); }

  Node *create(int T, int H) {
    Node *cur = new Node;
    cur->T = T;
    cur->H = H;

    if (T != H) {
      int M = (T + H) / 2;
      cur->l = create(T, M);
      cur->r = create(M + 1, H);
    }

    nodes.add(cur);

    return cur;
  }

  opa::utils::ObjContainer<Node> nodes;
  Node *root;
};

struct Result {
  Stats stats;
  std::vector<std::pair<int, int> > intersections;
  std::vector<std::pair<int, int> > connections;
  std::vector<int> included_a;
};

struct ProcOptions {
  bool extract_intersections = false;
  bool extract_netlist = false;
  bool extract_wells_info = false;
};

Result compare_layers(const Layer &a, const Layer &b,
                      const ProcOptions &options) {
  Result result;
  bool toggle_add = options.extract_netlist;
  if (a.size() == 0) return result;

  std::vector<Layer> tb = { a, b };
  std::priority_queue<Event, std::vector<Event>, std::greater<Event> > q;
  int layer_a = a[0].layer;

  std::vector<int> ylist;
  utils::Remapper<const Entry *> rmp;

  REP (i, 2) {
    const auto &cur = tb[i];
    REP (j, cur.size()) {
      auto &e = cur[j];
      q.push(Event{ e.box.low, bool(toggle_add ^ true), i, j });
      q.push(Event{ e.box.high, bool(toggle_add ^ false), i, j });
      ylist.push_back(e.box.low.y);
      ylist.push_back(e.box.high.y);

      rmp.get(&e);
    }
  }

  std::sort(ALL(ylist));
  opa::utils::make_unique(ylist);

  REP (i, 2) {
    auto &cur = tb[i];
    REP (j, cur.size()) {}
  }

  SegmentTree st[2];
  REP (f, 2) st[f].init(ylist.size());
  double sum_cover[2] = { 0, 0 };

  while (!q.empty()) {
    Event e = q.top();
    q.pop();
    Entry *entry = &tb[e.tb_id][e.tb_pos];
    int id = entry->layer == layer_a;

    int ylow = std::lower_bound(ALL(ylist), entry->box.low.y) - ylist.begin();
    int yhigh = std::lower_bound(ALL(ylist), entry->box.high.y) - ylist.begin();

    if (toggle_add ^ e.add) {
      std::set<Entry *> overlap = st[id].collect(ylow, yhigh);
      st[id ^ 1].root->addrem(ylow, yhigh, entry, true);

      for (auto &x : overlap) {
        if (x->layer == entry->layer) {
        } else {
          auto b3 = entry->box.intersection(x->box);
          if (options.extract_netlist) {
            if (id)
              result.connections.emplace_back(entry->id, x->id);
            else
              result.connections.emplace_back(x->id, entry->id);
          }

          if (b3.degenerate()) continue;
          double a1 = entry->box.area();
          double a2 = x->box.area();
          double a3 = b3.area();

          if (options.extract_intersections) {
            if (id)
              result.intersections.emplace_back(entry->id, x->id);
            else
              result.intersections.emplace_back(x->id, entry->id);
          }

          sum_cover[0] += a3;
          sum_cover[1] += a3;
          x->cover = x->cover.get_union(b3);
          entry->cover = entry->cover.get_union(b3);
          OPA_CHECK(entry->cover.area() <= a1, entry->cover, b3, x->box,
                    entry->box);
          OPA_CHECK(x->cover.area() <= a2, x->cover, b3, x->box, entry->box);

          OPA_CHECK(a3 >= 0, a3, b3, entry->box, x->box);
        }
      }

    } else {
      st[id ^ 1].root->addrem(ylow, yhigh, entry, false);
    }
  }

  if (options.extract_intersections) {
  } else if (options.extract_wells_info) {
    REP (i, tb[0].size()) {
      if (tb[0][i].cover == tb[0][i].box) result.included_a.push_back(tb[0][i].id);
    }

  } else {
    Stats stats;
    REP (f, 2) {
      double tot_area = 0;
      double covered = 0;
      for (auto &x : tb[f]) {
        tot_area += x.box.area(), covered += x.cover.area();
        OPA_CHECK(covered <= tot_area, covered, tot_area, x);
      }
      covered = std::min(covered, sum_cover[f]);
      (f == 0 ? stats.ratio1 : stats.ratio2) = covered / tot_area;
    }
    result.stats = stats;
  }
  return result;
}

void read_layers(Layers &layer_to_entries) {
  int n;
  scanf("%d", &n);
  REP (i, n) {

    Entry cur;
    scanf("%d%d%d %s", &cur.id, &cur.type, &cur.layer, buf);
    cur.cell_name = buf;

    if (cur.type == 1) {
      REP (j, 4) {
        IPos2 p;
        scanf("%d%d", &p.x, &p.y);
        cur.box.update(p);
      }

    } else {
      IPos2 p;
      scanf("%d%d", &p.x, &p.y);
      cur.box.update(p);

      scanf("%s", buf);
      buf[255] = 0;
      cur.text = buf;
    }
    layer_to_entries[cur.layer].push_back(cur);
  }
}

void dump_layers(const Layers &layers) {
  int n = 0;
  for (auto &x : layers) n += x.second.size();
  int finalid = 0;
  printf("%d\n", n);
  for (auto &x : layers) {
    for (auto &e : x.second) {
      printf("%d %d %d %s ", finalid++, e.type, e.layer, e.cell_name.c_str());
      if (e.type == 1) {
        REP (j, 4)
          printf("%d %d ", e.box.get(j).x, e.box.get(j).y);
      } else {
        printf("%d %d ", e.box.low.x, e.box.low.y);
        printf("%s", e.text.c_str());
      }

      puts("");
    }
  }
}

void do_test() {
  SegmentTree s;
  s.init(10);
  s.root->addrem(1, 2, (Entry *)1, true);
  s.root->addrem(3, 3, (Entry *)2, true);
  OPA_DISP0(s.collect(1, 2));
  OPA_DISP0(s.collect(1, 1));
  OPA_DISP0(s.collect(0, 1));
  OPA_DISP0(s.collect(2, 3));
  OPA_DISP0(s.collect(3, 4));
  OPA_DISP0(s.collect(2, 3));
  OPA_DISP0(s.collect(2, 5));
  OPA_DISP0(s.collect(-1, 0));
}

int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);

  if (FLAGS_test) {
    do_test();
    return 0;
  }

  Layers layer_to_entries;
  read_layers(layer_to_entries);
  std::map<int, Entry*> id_to_entry;
  for (auto &layer : layer_to_entries){
    for (auto &e : layer.second) id_to_entry[e.id] = &e;
  }

  ProcOptions options;
  auto conf = YAML::Load(FLAGS_params);

  if (FLAGS_split_wells) {
    options.extract_intersections = true;

    int gate_layer_id = conf["gate"].as<int>();
    auto &gate_layer = layer_to_entries[gate_layer_id];

    int well_layer_id = conf["well"].as<int>();
    auto &well_layer = layer_to_entries[well_layer_id];
    auto result = compare_layers(well_layer, gate_layer, options);

    std::map<int, std::vector<int> > splitters;
    for (auto &intersection : result.intersections)
      splitters[intersection.first].push_back(intersection.second);

    Layer nlayer;
    for (auto &e : splitters) {
      Entry nentry = *id_to_entry[e.first];
      Box curbox = nentry.box;

      for (auto &splitter : e.second) {
        Box split_box = id_to_entry[splitter]->box;
        OPA_CHECK(!curbox.intersection(split_box).degenerate(), curbox,
                  split_box, nentry);
        OPA_CHECK(split_box.get_range2(1).contains(curbox.get_range2(1)),
                  split_box, curbox);

        Box before = curbox.cut_toward_small(0, split_box.low[0]);
        Box after = curbox.cut_toward_large(0, split_box.high[0]);

        curbox = after;
        nentry.box = before;
        nlayer.push_back(nentry);
      }

      nentry.box = curbox;
      nlayer.push_back(nentry);
    }

    for (auto &e : well_layer) {
      if (!splitters.count(e.id)) {
        nlayer.push_back(e);
      }
    }
    layer_to_entries[well_layer_id] = nlayer;
    dump_layers(layer_to_entries);

  } else if (FLAGS_extract_netlist || FLAGS_extract_wells_info) {
    options.extract_wells_info = FLAGS_extract_wells_info;
    options.extract_netlist = FLAGS_extract_netlist;

    int layer1_id = conf["layer1"].as<int>();
    int layer2_id = conf["layer2"].as<int>();
    Layer layer1, layer2;
    layer1 = layer_to_entries[layer1_id];
    layer2 = layer_to_entries[layer2_id];
    for (auto &e : layer1) e.layer = 0;
    for (auto &e : layer2) e.layer = 1;

    auto result = compare_layers(layer1, layer2, options);

    if (options.extract_netlist) {
      std::sort(ALL(result.connections));
      utils::make_unique(result.connections);
      if (FLAGS_only_edges) {
        printf("%lu\n", result.connections.size());
        for (auto &x : result.connections) {
          printf("%d %d\n", x.first, x.second);
        }
      } else {

        utils::Remapper<int> objrmp;
        for (auto &x : result.connections) objrmp.get(x.first), objrmp.get(x.second);
        algo::UnionJoin uj(objrmp.size());
        for (auto &x : result.connections) {
          uj.merge(objrmp.get(x.first), objrmp.get(x.second));
        }

        auto groups = uj.get_groups();
        printf("%lu\n", groups.size());
        for (auto &entries : groups) {
          std::set<std::string> labels;
          std::vector<int> ids;
          for (auto &x : entries) {
            Entry *e = id_to_entry[objrmp.rget(x)];
            ids.push_back(e->id);
          }

          printf("%lu ", ids.size());
          for (auto &x : ids) printf("%d ", x);
          puts("");
        }
      }
    } else {
      printf("%lu\n", result.included_a.size());
      for (auto &x : result.included_a) {
        printf("%d\n", x);
      }
    }

  } else {
    for (auto &a : layer_to_entries) {
      OPA_DISP0(a.first);
      for (auto &b : layer_to_entries) {
        if (a.first >= b.first) continue;

        // if (a.first != 0x2e || b.first != 0x2f) continue;
        OPA_DISP("on ", a.first, b.first, a.second.size(), b.second.size());
        auto result = compare_layers(a.second, b.second, options);
        OPA_DISP("Processing layers ", a.first, b.first, result.stats);
      }
    }
  }

  return 0;
}
