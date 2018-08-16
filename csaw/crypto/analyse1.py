#!/usr/bin/python



t1="""I fys  cop whhrt"ioawoelpla.alelr s  edTigyn heeogiestuef t  . m ad yaanoIognontuist'  cwhtsh ee haprrhovh" auer.cvl a heddsFa  oeolabn rl eef ep  oynrflrogoao uebityr!lrso .el uemyorf  f fws eoitbfrt"""
t2="""I fysy cop ohhrt"uoawom pla.owelr ri edTelyn h logiea uef ng . msed yawtoIoge ntuira'  csntsh  o haphthovhehauerrevl aeredds"   oe.cabn  h eefFap  oolrflrrloao  ebityynlrsoogel uuemyorr!  f  .ws eeitb"""


s=""
for i in range(len(t1)):
    c=' '
    if t1[i]!=t2[i]:
        diff=ord(t1[i])-ord(t2[i])
        print diff
        c='#'
    s+=c
print s
print t1
