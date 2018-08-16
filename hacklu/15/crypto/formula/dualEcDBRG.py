#!/usr/bin/env python3

from randomSeed import randomNumber
from utils import EllipticCurve

class DualEcDbrg():
    def __init__(self):
        self.paramA = (-3)
        self.paramB = 2455155546008943817740293915197451784769108058161191238065 
        self.modulus = 6277101735386680763835789423207666416083908700390324961279 

        self.ellipticCurve = EllipticCurve(self.paramA, self.paramB, self.modulus) 

        self.basePointP = (602046282375688656758213480587526111916698976636884684818, 174050332293622031404857552280219410364023488927386650641)

        self.multiplier = 2183135607296040804176246882406033987585449191869874092818 

        self.basePointQ = self.ellipticCurve.doubleAdd(self.basePointP, self.multiplier) 

        self.initialVector = randomNumber(1, 2**256)
        self.seed = self.ellipticCurve.doubleAdd(self.basePointP, self.initialVector)[0]
        
        # This is P-192 NIST standard curve !!!
        # Don't even try to bruteforce something here

    def getRandInt(self):
        self.seed = self.ellipticCurve.doubleAdd(self.basePointP, self.seed)[0]
        return self.ellipticCurve.doubleAdd(self.basePointQ, self.seed)[0]



