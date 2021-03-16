import ROOT
from math import pi, sqrt, cos, sin, sinh, log, cosh
import textwrap

from CosmeticCode import vidNestedWPBitMapNamingList

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

def DeltaRPtMatched(pt, eta, phi, L, thr, ptthr):
    dr = 99
    pT = 999
    for l in L:
        dri = DeltaR(l['eta'], l['phi'], eta, phi)
        if dri < dr:
            dr = dri
            pT = l['pt']
    return True if dr < thr and abs(1- pt/pT) < ptthr else False

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

# convert int of vidNestedWPBitMap ( e.g. val = 611099940 ) to bitmap ( e.g. "100100011011001010010100100100")
# split vidBitmap string (containing 3 bits per cut) in parts of 3 bits ( e.g. ["100","100","011","011","001","010","010","100","100","100"] )
# convert 3 bits to int ( e.g. [4, 4, 3, 3, 1, 2, 2, 4, 4, 4])

def vidNestedWPBitMapToDict( vid ):
    idList = [ int( x, 2 ) for x in textwrap.wrap( "{0:030b}".format( vid ) , 3) ]
    return dict( zip( vidNestedWPBitMapNamingList, idList ) )

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def eleVID( vid, idVal, removedCuts=[] ):
    vidDict    = vidNestedWPBitMapToDict( vid )
    if not removedCuts:
        return all( [ cut >= idVal for cut in vidDict.values() ] )
    
    if ("pt"             in removedCuts):
        vidDict = removekey( vidDict, "MinPtCut" )
    if ("sieie"          in removedCuts):
        vidDict = removekey( vidDict, "GsfEleFull5x5SigmaIEtaIEtaCut" )
    if ("hoe"            in removedCuts):
        vidDict = removekey( vidDict, "GsfEleHadronicOverEMEnergyScaledCut" )
    if ("pfRelIso03_all" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleRelPFIsoScaledCut" )
    if ("SCEta" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleSCEtaMultiRangeCut" )
    if ("dEtaSeed" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleDEtaInSeedCut" )
    if ("dPhiInCut" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleDPhiInCut" )
    if ("EinvMinusPinv" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleEInverseMinusPInverseCut" )
    if ("convVeto" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleConversionVetoCut" )
    if ("lostHits" in removedCuts):
        vidDict = removekey( vidDict, "GsfEleMissingHitsCut" )
        
    return all( [ cut >= idVal for cut in vidDict.values() ] )

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
