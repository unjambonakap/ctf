# CONFidence/Dragon Sector CTF 2016 Teaser
# RE400 Python Crackme by Gynvael Coldwind
#
# Note: All the global variables are spawned in InitGlobals function,
# this is due to how the obfuscation works (i.e. I'm too lazy to do it
# automatically).
def InitXtermRGB():
  # Kudos for RGB values: https://gist.github.com/jasonm23/2868981
  global XTERM_RGB
  XTERM_RGB = [
      (0, 0, 0, 0),
      (128, 0, 0, 1),
      (0, 128, 0, 2),
      (128, 128, 0, 3),
      (0, 0, 128, 4),
      (128, 0, 128, 5),
      (0, 128, 128, 6),
      (192, 192, 192, 7),
      (128, 128, 128, 8),
      (255, 0, 0, 9),
      (0, 255, 0, 10),
      (255, 255, 0, 11),
      (0, 0, 255, 12),
      (255, 0, 255, 13),
      (0, 255, 255, 14),
      (255, 255, 255, 15),
      (0, 0, 0, 16),
      (0, 0, 95, 17),
      (0, 0, 135, 18),
      (0, 0, 175, 19),
      (0, 0, 215, 20),
      (0, 0, 255, 21),
      (0, 95, 0, 22),
      (0, 95, 95, 23),
      (0, 95, 135, 24),
      (0, 95, 175, 25),
      (0, 95, 215, 26),
      (0, 95, 255, 27),
      (0, 135, 0, 28),
      (0, 135, 95, 29),
      (0, 135, 135, 30),
      (0, 135, 175, 31),
      (0, 135, 215, 32),
      (0, 135, 255, 33),
      (0, 175, 0, 34),
      (0, 175, 95, 35),
      (0, 175, 135, 36),
      (0, 175, 175, 37),
      (0, 175, 215, 38),
      (0, 175, 255, 39),
      (0, 215, 0, 40),
      (0, 215, 95, 41),
      (0, 215, 135, 42),
      (0, 215, 175, 43),
      (0, 215, 215, 44),
      (0, 215, 255, 45),
      (0, 255, 0, 46),
      (0, 255, 95, 47),
      (0, 255, 135, 48),
      (0, 255, 175, 49),
      (0, 255, 215, 50),
      (0, 255, 255, 51),
      (95, 255, 0, 82),
      (95, 255, 95, 83),
      (95, 255, 135, 84),
      (95, 255, 175, 85),
      (95, 255, 215, 86),
      (95, 255, 255, 87),
      (95, 215, 0, 76),
      (95, 215, 95, 77),
      (95, 215, 135, 78),
      (95, 215, 175, 79),
      (95, 215, 215, 80),
      (95, 215, 255, 81),
      (95, 175, 0, 70),
      (95, 175, 95, 71),
      (95, 175, 135, 72),
      (95, 175, 175, 73),
      (95, 175, 215, 74),
      (95, 175, 255, 75),
      (95, 135, 0, 64),
      (95, 135, 95, 65),
      (95, 135, 135, 66),
      (95, 135, 175, 67),
      (95, 135, 215, 68),
      (95, 135, 255, 69),
      (95, 95, 0, 58),
      (95, 95, 95, 59),
      (95, 95, 135, 60),
      (95, 95, 175, 61),
      (95, 95, 215, 62),
      (95, 95, 255, 63),
      (95, 0, 0, 52),
      (95, 0, 95, 53),
      (95, 0, 135, 54),
      (95, 0, 175, 55),
      (95, 0, 215, 56),
      (95, 0, 255, 57),
      (135, 0, 255, 93),
      (135, 0, 215, 92),
      (135, 0, 175, 91),
      (135, 0, 135, 90),
      (135, 0, 95, 89),
      (135, 0, 0, 88),
      (135, 95, 255, 99),
      (135, 95, 215, 98),
      (135, 95, 175, 97),
      (135, 95, 135, 96),
      (135, 95, 95, 95),
      (135, 95, 0, 94),
      (135, 135, 255, 105),
      (135, 135, 215, 104),
      (135, 135, 175, 103),
      (135, 135, 135, 102),
      (135, 135, 95, 101),
      (135, 135, 0, 100),
      (135, 175, 255, 111),
      (135, 175, 215, 110),
      (135, 175, 175, 109),
      (135, 175, 135, 108),
      (135, 175, 95, 107),
      (135, 175, 0, 106),
      (135, 215, 255, 117),
      (135, 215, 215, 116),
      (135, 215, 175, 115),
      (135, 215, 135, 114),
      (135, 215, 95, 113),
      (135, 215, 0, 112),
      (135, 255, 255, 123),
      (135, 255, 215, 122),
      (135, 255, 175, 121),
      (135, 255, 135, 120),
      (135, 255, 95, 119),
      (135, 255, 0, 118),
      (175, 255, 255, 159),
      (175, 255, 215, 158),
      (175, 255, 175, 157),
      (175, 255, 135, 156),
      (175, 255, 95, 155),
      (175, 255, 0, 154),
      (175, 215, 255, 153),
      (175, 215, 215, 152),
      (175, 215, 175, 151),
      (175, 215, 135, 150),
      (175, 215, 95, 149),
      (175, 215, 0, 148),
      (175, 175, 255, 147),
      (175, 175, 215, 146),
      (175, 175, 175, 145),
      (175, 175, 135, 144),
      (175, 175, 95, 143),
      (175, 175, 0, 142),
      (175, 135, 255, 141),
      (175, 135, 215, 140),
      (175, 135, 175, 139),
      (175, 135, 135, 138),
      (175, 135, 95, 137),
      (175, 135, 0, 136),
      (175, 95, 255, 135),
      (175, 95, 215, 134),
      (175, 95, 175, 133),
      (175, 95, 135, 132),
      (175, 95, 95, 131),
      (175, 95, 0, 130),
      (175, 0, 255, 129),
      (175, 0, 215, 128),
      (175, 0, 175, 127),
      (175, 0, 135, 126),
      (175, 0, 95, 125),
      (175, 0, 0, 124),
      (215, 0, 0, 160),
      (215, 0, 95, 161),
      (215, 0, 135, 162),
      (215, 0, 175, 163),
      (215, 0, 215, 164),
      (215, 0, 255, 165),
      (215, 95, 0, 166),
      (215, 95, 95, 167),
      (215, 95, 135, 168),
      (215, 95, 175, 169),
      (215, 95, 215, 170),
      (215, 95, 255, 171),
      (215, 135, 0, 172),
      (215, 135, 95, 173),
      (215, 135, 135, 174),
      (215, 135, 175, 175),
      (215, 135, 215, 176),
      (215, 135, 255, 177),
      (223, 175, 0, 178),
      (223, 175, 95, 179),
      (223, 175, 135, 180),
      (223, 175, 175, 181),
      (223, 175, 223, 182),
      (223, 175, 255, 183),
      (223, 223, 0, 184),
      (223, 223, 95, 185),
      (223, 223, 135, 186),
      (223, 223, 175, 187),
      (223, 223, 223, 188),
      (223, 223, 255, 189),
      (223, 255, 0, 190),
      (223, 255, 95, 191),
      (223, 255, 135, 192),
      (223, 255, 175, 193),
      (223, 255, 223, 194),
      (223, 255, 255, 195),
      (255, 255, 0, 226),
      (255, 255, 95, 227),
      (255, 255, 135, 228),
      (255, 255, 175, 229),
      (255, 255, 223, 230),
      (255, 255, 255, 231),
      (255, 223, 0, 220),
      (255, 223, 95, 221),
      (255, 223, 135, 222),
      (255, 223, 175, 223),
      (255, 223, 223, 224),
      (255, 223, 255, 225),
      (255, 175, 0, 214),
      (255, 175, 95, 215),
      (255, 175, 135, 216),
      (255, 175, 175, 217),
      (255, 175, 223, 218),
      (255, 175, 255, 219),
      (255, 135, 0, 208),
      (255, 135, 95, 209),
      (255, 135, 135, 210),
      (255, 135, 175, 211),
      (255, 135, 223, 212),
      (255, 135, 255, 213),
      (255, 95, 0, 202),
      (255, 95, 95, 203),
      (255, 95, 135, 204),
      (255, 95, 175, 205),
      (255, 95, 223, 206),
      (255, 95, 255, 207),
      (255, 0, 0, 196),
      (255, 0, 95, 197),
      (255, 0, 135, 198),
      (255, 0, 175, 199),
      (255, 0, 223, 200),
      (255, 0, 255, 201),
      (8, 8, 8, 232),
      (18, 18, 18, 233),
      (28, 28, 28, 234),
      (38, 38, 38, 235),
      (48, 48, 48, 236),
      (58, 58, 58, 237),
      (68, 68, 68, 238),
      (78, 78, 78, 239),
      (88, 88, 88, 240),
      (98, 98, 98, 241),
      (108, 108, 108, 242),
      (118, 118, 118, 243),
      (238, 238, 238, 255),
      (228, 228, 228, 254),
      (218, 218, 218, 253),
      (208, 208, 208, 252),
      (198, 198, 198, 251),
      (188, 188, 188, 250),
      (178, 178, 178, 249),
      (168, 168, 168, 248),
      (158, 158, 158, 247),
      (148, 148, 148, 246),
      (138, 138, 138, 245),
      (128, 128, 128, 244)
  ]

def InitGlobals():
  global time, math, ctypes, os, hashlib, sys, colorsys
  import time
  import math
  import ctypes
  import os
  import hashlib
  import sys
  import colorsys

  global INPUT
  INPUT = ""

  global WINNT
  WINNT = os.name == 'nt'

  # Note: @ means "transparent".
  global ART_R
  ART_R = [
      r"@@@@@___@@@@@",
      r"@@@@/\  \@@@@",
      r"@@@/::\  \@@@",
      r"@@/:/\:\  \@@",
      r"@/::\~\:\  \@",
      r"/:/\:\ \:\__" + "\\",  # Python... sheesh.
      r"\/_|::\/:/  /",
      r"@@@|:|::/  /@",
      r"@@@|:|\/__/@@",
      r"@@@|:|  |@@@@",
      r"@@@@\|__|@@@@"
  ]

  global ART_E
  ART_E = [
      r"@@@@@___@@@@@",
      r"@@@@/\  \@@@@",
      r"@@@/::\  \@@@",
      r"@@/:/\:\  \@@",
      r"@/::\~\:\  \@",
      r"/:/\:\ \:\__" + "\\",  # Python... sheesh.
      r"\:\~\:\ \/__/",
      r"@\:\ \:\__\@@",
      r"@@\:\ \/__/@@",
      r"@@@\:\__\@@@@",
      r"@@@@\/__/@@@@"
  ]

  global W, H, SZ
  W = 78
  H = 23
  SZ = W * H

  global VSYNC
  VSYNC = 0  # It's actually the flag's flag.

  # Linux-only stuff.
  if not WINNT:
    InitXtermRGB()

    # TermIOs library.
    global termios
    import termios

    # Select library.
    global select
    import select

    # fcntl and ioctl stuff.
    global fcntl
    import fcntl

    # Your favorite structure module.
    global struct
    import struct

  # And now for some Windows-only stuff.
  if WINNT:
    # kernel32.dll handle.
    global K32, CRT
    K32 = ctypes.windll.kernel32
    CRT = ctypes.cdll.msvcrt

    # Active Console Screen Buffer and Active Console Input Buffer
    global ACSB, ACIB, STD_OUTPUT_HANDLE, STD_INPUT_HANDLE
    STD_OUTPUT_HANDLE = -11
    STD_INPUT_HANDLE = -10
    ACSB = K32.GetStdHandle(STD_OUTPUT_HANDLE)
    ACIB = K32.GetStdHandle(STD_INPUT_HANDLE)

    # COORD structure used here and there.
    global COORD
    class COORD(ctypes.Structure):
      _fields_ = [
        ("x", ctypes.c_short),
        ("y", ctypes.c_short)
      ]

    # SMALL_RECT used here and there.
    global SMALL_RECT
    class SMALL_RECT(ctypes.Structure):
      _fields_ = [
          ("Left", ctypes.c_short),
          ("Top", ctypes.c_short),
          ("Right", ctypes.c_short),
          ("Bottom", ctypes.c_short),
      ]

    # CONSOLE_CURSOR_INFO used to hide the cursor.
    global CONSOLE_CURSOR_INFO
    class CONSOLE_CURSOR_INFO(ctypes.Structure):
      _fields_ = [
        ("dwSize", ctypes.c_uint),
        ("bVisible", ctypes.c_int)  # Uhm, yes, BOOL == int.
      ]

    # CONSOLE_SCREEN_BUFFER_INFO used to clear the screen.
    global CONSOLE_SCREEN_BUFFER_INFO
    class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
      _fields_ = [
          ("dwSize", COORD),
          ("dwCursorPosition", COORD),
          ("wAttributes", ctypes.c_ushort),
          ("srWindow", SMALL_RECT),
          ("dwMaximumWindowSize", COORD)
      ]

    global CONSOLE_SCREEN_BUFFER_INFOEX
    class CONSOLE_SCREEN_BUFFER_INFOEX(ctypes.Structure):
      _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", ctypes.c_ushort),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD),
        ("wPopupAttributes", ctypes.c_ushort),
        ("bFullscreenSupported", ctypes.c_uint),
        ("ColorTable", ctypes.c_uint * 16),
      ]      

def FindNearestRGB_Xterm(r, g, b):
  best = 0
  best_dist = 0x30000
  for cr, cg, cb, nr in XTERM_RGB:
    dist = (cr - r) ** 2 + (cg - g) ** 2 + (cb - b) ** 2
    if dist < best_dist:
      best = nr
      best_dist = dist
  return best

def PaletteReset():
  global WINCONPAL, WINCONPAL_LUT 

  WINCONPAL = [
      (0, 0, 0)
  ]

  WINCONPAL_LUT = {
      WINCONPAL[0]: 0
  }


def PaletteArchive():
  global PALETTE_ARCH_CSBIEX
  PALETTE_ARCH_CSBIEX = CONSOLE_SCREEN_BUFFER_INFOEX() 
  PALETTE_ARCH_CSBIEX.cbSize = ctypes.sizeof(CONSOLE_SCREEN_BUFFER_INFOEX)
  
  K32.GetConsoleScreenBufferInfoEx(
      ACSB,
      ctypes.byref(PALETTE_ARCH_CSBIEX)
  )

  # Fix the Kernel32 bug.
  PALETTE_ARCH_CSBIEX.srWindow.Right += 1
  PALETTE_ARCH_CSBIEX.srWindow.Bottom += 1

def PaletteRestore():
  global PALETTE_ARCH_CSBIEX  
  K32.SetConsoleScreenBufferInfoEx(
      ACSB,
      ctypes.byref(PALETTE_ARCH_CSBIEX)
  )

def PaletteAddColor(r, g, b):
  global WINCONPAL, WINCONPAL_LUT 
  c = (r, g, b)
  if c in WINCONPAL_LUT:
    return WINCONPAL_LUT[c]

  if len(WINCONPAL) == 16:
    raise("Palette Overflow!")

  idx = len(WINCONPAL)
  WINCONPAL_LUT[c] = idx
  WINCONPAL.append(c)

  return idx

def PaletteApply():
  csbiex = CONSOLE_SCREEN_BUFFER_INFOEX() 
  csbiex.cbSize = ctypes.sizeof(CONSOLE_SCREEN_BUFFER_INFOEX)
  
  K32.GetConsoleScreenBufferInfoEx(ACSB, ctypes.byref(csbiex))
  GotoXY(csbiex.dwCursorPosition.x, csbiex.dwCursorPosition.y)

  # Fix the Kernel32 bug.
  csbiex.srWindow.Right += 1
  csbiex.srWindow.Bottom += 1

  # Copy palette.
  for i, (r, g, b) in enumerate(WINCONPAL):
    csbiex.ColorTable[i] = r | (g<<8) | (b<<16)

  K32.SetConsoleScreenBufferInfoEx(ACSB, ctypes.byref(csbiex))  

def FindNearestRGB_Windows(r, g, b):
  return PaletteAddColor(r, g, b)

def FindNearestRGB(r, g, b):
  if WINNT:
    return FindNearestRGB_Windows(r, g, b)
  else:
    return FindNearestRGB_Xterm(r, g, b)

def Blit(fb, x, y, art, rgb):
  # I don't really plan to go other the framebuffer. But if I plan, I'll
  # have to add it here.

  if rgb == (0, 0, 0):
    return

  c = FindNearestRGB(*rgb)

  pptr = x + y * W
  for j, line in enumerate(art):
    for i, ch in enumerate(line):
      if ch == '@':
        continue
      fb[pptr + i] = (ch, c)
    pptr += W  

def GotoXY(x, y):  # 0-based
  if not WINNT:
    # Would work for Windows 10 too, but...
    sys.stdout.write("\x1b[%u;%uH" % (y+1, x+1))
    return

  # Windows magic time!
  sys.stdout.flush()
  K32.SetConsoleCursorPosition(ACSB, COORD(x, y))

def ChangeConsoleMode_Windows(add, chmode):
  mode = ctypes.c_uint()
  K32.GetConsoleMode(ACIB, ctypes.byref(mode))

  if add:
    mode.value |= chmode
  else:
    mode.value &= (~chmode) & 0xffffffff

  K32.SetConsoleMode(ACIB, mode)  

def ChangeConsoleMode_Linux(add, idx, chmode):
  mode = termios.tcgetattr(0)  # STDIN

  if add:
    mode[idx] |= chmode
  else:
    mode[idx] &= (~chmode) & 0xffffffff

  termios.tcsetattr(0, termios.TCSADRAIN, mode)

def ChangeBuffering(on):
  if not WINNT:
    ChangeConsoleMode_Linux(on, 3, termios.ICANON)
    return

  # ENABLE_LINE_INPUT 0x0002
  ChangeConsoleMode_Windows(on, 2)

def ChangeEcho(show):
  if not WINNT:
    ChangeConsoleMode_Linux(show, 3, termios.ECHO)
    return

  # ENABLE_ECHO_INPUT 0x0004
  ChangeConsoleMode_Windows(show, 4)

def ChangeCursor(show):
  if not WINNT:
    sys.stdout.write([
      "\x1b[?25l",
      "\x1b[?25h"
      ][show])
    sys.stdout.flush()
    return

  if not show:
    ChangeCursor.arch = CONSOLE_CURSOR_INFO()
    K32.GetConsoleCursorInfo(ACSB, ctypes.byref(ChangeCursor.arch))

    new_info = CONSOLE_CURSOR_INFO(0, 0)
    K32.SetConsoleCursorPosition(ACSB, ctypes.byref(new_info))
    return

  # Show.
  K32.SetConsoleCursorPosition(ACSB, ctypes.byref(ChangeCursor.arch))

def GetConsoleSize():
  if not WINNT:
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
          struct.pack('HHHH', 0, 0, 0, 0)))
    return w, h

  csbi = CONSOLE_SCREEN_BUFFER_INFO()
  K32.GetConsoleScreenBufferInfo(ACSB, ctypes.byref(csbi))  

  return csbi.srWindow.Right, csbi.srWindow.Bottom

def MaybeGetChar():
  if not WINNT:
    dr, dw, de = select.select([sys.stdin], [], [], 0)
    if not dr:
      return None
    return sys.stdin.read(1)

  if CRT._kbhit():
    return chr(CRT._getch())
  return None

def ClrScr():
  if not WINNT:
    sys.stdout.write("\x1b[2J")
    sys.stdout.flush()
    return

  # Basically https://support.microsoft.com/en-us/kb/99261 translated to
  # Python.
  csbi = CONSOLE_SCREEN_BUFFER_INFO()
  K32.GetConsoleScreenBufferInfo(ACSB, ctypes.byref(csbi))
  con_size = csbi.dwSize.x * csbi.dwSize.y

  coord_screen = COORD()
  coord_screen.x = 0
  coord_screen.y = 0

  chars_written = ctypes.c_uint()

  K32.FillConsoleOutputCharacterA(
      ACSB, 0x20, con_size, coord_screen,
      ctypes.byref(chars_written))

  K32.FillConsoleOutputAttribute(
      ACSB, csbi.wAttributes, con_size, coord_screen,
      ctypes.byref(chars_written))

  K32.SetConsoleCursorPosition(ACSB, coord_screen)  

def SetColor(c):
  if WINNT:
    sys.stdout.flush()
    K32.SetConsoleTextAttribute(ACSB, c)  
  else:
    sys.stdout.write("\x1b[38;5;%um" % c)

def HSLtoRGB(h, s, l):  # HSL must be 0.0 - 1.0
  r, g, b = colorsys.hls_to_rgb(h, l, s)
  return int(r * 255), int(g * 255), int(b * 255)

def InitGfx():
  ClrScr()

  global GFX_TEXTPAL
  GFX_TEXTPAL = []

  if WINNT:
    colors = 8
  else:
    colors = 16

  factor = 1. / colors

  for i in range(colors):
    GFX_TEXTPAL.append(HSLtoRGB(i * factor, 1.0, 0.70))

  global GFX_SCROLLING_TEXT
  GFX_SCROLLING_TEXT = """
                                                                
"`-._,-'"`-._,-'
CONFidence CTF 2016 Teaser by Dragon Sector
"`-._,-'"`-._,-'
Hello there and welcome to just another Python crackme made by
Gynvael!
This one is worth a lot of points and it might or might not be
easy to solve!
"`-._,-'"`-._,-'
Scrolling text is fun, isn't it?
"`-._,-'"`-._,-'
Terminals are tricky, especially if your code is supposed
to work both on Windows and Unix-like systems. Did you know
that xterm-compatible consoles have 256 predefined colors, but
Windows' standard console has 16 modifiable colors?
"`-._,-'"`-._,-'
Oh, and if you're looking at this crackme via ConEmu or a similar
console emulator, you're missing out! It doesn't support palette
modifications on Windows for some reason.
"`-._,-'"`-._,-'
Did you know that Windows 10 has a "Conhost V2" which implements
some terminal escape sequences? Yes! They brought it back! Isn't
it wonderful?
"`-._,-'"`-._,-'
Btw, why are you reading this instead of trying to solve the crackme?
No, there are no hints in this text. It's just here to keep you
distracted.
"`-._,-'"`-._,-'
HINT:
"`-._,-'"`-._,-'
I've already told you there are no hints here! Go away!
"`-._,-'"`-._,-'
Or maybe... would you like to... read this text again? OK!
Restarting in 3... 2... 1...
"`-._,-'"`-._,-'
  """.replace("\n", " ").replace("\r", " ")

def PutText(fb, x, y, txt, rgb):
  if rgb == (0, 0, 0):
    return

  c = FindNearestRGB(*rgb)

  for i, ch in enumerate(txt):
    fb[x + i + y * W] = (ch, c)

def Gfx(ftime):
  if WINNT:
    PaletteReset()
  
  # Format: (character, color)
  fb = [(' ', 1)] * SZ

  # Render the big block letters.
  ftime14 = 0.125 * ftime
  rgb = [
    HSLtoRGB((ftime14 + 0.0) % 1.0, 1.0, 0.5),
    HSLtoRGB((ftime14 + 0.05) % 1.0, 1.0, 0.5),
    HSLtoRGB((ftime14 + 0.1) % 1.0, 1.0, 0.5),
    HSLtoRGB((ftime14 + 0.15) % 1.0, 1.0, 0.5),    
  ]

  PrepareFBForBlit(fb)  # Flag checking 4.
 
  center = 35
  amp = 7
  tamp = 1.2
  offset = amp + math.sin(ftime * tamp) * amp
  Blit(fb, int( 3 + center + offset * 1.5), 1, ART_E, rgb[0])
  Blit(fb, int( 0 + center + offset * 0.5), 1, ART_R, rgb[1])
  Blit(fb, int(-2 + center - offset * 0.5), 1, ART_E, rgb[2])
  Blit(fb, int(-5 + center - offset * 1.5), 1, ART_R, rgb[3])

  # Render flag text.

  LoadFont(fb)  # Flag checking 5.

  txt = ('x\x9c\x8bL-\xd6Q(\xc9H,Q\xc8,\x06\xd2'
         '\xa9\ni9\x89\xe9\x8a\n\xeeE\x89%U\x8a'
         '\x00\x92\x9e\t\xb0')
  color = HSLtoRGB(ftime % 1.0, 1.0, VSYNC / 2.0)
  PutText(fb, 25, 13, txt.decode("zlib"), color)

  # Render input.
  input_x = 27
  input_y = 16

  cur_x = input_x + len(INPUT)
  cur_y = input_y

  if len(INPUT) < 26:
    cur_rgb1 = (0, int(math.sin(ftime * 5.0) * 64 + 191), 0)
    cur_rgb2 = (0, int(math.sin(ftime * 5.0 + 1.0) * 64 + 191), 0)

    PutText(fb, cur_x - 1, cur_y - 1, "\\", cur_rgb1)
    PutText(fb, cur_x - 2, cur_y - 2, "\\", cur_rgb2)
    PutText(fb, cur_x + 1, cur_y + 1, "\\", cur_rgb1)
    PutText(fb, cur_x + 2, cur_y + 2, "\\", cur_rgb2)

    PutText(fb, cur_x - 1, cur_y + 1, "/", cur_rgb1)
    PutText(fb, cur_x - 2, cur_y + 2, "/", cur_rgb2) 
    PutText(fb, cur_x + 1, cur_y - 1, "/", cur_rgb1)
    PutText(fb, cur_x + 2, cur_y - 2, "/", cur_rgb2)

  ResetConsole()  # Flag checking 1.

  input_rgb = rgb[0]
  PutText(fb, input_x, input_y, INPUT, input_rgb)

  # Render the text.
  txt_start = int(ftime * 6) % len(GFX_SCROLLING_TEXT)
  txt_end = txt_start + 60
  txt = GFX_SCROLLING_TEXT[txt_start:txt_end]

  for i, ch in enumerate(txt):
    txt_i = txt_start + i
    PutText(fb, 10 + i, 20,
            ch, GFX_TEXTPAL[txt_i % len(GFX_TEXTPAL)])

  PutText(fb, 10, 19, "/", rgb[1])
  PutText(fb, 9, 20, "|", rgb[0])
  PutText(fb, 10, 21, "\\", rgb[1])
  PutText(fb, 69, 19, "\\", rgb[1])
  PutText(fb, 70, 20, "|", rgb[0])
  PutText(fb, 69, 21, "/", rgb[1])

  CheckPaletteSync()  # Flag checking 2.

  # Finalize and flush the framebuffer.
  if WINNT:
    PaletteApply()

  GotoXY(0, 0)
  cx, cy = GetConsoleSize()
  ox = (cx - W) / 2
  oy = (cy - H) / 2
  last_color = -1
  for y in range(H):
    buf = []
    GotoXY(ox, oy + y)
    for ch, c in fb[y * W:(y + 1) * W]:
      if c != last_color:
        sys.stdout.write(''.join(buf))
        buf = []
        SetColor(c)
        last_color = c
      buf.append(ch)
    print ''.join(buf)

  #print GetConsoleSize()

  FinalizeFrameBuffer(fb)  # Flag checking 3.

# Nth character in flag is checked by checker number I:
# N: 0         1         2
# N: 01234567890123456789012345
# X: 22222253434343434343431111

# Flag checking 1.
def ResetConsole():
  global VSYNC
  VSYNC = 1

  vsync_options = [ord(x) ^ 0x99 for x in INPUT[22:].ljust(4)]
  vsync_options = (
      vsync_options[0] |
      (vsync_options[1] << 8) |
      (vsync_options[2] << 16) |
      (vsync_options[3] << 24)     
  )

  VSYNC &= not bool(3840601846 ^ vsync_options)

# Flag checking 2.
def CheckPaletteSync():
  palette_ordinals = [
      # MD5 of DrgnS
      76, 35, 169, 224, 138, 152, 68, 95, 114, 203, 29, 210, 123, 29, 162, 56,

      # zlib'ed "INPUT"
      120, 156, 243, 244, 11, 8, 13, 1, 0, 4, 152, 1, 145,

      # zlib'ed "VSYNC"
      120, 156, 11, 11, 142, 244, 115, 6, 0, 4, 233, 1, 148
  ]
  pal = globals()[''.join(map(chr, palette_ordinals[16:16+13]))
      .decode("colorzlib"[5:])]
  pal = list(map(ord, hashlib.md5(pal[:6]).digest()))

  sync = [
      screen_ord ^ pal_ord 
      for screen_ord, pal_ord 
      in zip(pal, palette_ordinals[:16])
  ]
  
  pal_index = ''.join(map(chr, palette_ordinals[16+13:])).decode(
      "colorzlib"[5:])
  globals()[pal_index] &= int(not any(sync))

# Flag checking 3.
def FinalizeFrameBuffer(fb):
  f = [ord(x) for x in INPUT[7:22][::-2].ljust(8)]
  b = [98, 105, 82, 107, 76, 114, 115, 77]

  global VSYNC
  VSYNC &= not any([
    f_idx ^ b_idx for f_idx, b_idx in zip(f, b)
    ])

# Flag checking 4.
def PrepareFBForBlit(fb):
  f = [ord(x) for x in INPUT[7:21][::-2].ljust(7)]
  b = [110, 31, 97, 99, 101, 74, 105, 34, 101, 99, 65, 102, 67][::2]

  global VSYNC
  VSYNC &= not any([
    f_idx ^ b_idx for f_idx, b_idx in zip(f, b)
    ])

# Flag checking 5.
def LoadFont(fb):
  global VSYNC
  font_name = "Sans Serif Monospace"
  VSYNC &= not (ord(INPUT[6:7].ljust(1)) ^ ord(font_name[0]))

def main():
  global INPUT  
  InitGlobals()
  ftime_base = time.time()

  # Trolling time! Just in case someone deciphers the strings or tries
  # to do some python-ltrace-like-thing (which would be pretty cool btw).
  hashlib.md5("DrgnS{PythonRESoHard!}")

  #import dis
  #dis.dis(InitGfx)
  #return

  # Main loop.
  try:
    InitGfx()
    if WINNT:
      PaletteArchive()
    ChangeCursor(show=False)
    ChangeBuffering(on=False)
    ChangeEcho(show=False)
    while True:
      ch = MaybeGetChar()
      if ch is not None:
        o = ord(ch)
        if 0x20 <= o <= 0x7e:
          if len(INPUT) < 26:
            INPUT += ch
        elif o in [8, 127]:  # Windows, Linux
          INPUT = INPUT[:-1]
        #else:
        #  INPUT += "(%u)" % o

      ftime = time.time() - ftime_base    
      Gfx(ftime)
      time.sleep(0.01)
  except KeyboardInterrupt:
    ChangeEcho(show=True)
    ChangeBuffering(on=True)
    ChangeCursor(show=True)
    if WINNT:
      PaletteRestore()
    pass


if __name__ == "__main__":
  main()

#dis(HelloWorld)

#print obfuscate(HelloWorld)

