#!/usr/bin/env python


from curses.ascii import isprint
lst='83 230 69 128 66 214 89 24 92 204'.split(' ')
lst=list(map(int, lst))
n=len(lst)

for i in range(2):
  for j in range(i+1):
    tb=lst[j::i+1]
    print('for ', i, j, tb)
    for x in range(256):
      for a in tb:
        if not isprint(chr((256-a+x)%128)):
          break
      else:
        print(''.join([chr((a^x)%128) for a in tb]))


u=[lst[i+1]-lst[i] for i in range(n-1)]
print(u)
