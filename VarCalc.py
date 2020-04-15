import ROOT
from math import pi, sqrt, cos, sin, sinh, log, cosh

def DeltaPhi(phi1, phi2):
    dphi = phi2-phi1
    if  dphi > pi:
        dphi -= 2.0*pi
    if dphi <= -pi:
        dphi += 2.0*pi
    return abs(dphi)

def DeltaR(eta1, phi1, eta2, phi2):
    return sqrt(DeltaPhi(phi1, phi2)**2 + (eta1 - eta2)**2)

def DeltaRMatched(eta, phi, L, thr):
    dr = 99
    for l in L:
        dri = DeltaR(l['eta'], l['phi'], eta, phi)
        if dri < dr: dr = dri
    return True if dr < thr else False

def sortedlist(l, k='pt'):
    sl = sorted(l, key = lambda d: d[k], reverse=True)
    return sl

def MT(pt, phi, metpt, metphi):
    return sqrt(2 * pt * metpt * (1 - cos(phi - metphi)))

def CT1(met, HT):
    return min(met, HT-100)

def CT2(met, ISRpt):
    return min(met, ISRpt-25)

    
def GenFlagString(flag):
    s = '{0:15b}'.format(flag)
    return s

"""
Comments on gen status flags:
According to the CMSSW GEN structure(), following bits are used for different status. 
So we need to check the correspoding element in the bit string returned by GenFlagString function
string index = 14-bit

"0 : isPrompt," : s[14] or s[-1] 
"1 : isDecayedLeptonHadron, "
"2 : isTauDecayProduct, "
"3 : isPromptTauDecayProduct, "
"4 : isDirectTauDecayProduct, "
"5 : isDirectPromptTauDecayProduct, "
"6 : isDirectHadronDecayProduct, "
"7 : isHardProcess, " 
"8 : fromHardProcess, " : s[6]
"9 : isHardProcessTauDecayProduct, "
"10 : isDirectHardProcessTauDecayProduct, "
"11 : fromHardProcessBeforeFSR, " : s[3]
"12 : isFirstCopy, " : s[2]
"13 : isLastCopy, "  : s[1]
"14 : isLastCopyBeforeFSR : s[0]

"""

def Fill1D(h, a, w=1):
    nbin = h.GetNbinsX()
    low = h.GetBinLowEdge(nbin)
    high = h.GetBinLowEdge(nbin + 1)
    copy = a
    if copy >= high: copy = low
    h.Fill(copy, w)

def Fill2D(h, a, b, w=1):
    nbinx = h.GetNbinsX()
    lowx = h.GetBinLowEdge(nbinx)
    highx = h.GetBinLowEdge(nbinx + 1)
    copyx = a
    if copyx >= highx: copyx = lowx
    nbiny = h.GetNbinsY()
    lowy = h.GetBinLowEdge(nbiny)
    highy = h.GetBinLowEdge(nbiny + 1)
    copyy = a
    if copyy >= highy: copyy = lowy
    h.Fill(copyx, copyy, w)
