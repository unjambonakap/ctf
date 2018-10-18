#include "pin.H"
#include <inttypes.h>
#include <iostream>
#include <opa/utils/string_base.h>
#include <opa_common_base.h>

UINT64 ins_count = 0;

VOID PIN_FAST_ANALYSIS_CALL docount(ADDRINT c) { ins_count += c; }
VOID Trace(TRACE trace, VOID *v) {
  // Visit every basic block  in the trace
  for (BBL bbl = TRACE_BblHead(trace); BBL_Valid(bbl); bbl = BBL_Next(bbl)) {
    BBL_InsertCall(bbl, IPOINT_ANYWHERE, AFUNPTR(docount),
                   IARG_FAST_ANALYSIS_CALL, IARG_UINT32, BBL_NumIns(bbl),
                   IARG_END);
  }
}

VOID Instruction(INS ins, VOID *v) {
  INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)docount, IARG_INST_PTR, IARG_END);
}



class State {
public:
  int curlen = 0;
  char buf[100] = { 0 };
  std::vector<int> cnt;
  char &curc() { return buf[curlen - 1]; }
};

State g_state;


void done() {
  puts("Found solution >> ");
  REP (i, g_state.curlen) { printf("%02x", g_state.buf[i]); }
  puts("");

  PIN_ExitApplication(0);
}

void hook_func(const CONTEXT *ctx, ADDRINT ip, BOOL is_entry,
               ADDRINT arg0, ADDRINT arg1, ADDRINT ret) {
  if (ret) {
    if (ret == 1) {
      done();
      g_state.cnt.push_back(ins_count);
      g_state.curc()++;
    }

  } else {
    ins_count = 0;
    if (g_state.curc() == 128) {
      printf("done processing %d\n", g_state.curlen);
      out(g_state.cnt);
      int maxv = std::max_element(ALL(g_state.cnt)) - g_state.cnt.begin();
      g_state.curc() = maxv;
      g_state.curlen++;
      g_state.curc() = 0;
      g_state.cnt.clear();
    }
  }
}

BOOL catch_signal(THREADID tid, INT32 sig, CONTEXT *ctxt, BOOL hasHandler,
                  const EXCEPTION_INFO *pExceptInfo, VOID *v) {
  puts("exit segfault");
  PIN_ExitApplication(0);
  return true;
}

static void I_ImageLoad(IMG img, void *v) {
  bool is_main = IMG_IsMainExecutable(img);
  string img_name = IMG_Name(img);

  PIN_LockClient();
  for (SEC sec = IMG_SecHead(img); SEC_Valid(sec); sec = SEC_Next(sec)) {
    for (RTN rtn = SEC_RtnHead(sec); RTN_Valid(rtn); rtn = RTN_Next(rtn)) {
      SYM sym = RTN_Sym(rtn);
      RTN_Open(rtn);
      std::string name = RTN_Name(rtn);
      if (is_main && name == "test") {

        RTN_InsertCall(
          rtn, IPOINT_BEFORE, (AFUNPTR)hook_func,
          IARG_CONST_CONTEXT, IARG_INST_PTR, IARG_BOOL, TRUE,
          IARG_FUNCARG_ENTRYPOINT_VALUE, 0, IARG_FUNCARG_ENTRYPOINT_VALUE, 1,
          IARG_FUNCARG_ENTRYPOINT_VALUE, 2, IARG_FUNCARG_ENTRYPOINT_VALUE, 3,
          IARG_FUNCARG_ENTRYPOINT_VALUE, 4, IARG_FUNCRET_EXITPOINT_VALUE,
          IARG_END);

        RTN_InsertCall(
          rtn, IPOINT_AFTER, (AFUNPTR)hook_func,
          IARG_CONST_CONTEXT, IARG_INST_PTR, IARG_BOOL, FALSE,
          IARG_FUNCARG_ENTRYPOINT_VALUE, 0, IARG_FUNCARG_ENTRYPOINT_VALUE, 1,
          IARG_FUNCARG_ENTRYPOINT_VALUE, 2, IARG_FUNCARG_ENTRYPOINT_VALUE, 3,
          IARG_FUNCARG_ENTRYPOINT_VALUE, 4, IARG_FUNCRET_EXITPOINT_VALUE,
          IARG_END);
      }

      RTN_Close(rtn);
    }
  }
  PIN_UnlockClient();

  return;
}

INT32 Usage() {
  PIN_ERROR("callstack tool" + KNOB_BASE::StringKnobSummary() + "\n");
  return -1;
}
int main(int argc, char *argv[]) {
  if (PIN_Init(argc, argv)) return Usage();
  PIN_InitSymbols();

  TRACE_AddInstrumentFunction(Trace, 0);
  IMG_AddInstrumentFunction(I_ImageLoad, 0);


  // Never returns
  PIN_StartProgram();

  return 0;
}
