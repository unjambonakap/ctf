; ===========================================================================

; Segment type:	Pure code
		AREA __text, CODE, READWRITE
		; ORG 0xA80
		CODE16

; =============== S U B	R O U T	I N E =======================================


		EXPORT _col_size
_col_size				; CODE XREF: _validate_database+DEp
					; _check_login+48p ...

ps
var_C		= -0xC//size of input file?
var_8		= -8 //input file?
var_4		= -4 //ret value

		SUB		SP, SP,	#0xC
		STR		R0, [SP,#0xC+var_8]
		LDRB		R0, [R0]
		CMP		R0, #7
		STR		R0, [SP,#0xC+var_C]//len < 7
		BHI		loc_AEA
		LDR		R1, [SP,#0xC+var_C]
		TBB.W		[PC,R1]	; switch 8 cases
; ---------------------------------------------------------------------------
jpt_A8E		DCB 4			; jump table for switch	statement
		DCB 9
		DCB 0xE
		DCB 0x13
		DCB 0x18
		DCB 0x1D
		DCB 0x22
		DCB 0x27
; ---------------------------------------------------------------------------

loc_A9A					; CODE XREF: _col_size+Ej
		MOVS		R0, #1	; jumptable 00000A8E case 0
		STR		R0, [SP,#0xC+var_4]
		B		loc_AF2
; ---------------------------------------------------------------------------

loc_AA4					; CODE XREF: _col_size+Ej
		MOVS		R0, #2	; jumptable 00000A8E case 1
		STR		R0, [SP,#0xC+var_4]
		B		loc_AF2
; ---------------------------------------------------------------------------

loc_AAE					; CODE XREF: _col_size+Ej
		MOVS		R0, #4	; jumptable 00000A8E case 2
		STR		R0, [SP,#0xC+var_4]
		B		loc_AF2
; ---------------------------------------------------------------------------

loc_AB8					; CODE XREF: _col_size+Ej
		MOVS		R0, #8	; jumptable 00000A8E case 3
		STR		R0, [SP,#0xC+var_4]
		B		loc_AF2
; ---------------------------------------------------------------------------

loc_AC2					; CODE XREF: _col_size+Ej
		MOVS		R0, #8	; jumptable 00000A8E case 4
		STR		R0, [SP,#0xC+var_4]
		B		loc_AF2
; ---------------------------------------------------------------------------

loc_ACC					; CODE XREF: _col_size+Ej
		MOVS		R0, #0x10 ; jumptable 00000A8E case 5
		STR		R0, [SP,#0xC+var_4]
		B		loc_AF2
; ---------------------------------------------------------------------------

loc_AD6					; CODE XREF: _col_size+Ej
		MOVS		R0, #0x20 ; ' '	; jumptable 00000A8E case 6
		STR		R0, [SP,#0xC+var_4]
		B		loc_AF2
; ---------------------------------------------------------------------------

loc_AE0					; CODE XREF: _col_size+Ej
		MOVS		R0, #4	; jumptable 00000A8E case 7
		STR		R0, [SP,#0xC+var_4]
		B		loc_AF2
; ---------------------------------------------------------------------------

loc_AEA					; CODE XREF: _col_size+Aj
		MOVS		R0, #0
		STR		R0, [SP,#0xC+var_4]

loc_AF2					; CODE XREF: _col_size+22j
					; _col_size+2Cj ...
		LDR		R0, [SP,#0xC+var_4]
		ADD		SP, SP,	#0xC
		BX		LR
; End of function _col_size


; =============== S U B	R O U T	I N E =======================================


		EXPORT _validate_database
_validate_database

var_2C		= -0x2C
var_28		= -0x28
var_24		= -0x24
var_20		= -0x20
var_1C		= -0x1C
var_18		= -0x18
var_14		= -0x14
var_10		= -0x10
var_C		= -0xC

		PUSH		{R7,LR}
		MOV		R7, SP
		SUB		SP, SP,	#0x24
		MOVS		R2, #0xC
		STR		R0, [SP,#0x2C+var_10]
		STR		R1, [SP,#0x2C+var_14]
		LDR		R0, [SP,#0x2C+var_10]
		STR		R0, [SP,#0x2C+var_18]
		STR		R2, [SP,#0x2C+var_1C]
		LDR		R0, [SP,#0x2C+var_14]
		LDR		R1, [SP,#0x2C+var_1C]
		CMP		R0, R1 // if size -  0#c
		BCS		loc_B20
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A//fail here
; ---------------------------------------------------------------------------

loc_B20					; CODE XREF: _validate_database+1Cj
		MOV		R0, #0x4F4C4F57
		LDR		R1, [SP,#0x2C+var_18]
		LDR		R1, [R1]
		CMP		R1, R0
		BEQ		loc_B3A
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_B3A					; CODE XREF: _validate_database+36j
		LDR		R0, [SP,#0x2C+var_18]
		LDR		R0, [R0,#4]
		CMP		R0, #1
		BEQ		loc_B4C
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_B4C					; CODE XREF: _validate_database+48j
		LDR		R0, [SP,#0x2C+var_18]
		LDRH		R0, [R0,#0xA]
		CMP		R0, #4
		BGE		loc_B5E
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_B5E					; CODE XREF: _validate_database+5Aj
		LDR		R0, [SP,#0x2C+var_18]
		LDRH		R0, [R0,#0xA]
		CMP.W		R0, #0x1000
		BLE		loc_B72
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_B72					; CODE XREF: _validate_database+6Ej
		LDR		R0, [SP,#0x2C+var_18]
		LDRH		R0, [R0,#8]
		CMP		R0, #4
		BGE		loc_B84
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_B84					; CODE XREF: _validate_database+80j
		LDR		R0, [SP,#0x2C+var_18]
		LDRH		R0, [R0,#8]
		CMP		R0, #0x10
		BLE		loc_B96
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_B96					; CODE XREF: _validate_database+92j
		LDR		R0, [SP,#0x2C+var_18]
		LDRH		R0, [R0,#8]
		MOVS		R1, #0x11
		MULS		R0, R1
		LDR		R1, [SP,#0x2C+var_1C]
		ADD		R0, R1
		STR		R0, [SP,#0x2C+var_1C]
		LDR		R0, [SP,#0x2C+var_14]
		LDR		R1, [SP,#0x2C+var_1C]
		CMP		R0, R1
		BCS		loc_BBA
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_BBA					; CODE XREF: _validate_database+B6j
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_20]
		LDR		R1, [SP,#0x2C+var_10]
		ADDS		R1, #0xC
		STR		R1, [SP,#0x2C+var_24]
		STR		R0, [SP,#0x2C+var_28]

loc_BCA					; CODE XREF: _validate_database+108j
		LDR		R0, [SP,#0x2C+var_28]
		LDR		R1, [SP,#0x2C+var_18]
		LDRH		R1, [R1,#8]
		CMP		R0, R1
		BCS		loc_C02
		LDR		R0, [SP,#0x2C+var_24]
		BL		_col_size
		STR		R0, [SP,#0x2C+var_2C]
		LDR		R0, [SP,#0x2C+var_2C]
		CMP		R0, #0
		BNE		loc_BEC
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_BEC					; CODE XREF: _validate_database+E8j
		LDR		R0, [SP,#0x2C+var_2C]
		LDR		R1, [SP,#0x2C+var_20]
		ADD		R0, R1
		STR		R0, [SP,#0x2C+var_20]
		LDR		R0, [SP,#0x2C+var_24]
		ADDS		R0, #0x11
		STR		R0, [SP,#0x2C+var_24]
		LDR		R0, [SP,#0x2C+var_28]
		ADDS		R0, #1
		STR		R0, [SP,#0x2C+var_28]
		B		loc_BCA
; ---------------------------------------------------------------------------

loc_C02					; CODE XREF: _validate_database+DAj
		LDR		R0, [SP,#0x2C+var_20]
		LDR		R1, [SP,#0x2C+var_18]
		LDRH		R1, [R1,#0xA]
		MULS		R0, R1
		LDR		R1, [SP,#0x2C+var_1C]
		ADD		R0, R1
		STR		R0, [SP,#0x2C+var_1C]
		LDR		R0, [SP,#0x2C+var_14]
		LDR		R1, [SP,#0x2C+var_1C]
		CMP		R0, R1
		BCS		loc_C22
		MOVS		R0, #0
		STR		R0, [SP,#0x2C+var_C]
		B		loc_C2A
; ---------------------------------------------------------------------------

loc_C22					; CODE XREF: _validate_database+11Ej
		MOVS		R0, #1
		STR		R0, [SP,#0x2C+var_C]

loc_C2A					; CODE XREF: _validate_database+26j
					; _validate_database+40j ...
		LDR		R0, [SP,#0x2C+var_C]
		ADD		SP, SP,	#0x24
		POP		{R7,PC}
; End of function _validate_database


; =============== S U B	R O U T	I N E =======================================


		EXPORT _check_login
_check_login

var_6C		= -0x6C
var_68		= -0x68
var_64		= -0x64
var_60		= -0x60
var_5C		= -0x5C
var_58		= -0x58
var_54		= -0x54
var_50		= -0x50
var_4C		= -0x4C
var_48		= -0x48
var_44		= -0x44
var_40		= -0x40
var_3C		= -0x3C
var_38		= -0x38
var_34		= -0x34
var_30		= -0x30
var_2C		= -0x2C
var_28		= -0x28
var_24		= -0x24
var_20		= -0x20
var_1C		= -0x1C
var_18		= -0x18
var_14		= -0x14
var_10		= -0x10
var_C		= -0xC

		PUSH		{R7,LR}
		MOV		R7, SP
		SUB		SP, SP,	#0x64
		MOVS		R2, #0
		STR		R0, [SP,#0x6C+var_10]
		STR		R1, [SP,#0x6C+var_14]
		LDR		R0, [SP,#0x6C+var_10]
		STR		R0, [SP,#0x6C+var_18]
		LDR		R0, [SP,#0x6C+var_10]
		ADDS		R0, #0xC
		STR		R0, [SP,#0x6C+var_1C]
		LDR		R0, [SP,#0x6C+var_10]
		ADDS		R0, #0xC
		STR		R0, [SP,#0x6C+var_20]
		LDR		R0, [SP,#0x6C+var_18]
		LDRH		R0, [R0,#8]
		MOVS		R1, #0x11
		MULS		R0, R1
		LDR		R1, [SP,#0x6C+var_20]
		ADD		R0, R1
		STR		R0, [SP,#0x6C+var_20]
		STR		R2, [SP,#0x6C+var_24]
		LDR		R0, [SP,#0x6C+var_10]
		ADDS		R0, #0xC
		STR		R0, [SP,#0x6C+var_28]
		STR		R2, [SP,#0x6C+var_2C]

loc_C6C					; CODE XREF: _check_login+72j
		LDR		R0, [SP,#0x6C+var_2C]
		LDR		R1, [SP,#0x6C+var_18]
		LDRH		R1, [R1,#8]
		CMP		R0, R1
		BCS		loc_CA4
		LDR		R0, [SP,#0x6C+var_28]
		BL		_col_size
		STR		R0, [SP,#0x6C+var_30]
		LDR		R0, [SP,#0x6C+var_30]
		CMP		R0, #0
		BNE		loc_C8E
		MOVS		R0, #0
		STR		R0, [SP,#0x6C+var_C]
		B		loc_F1C
; ---------------------------------------------------------------------------

loc_C8E					; CODE XREF: _check_login+52j
		LDR		R0, [SP,#0x6C+var_30]
		LDR		R1, [SP,#0x6C+var_24]
		ADD		R0, R1
		STR		R0, [SP,#0x6C+var_24]
		LDR		R0, [SP,#0x6C+var_28]
		ADDS		R0, #0x11
		STR		R0, [SP,#0x6C+var_28]
		LDR		R0, [SP,#0x6C+var_2C]
		ADDS		R0, #1
		STR		R0, [SP,#0x6C+var_2C]
		B		loc_C6C
; ---------------------------------------------------------------------------

loc_CA4					; CODE XREF: _check_login+44j
		LDR		R0, [SP,#0x6C+var_20]
		STR		R0, [SP,#0x6C+var_28]
		LDR		R0, [SP,#0x6C+var_10]
		LDR		R1, [SP,#0x6C+var_14]
		ADD		R0, R1
		STR		R0, [SP,#0x6C+var_34]

loc_CB0					; CODE XREF: _check_login+2E2j
		LDR		R0, [SP,#0x6C+var_28]
		LDR		R1, [SP,#0x6C+var_34]
		CMP		R0, R1
		BCS.W		loc_F14
		MOVS		R0, #0
		LDR		R1, [SP,#0x6C+var_28]
		STR		R1, [SP,#0x6C+var_38]
		STR		R0, [SP,#0x6C+var_3C]
		STR		R0, [SP,#0x6C+var_40]
		STR		R0, [SP,#0x6C+var_44]
		STR		R0, [SP,#0x6C+var_48]
		STR		R0, [SP,#0x6C+var_4C]

loc_CCE					; CODE XREF: _check_login+296j
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R1, [SP,#0x6C+var_18]
		LDRH		R1, [R1,#8]
		CMP		R0, R1
		BCS.W		loc_EC8
		MOV		R1, #(aUsername	- 0xCE6) ; "USERNAME"
		ADD		R1, PC	; "USERNAME"
		MOVS		R2, #8	; size_t
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R3, [SP,#0x6C+var_1C]
		MOV		R9, #0x11
		MUL.W		R0, R0,	R9
		ADD		R0, R3
		ADDS		R0, #1	; char *
		BLX		_strncmp
		CMP		R0, #0
		BNE		loc_D3E
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R1, [SP,#0x6C+var_1C]
		MOVS		R2, #0x11
		MULS		R0, R2
		ADD		R0, R1
		LDRB		R0, [R0]
		CMP		R0, #5
		BNE		loc_D3E
		MOV		R1, #(aCaptainfalcon - 0xD26) ;	"captainfalcon"
		ADD		R1, PC	; "captainfalcon"
		MOVS		R2, #0xE ; size_t
		LDR		R0, [SP,#0x6C+var_38] ;	char *
		BLX		_strncmp
		CMP		R0, #0
		BNE		loc_D3C
		MOVS		R0, #1
		STR		R0, [SP,#0x6C+var_3C]

loc_D3C					; CODE XREF: _check_login+102j
		B		loc_D3E
; ---------------------------------------------------------------------------

loc_D3E					; CODE XREF: _check_login+D4j
					; _check_login+E8j ...
		MOV		R1, #(aPassword	- 0xD4A) ; "PASSWORD"
		ADD		R1, PC	; "PASSWORD"
		MOVS		R2, #8	; size_t
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R3, [SP,#0x6C+var_1C]
		MOV		R9, #0x11
		MUL.W		R0, R0,	R9
		ADD		R0, R3
		ADDS		R0, #1	; char *
		BLX		_strncmp
		CMP		R0, #0
		BNE		loc_DA2
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R1, [SP,#0x6C+var_1C]
		MOVS		R2, #0x11
		MULS		R0, R2
		ADD		R0, R1
		LDRB		R0, [R0]
		CMP		R0, #6
		BNE		loc_DA2
		MOV		R1, #(aFc03329505475d -	0xD8A) ; "fc03329505475dd4be51627cc7f0b1f1"
		ADD		R1, PC	; "fc03329505475dd4be51627cc7f0b1f1"
		MOVS		R2, #0x20 ; ' '	; size_t
		LDR		R0, [SP,#0x6C+var_38] ;	char *
		BLX		_strncmp
		CMP		R0, #0
		BNE		loc_DA0
		MOVS		R0, #1
		STR		R0, [SP,#0x6C+var_40]

loc_DA0					; CODE XREF: _check_login+166j
		B		loc_DA2
; ---------------------------------------------------------------------------

loc_DA2					; CODE XREF: _check_login+138j
					; _check_login+14Cj ...
		MOV		R1, #(aAdmin - 0xDAE) ;	"ADMIN"
		ADD		R1, PC	; "ADMIN"
		MOVS		R2, #5	; size_t
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R3, [SP,#0x6C+var_1C]
		MOV		R9, #0x11
		MUL.W		R0, R0,	R9
		ADD		R0, R3
		ADDS		R0, #1	; char *
		BLX		_strncmp
		CMP		R0, #0
		BNE		loc_E0C
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R1, [SP,#0x6C+var_1C]
		MOVS		R2, #0x11
		MULS		R0, R2
		ADD		R0, R1
		LDRB		R0, [R0]
		CMP		R0, #0
		BNE		loc_E0C
		LDR		R0, [SP,#0x6C+var_38]
		LDRB		R0, [R0]
		STRB.W		R0, [SP,#0x6C+var_50]
		LDRB.W		R0, [SP,#0x6C+var_50]
		CMP		R0, #1
		BNE		loc_DFA
		MOVS		R0, #1
		STR		R0, [SP,#0x6C+var_44]

loc_DFA					; CODE XREF: _check_login+1C0j
		MOV		R0, #(aU - 0xE06) ; "%u\n"
		ADD		R0, PC	; "%u\n"
		LDR		R1, [SP,#0x6C+var_44]
		BLX		_printf
		STR		R0, [SP,#0x6C+var_58]

loc_E0C					; CODE XREF: _check_login+19Cj
					; _check_login+1B0j
		MOV		R1, #(aIsawesome - 0xE18) ; "ISAWESOME"
		ADD		R1, PC	; "ISAWESOME"
		MOVS		R2, #9	; size_t
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R3, [SP,#0x6C+var_1C]
		MOV		R9, #0x11
		MUL.W		R0, R0,	R9
		ADD		R0, R3
		ADDS		R0, #1	; char *
		BLX		_strncmp
		CMP		R0, #0
		BNE		loc_E68
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R1, [SP,#0x6C+var_1C]
		MOVS		R2, #0x11
		MULS		R0, R2
		ADD		R0, R1
		LDRB		R0, [R0]
		CMP		R0, #0
		BNE		loc_E68
		LDR		R0, [SP,#0x6C+var_38]
		LDRB		R0, [R0]
		STRB.W		R0, [SP,#0x6C+var_54]
		LDRB.W		R0, [SP,#0x6C+var_54]
		CMP		R0, #1
		MOVW		R0, #0
		IT EQ
		MOVEQ		R0, #1
		AND.W		R0, R0,	#1
		STR		R0, [SP,#0x6C+var_48]

loc_E68					; CODE XREF: _check_login+206j
					; _check_login+21Aj
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R1, [SP,#0x6C+var_1C]
		MOVS		R2, #0x11
		MULS		R0, R2
		ADD		R0, R1
		ADDS		R1, R0,	#1
		LDR		R0, [SP,#0x6C+var_4C]
		LDR		R2, [SP,#0x6C+var_1C]
		MOVS		R3, #0x11
		MULS		R0, R3
		ADD		R0, R2
		STR		R1, [SP,#0x6C+var_5C]
		BL		_col_size
		MOV		R1, #(a_16sUP -	0xE98) ; "%.16s %u\t%p\n"
		ADD		R1, PC	; "%.16s %u\t%p\n"
		LDR		R3, [SP,#0x6C+var_38]
		STR		R0, [SP,#0x6C+var_60]
		MOV		R0, R1	; char *
		LDR		R1, [SP,#0x6C+var_5C]
		LDR		R2, [SP,#0x6C+var_60]
		BLX		_printf
		LDR		R1, [SP,#0x6C+var_4C]
		LDR		R2, [SP,#0x6C+var_1C]
		MOVS		R3, #0x11
		MULS		R1, R3
		ADD		R1, R2
		STR		R0, [SP,#0x6C+var_64]
		MOV		R0, R1
		BL		_col_size
		LDR		R1, [SP,#0x6C+var_38]
		ADD		R0, R1
		STR		R0, [SP,#0x6C+var_38]
		LDR		R0, [SP,#0x6C+var_4C]
		ADDS		R0, #1
		STR		R0, [SP,#0x6C+var_4C]
		B		loc_CCE
; ---------------------------------------------------------------------------

loc_EC8					; CODE XREF: _check_login+A6j
		MOV		R0, #(aUsernameUPassw -	0xED4) ; "username: %u\tpassword: %u\tadmin: %u\t"...
		ADD		R0, PC	; "username: %u\tpassword: %u\tadmin: %u\t"...
		LDR		R1, [SP,#0x6C+var_3C]
		LDR		R2, [SP,#0x6C+var_40]
		LDR		R3, [SP,#0x6C+var_44]
		LDR.W		R9, [SP,#0x6C+var_48]
		STR.W		R9, [SP,#0x6C+var_6C]
		BLX		_printf
		LDR		R1, [SP,#0x6C+var_3C]
		CMP		R1, #0
		STR		R0, [SP,#0x6C+var_68]
		BEQ		loc_F08
		LDR		R0, [SP,#0x6C+var_40]
		CMP		R0, #0
		BEQ		loc_F08
		LDR		R0, [SP,#0x6C+var_44]
		CMP		R0, #0
		BEQ		loc_F08
		LDR		R0, [SP,#0x6C+var_48]
		CMP		R0, #0
		BEQ		loc_F08
		MOVS		R0, #1
		STR		R0, [SP,#0x6C+var_C]
		B		loc_F1C
; ---------------------------------------------------------------------------

loc_F08					; CODE XREF: _check_login+2BAj
					; _check_login+2C0j ...
		B		loc_F0A
; ---------------------------------------------------------------------------

loc_F0A					; CODE XREF: _check_login:loc_F08j
		LDR		R0, [SP,#0x6C+var_24]
		LDR		R1, [SP,#0x6C+var_28]
		ADD		R0, R1
		STR		R0, [SP,#0x6C+var_28]
		B		loc_CB0
; ---------------------------------------------------------------------------

loc_F14					; CODE XREF: _check_login+86j
		MOVS		R0, #0
		STR		R0, [SP,#0x6C+var_C]

loc_F1C					; CODE XREF: _check_login+5Cj
					; _check_login+2D6j
		LDR		R0, [SP,#0x6C+var_C]
		ADD		SP, SP,	#0x64
		POP		{R7,PC}
; End of function _check_login

; __text	ends
