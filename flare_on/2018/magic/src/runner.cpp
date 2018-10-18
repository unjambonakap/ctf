#include <opa_common.h>
#include <sys/mman.h>

using namespace std;

void *execute_buf;
const int execute_maxlen = 0x100000;
std::vector<int> charset;

void runner_init() {
  std::string letters = "inds isng  llg w. e  HthitheoftheAh,urnolik inefe  yo "
                        "blrhot in owaceaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

  std::set<int> sl;
  for (auto &c : letters) sl.insert(c);
  charset = std::vector<int>(ALL(sl));

  execute_buf = mmap(0, execute_maxlen, PROT_READ | PROT_WRITE | PROT_EXEC,
                     MAP_PRIVATE | MAP_ANON, -1, 0);
  OPA_CHECK0(execute_buf != MAP_FAILED);
}

OPA_REGISTER_INIT(runner_init, runner_init);

typedef int (*call_t)(const void *a, void *b, const void *c);

struct Data {
  std::string arg3;
  std::string stack;
  std::string res;
  int sz;
};
Data g_data;

void *getsp(void) {
  uint64_t sp;
  asm("mov %%rsp, %0" : "=rm"(sp));
  return (void *)(sp + 8);
}

int do_call(const std::string &cnd) {
  void *sp = getsp();
  std::string nargs3 = g_data.arg3;
  int ssz = g_data.stack.size();
  call_t caller = (call_t)execute_buf;
  REP (i, g_data.stack.size())
    *((char *)sp - ssz + i) = g_data.stack[i];
  if (caller(cnd.data(), (void *)g_data.sz, nargs3.data())) {
    g_data.res = cnd;
    return 1;
  }
  return 0;
}

int gen(int pos, const std::string &cnd) {
  if (pos == g_data.sz) {
    return do_call(cnd);
  }

  std::string now = cnd;
  now.push_back(0);
  REP(i, charset.size()){
    now[pos] = charset[i];
    if (gen(pos + 1, now)) return 1;
  }
  return 0;
}

std::string do_solve(const std::string &code, int nchars,
                     const std::string &arg3, const std::string &stack) {
  g_data.arg3 = arg3;
  g_data.stack = stack;
  g_data.sz = nchars;
  memcpy(execute_buf, code.data(), code.size());

  OPA_CHECK0(gen(0, ""));
  return g_data.res;
}
