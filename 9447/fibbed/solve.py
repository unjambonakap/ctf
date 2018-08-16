#!/usr/bin/env python

prime = 981725946171163877
s1 = 58449491987662952
s2 = 704965025359609904
c1 = 453665378628814896
c2 = 152333692332446539

def mult(m1, m2):
  r = [[0, 0], [0, 0]]
  for i in range(2):
    for j in range(2):
      t = 0
      for k in range(2):
        t += m1[i][k] * m2[k][j]
      r[i][j] = t % prime
  return r

def faste(m, pw):
  x=[[1,0],[0,1]]
  while pw>0:
    print(pw)
    if pw&1:
      x=mult(m,x)
    m=mult(m,m)
    pw>>=1
  return x



def main():
  store=int(1e6)
  step=prime//store
  data={}
  M=[[0,1], [1,1]]
  M=faste(M, step)

  cur=[[1,0],[0,1]]
  for i in range(store+1):
    x=cur[0]
    data[tuple(x)]=i
    cur=mult(M,cur)
    if i%1000==0:
      print(i, store)
  print('done')




main()
