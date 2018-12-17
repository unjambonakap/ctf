import hashlib
def checkit(a):
  a = a.encode()
  n = len(a)
  for i in range(n):
    if a[i] != ord('0'): break
  if i == 0: return 0
  if a[i] != ord('e'):
    return 0
  for j in range(i+1, n):
    if a[j] > 90: return 0
  return 1


assert checkit('0e123418218')
assert checkit('000e123418218')
assert not checkit('000e1234182a8')
assert not checkit('100e1234182a8')

for i in range(2**35):
  x = str(i)+'Shrewk'
  r = hashlib.md5(x.encode()).hexdigest()
  if checkit(r):
    print('PASS  = ', i)
    break
