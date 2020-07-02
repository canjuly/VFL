import math

debug = False

def cal_jaccard(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("jaccard:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    a = Ncf + Nuf + Ncp
    if a == 0:
        return 0
    b = Ncf / a
    return b

def cal_naish(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("naish:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    a = Ncp + Nup + 1
    b = Ncf - Ncp / a
    return b

def cal_GP08(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("GP08:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    a = Ncf * Ncf
    b = 2 * Ncp + 2 * Ncf + 3 * Nup
    c = a * b
    return c

def cal_GP10(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("GP10:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    if Nup == 0:
        return 0
    a = Ncf - 1 / Nup
    b = math.sqrt(a)
    return b

def cal_GP11(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("GP11:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    a = Ncf * Ncf
    b = math.sqrt(Nup)
    c = a * (a + b)
    return c

def cal_GP13(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("GP13:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    a = 2 * Ncp + Ncf
    if a == 0:
        return 0
    b = Ncf * (1 + 1 / a)
    return b

def cal_GP20(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("GP20:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    a = Ncp + Nup
    if a == 0:
        return 0
    b = 2 * (Ncf + Nup / a)
    return b

def cal_GP26(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("GP26:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    a = Ncf * Ncf
    b = math.sqrt(Nup)
    c = 2 * a + b
    return c

def cal_turantula(Ncf, Nuf, Ncp, Nup):
    if debug:
        print("turantula:%d %d %d %d" %(Ncf, Nuf, Ncp, Nup))
    if Ncf + Nuf == 0:
        return 0
    if Ncp + Nup == 0:
        return 0
    a = Ncf / (Ncf + Nuf)
    b = Ncp / (Ncp + Nup)
    c = a / (a + b)
    return c

def cal_dstar(tf, tp, aef, aep, anf, anp, index):
    if debug:
        print("Dstar:%d %d %d %d %d %d" %(tf, tp, aef, aep, anf, anp))
    a = aep + (tf - aef)
    if a == 0:
        return 0
    b = math.pow(aef, index)
    c = b / a
    return c


def cal_ochiai(tf, tp, aef, aep, anf, anp):
    if debug:
        print("Ochiai:%d %d %d %d %d %d" %(tf, tp, aef, aep, anf, anp))
    if aef == 0:
        return 0
    a = aef + aep
    b = math.sqrt(tf * a)
    if b == 0:
        return 0
    c = aef / b
    return c


def cal_ochiai_new(tf, tp, aef, aep, anf, anp):
    if debug:
        print("Ochiai_new:%d %d %d %d %d %d" %(tf, tp, aef, aep, anf, anp))
    if aef == 0:
        return 0
    a = aef + aep
    b = math.sqrt(tf * a)
    if b == 0:
        return 0
    c = math.pow(aef, 3) / b
    return c


def cal_op2(tf, tp, aef, aep, anf, anp):
    if debug:
     print("op2:%d %d %d %d %d %d" %(tf, tp, aef, aep, anf, anp))
    a = aep / (tp + 1)
    b = aef - a
    return b