#!/usr/bin/env python3

class EllipticCurve():
    def __init__(self, a, b, modulus):
        self.a = a
        self.b = b
        self.modulus = modulus

    def doubleAdd(self, base, multiplier):
        binMultiplier = bin(multiplier)[3:]          
        val = base 
        
        for c in binMultiplier:
            val = self.addPoint(val, val)
            if (c == '1'):
                val = self.addPoint(val, base)
                
        return val


    def addPoint(self, p1, p2):
        if (p1 != None and p2 != None):
            s = 0
            
            x1 = p1[0]
            y1 = p1[1]
            x2 = p2[0]
            y2 = p2[1]
            
            if (p1 == p2):
                s = (((3 * x1 * x1) + self.a) * pow((2 * y1), (self.modulus - 2), self.modulus )) % self.modulus 
            elif (x1 != x2):
                s = ((y2 - y1) * pow((x2 - x1), (self.modulus - 2), self.modulus)) % self.modulus
            else:
                return None

            x3 = ((s * s) - x1 - x2) % self.modulus
            y3 = (s * (x1 - x3) - y1) % self.modulus

            return (x3 ,y3)
        return None

    def checkValidity(self):
        return (((4 * pow(self.a, 3, self.modulus) + (27 * pow(self.b, 2, self.modulus))) % self.modulus) != 0)

class SquareAndMultiply():
    def __init__(self):
        pass
        
    def sqm(self, base, exponent, modulus):
        binExponent = bin(exponent)[2:]            
        val = base
        
        for c in binExponent[1:]:
            val = pow(val, 2, modulus)
            if (c == '1'):
                val = (val * base) % modulus
                
        return val

