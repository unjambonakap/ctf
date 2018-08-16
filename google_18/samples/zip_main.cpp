#include <opa_common.h>

#include <opa/crypto/lfsr.h>
#include <opa/crypto/lfsr_small.h>
#include <opa/utils/buffer_reader.h>
#include <opa/utils/buffer_writer.h>
#include <yaml-cpp/yaml.h>

DEFINE_string(config_filename, "", "");
DEFINE_string(data_filename, "", "");

using namespace std;
using namespace opa;

const int LFSR_SIZE = 20;
int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);

  std::string data = utils::read_file(FLAGS_data_filename);
  YAML::Node config = YAML::LoadFile(FLAGS_config_filename);

  std::vector<s8> known_data;
  int sz = data.size();
  known_data.resize(sz * 8, -1);
  for (auto entry : config["known"]) {
    int pos = entry["pos"].as<int>();
    int val = entry["val"].as<int>();
    if (known_data[pos] == -1) known_data[pos] = 0;
    known_data[pos] |= 1 << val;
  }

  std::vector<std::vector<int> > ok_pos(8);
  REP (lfsr_id, 8) {
    int iv = config["lfsr"][lfsr_id].as<int>();
    OPA_DISP("set iv", iv);
    REP (poly, 1 << LFSR_SIZE) {
      opa::crypto::LFSR_GF2_small lfsr(poly | (1 << LFSR_SIZE), LFSR_SIZE, iv);
      bool ok = true;

      REP (pos, sz) {
        u8 cur = lfsr.get_next_non_galois();
        s8 can = known_data[lfsr_id + pos * 8];
        if (can == -1) continue;

        u8 cipher = (data[pos] >> lfsr_id) & 1;
        u8 got = cipher ^ cur;
        if (!((can >> got) & 1)) {
          ok = false;
          break;
        }
      }
      if (!ok) continue;
      ok_pos[lfsr_id].push_back(poly);
    }
    OPA_DISP0(ok_pos[lfsr_id].size());
  }

  std::vector<std::vector<int> > can = { {} };
  REP (lfsr_id, 8) {
    std::vector<std::vector<int> > ncan;
    for (auto &e : can) {
      for (auto &x : ok_pos[lfsr_id]) {
        ncan.push_back(e);
        ncan.back().push_back(x);
      }
    }
    can = ncan;
  }

  int id = 0;
  for (auto &x : can) {
    ++id;
    std::string d = data;
    REP (lfsr_id, 8) {
      int iv = config["lfsr"][lfsr_id].as<int>();
      opa::crypto::LFSR_GF2_small lfsr(x[lfsr_id] | (1 << LFSR_SIZE), LFSR_SIZE,
                                       iv);
      bool ok = true;

      REP (pos, sz) {
        u8 cur = lfsr.get_next_non_galois();
        d[pos] ^= cur << lfsr_id;
      }
    }

    std::string fname = opa::utils::stdsprintf("/tmp/resfile_%05d.png", id);
    utils::write_file(fname, d);
  }

  return 0;
}
