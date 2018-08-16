#define INS_ENUM_NAME(x) Ins_##x
#define INS_OP_MODE(x) OpMode_##x
// format: INS_DECL(name, format, format_code, op1, op2)

INS_DECL(RRC, Format_SingleOp, 0x000, Dest, None)
INS_DECL(SWPB, Format_SingleOp, 0x080, Dest, None)
INS_DECL(RRA, Format_SingleOp, 0x100, Src, None)
INS_DECL(SXT, Format_SingleOp, 0x180, Dest, None)
INS_DECL(PUSH, Format_SingleOp, 0x200, Src, None)
INS_DECL(CALL, Format_SingleOp, 0x280, Src, None)
INS_DECL(RETI, Format_SingleOp, 0x300, None, None)

INS_DECL(JNE, Format_Jump, 0x20, None, None)
INS_DECL(JEQ, Format_Jump, 0x24, None, None)
INS_DECL(JNC, Format_Jump, 0x28, None, None)
INS_DECL(JC, Format_Jump, 0x2c, None, None)
INS_DECL(JN, Format_Jump, 0x30, None, None)
INS_DECL(JGE, Format_Jump, 0x34, None, None)
INS_DECL(JL, Format_Jump, 0x38, None, None)
INS_DECL(JMP, Format_Jump, 0x3c, None, None)

INS_DECL(MOV, Format_DoubleOp, 0x4, Src, Dest)
INS_DECL(ADD, Format_DoubleOp, 0x5, Src, Dest)
INS_DECL(ADDC, Format_DoubleOp, 0x6, Src, Dest)
INS_DECL(SUBC, Format_DoubleOp, 0x7, Src, Dest)
INS_DECL(SUB, Format_DoubleOp, 0x8, Src, Dest)
INS_DECL(CMP, Format_DoubleOp, 0x9, Src, Dest)
INS_DECL(DADD, Format_DoubleOp, 0xa, Src, Dest)
INS_DECL(BIT, Format_DoubleOp, 0xb, Src, Dest)
INS_DECL(BIC, Format_DoubleOp, 0xc, Src, Dest)
INS_DECL(BIS, Format_DoubleOp, 0xd, Src, Dest)
INS_DECL(XOR, Format_DoubleOp, 0xe, Src, Dest)
INS_DECL(AND, Format_DoubleOp, 0xf, Src, Dest)
#undef INS_OP_MODE
#undef INS_ENUM_NAME
