#include <opa/crypto/hash.h>
#include <opa/math/common/fast_gf2.h>
#include <opa/threading/auto_job.h>
#include <opa/threading/dispatcher.h>
#include <opa/threading/runner.h>
#include <opa/utils/buffer_reader.h>
#include <opa_common.h>
#include <random>

constexpr int NBITX = 20;
using namespace std;
DEFINE_string(work_dir, ".", "");

int N, M;
std::string base_sol;
std::vector<opa::math::common::BitVec> kernel;

struct S64_pb : public opa::utils::ProtobufParams {
  s64 v;
  OPA_TGEN_IMPL(v);
};

struct Task : public opa::threading::AutoFindOneJob<S64_pb, S64_pb> {
  opa::crypto::Sha256 hasher;
  opa::math::common::BitVec vec;
  Task() { vec.init(M); }

  bool checkit(u64 tx) {
    vec.setz();
    REP (i, kernel.size()) {
      if (tx >> i & 1) {
        vec.sxorz(kernel[i]);
      }
    }

    std::string nsol = base_sol;
    vec.xorz((u64 *)nsol.data());
    int sz = nsol[7];
    if (8 + sz + 16 > nsol.size()) return false;
    FOR (j, 8, 8 + sz) {
      if (!isprint(nsol[j])) return false;
    }

    hasher.reset();
    hasher.update((const u8 *)nsol.data(), nsol.size() - 16);
    std::string wanted_hash(nsol.data() + nsol.size() - 16, 16);
    std::string current_hash = std::string(hasher.get().data(), 16);
    if (wanted_hash != current_hash) return false;

    std::string fsol(nsol.data() + 8, sz);
    OPA_DISP("Solution found >> ", fsol);
    return true;
  }

  virtual void auto_worker_do_work(const S64_pb &data,
                                   S64_pb &out_res) override {
    out_res.v = -1;
    REP (i, 1 << NBITX) {
      u64 tx = (data.v << NBITX) | i;
      if (checkit(tx)) {
        out_res.v = tx;
        return;
      }
    }
  }

  virtual bool auto_server_handle_res(const S64_pb &res) override {
    return res.v != -1;
  }

  virtual void auto_server_get_work() override {
    S64_pb id;
    REP64(i, 1ull << (N - NBITX)) {
      id.v = i;
      bool more;
      cb()(id, more);
      if (!more) break;
    }
  }

  S64_pb dummy_params;

  OPA_CLOUDY_JOB_DECL;
  OPA_TGEN_IMPL(dummy_params);
};
OPA_CLOUDY_REGISTER_BASE(Task);
OPA_CLOUDY_JOB_IMPL(Task);

int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);
  base_sol = opa::utils::read_file(FLAGS_work_dir + "/sol.base");
  std::string kernel_desc = opa::utils::read_file(FLAGS_work_dir + "/sol.kern");
  {
    N = ((int *)kernel_desc.data())[0];
    M = ((int *)kernel_desc.data())[1];
    OPA_CHECK(kernel_desc.size() == N*M+8, kernel_desc.size(), N, M);
    REP (i, N) {
      kernel.emplace_back();
      kernel.back().init(M);
      REP (j, M)
        kernel.back().set(j, kernel_desc[i * M + j + 8] == '1');
    }
  }

  opa::threading::Runner::Build();
  opa::threading::Runner runner;
  runner.run_both();
  opa::threading::Dispatcher *dispatcher = runner.dispatcher();

  UPTR(Task)
  task(opa::threading::Runner::GetJob<Task>(Task::JobName));
  dispatcher->process_job(*task);
  OPA_DISP0("done");

  return 0;
}
//fsol=34C3_w0w_who_kn3w_y0u_d0nt_w4nt_l1n34r1ty_1n_AES,

