#include <opa_common.h>
#include <matasano/ex_57.h>
#include <matasano/ex_58.h>
#include <matasano/ex_59.h>
#include <matasano/ex_60.h>
#include <matasano/ex_61.h>
#include <matasano/ex_62.h>
#include <matasano/ex_63.h>
#include <matasano/ex_64.h>
#include <matasano/ex_65.h>

DEFINE_int32(ex, 57, "");

using namespace matasano;

int main(int argc, char **argv) {
  opa::init::opa_init(argc, argv);
  switch (FLAGS_ex) {
    OPA_CASE(57, ex_57();)
    OPA_CASE(58, ex_58();)
    OPA_CASE(59, ex_59();)
    OPA_CASE(60, ex_60();)
    OPA_CASE(61, ex_61();)
    OPA_CASE(62, ex_62();)
    OPA_CASE(63, ex_63();)
    OPA_CASE(64, ex_64();)
    OPA_CASE(65, ex_65();)
  }

  return 0;
}
