data = [
  [0x1580, 0x4],
[0x1581, 0x0],
[0x11fa, 0x90],
[0x11fb, 0x90],
[0x1083, 0xc6],
[0x1075, 0x57],
]
x = bytearray(open('./def_abc', 'rb').read())
for a, b in data:
  x[a] = b
open('./def_abc.patched', 'wb').write(x)
#0x1580, 0x4

#0x1581, 0x0
#0x1083, 0xc6
#0x11fa, 0x90
#0x11fb, 0x90
#0x1075, 0x57
