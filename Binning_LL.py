import ROOT
import math
import os, sys


CT_bin = [300, 400, -1]
MT_bin = [0, 60, 95, 130, -1]
LepPt_bin = [3, 5, 12, 20, 30]
ElePt_bin = [5, 12, 20, 30]

EachMT_div = len(LepPt_bin)-1
EachCT_div = (len(LepPt_bin)-1) * (len(MT_bin)-1) - 1 #for last MT bin, leppT start from 5 GeV


def findSR1BinIndex(CT, MT, LepPt, LepChrg):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        cutchrg = LepChrg==-1 if j < len(MT_bin)-3 else True # -1 charge only for first two MT bins
        for i in range(len(CT_bin)-1):
            cut2 = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
            lep = ElePt_bin if j >= len(MT_bin)-3 else LepPt_bin #for last two MT bin, leppT start from 5 GeV
            for k in range(len(lep)-1):
                cut3 = LepPt>lep[k] and LepPt<=lep[k+1]
                idx += 1
                if (cut1 and cut2 and cut3 and cutchrg):
                    pickIdx = idx
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    return pickIdx

def findSR2BinIndex(CT, MT, LepPt):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        for i in range(len(CT_bin)-1):
            cut2 = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
            lep = ElePt_bin if j >= len(MT_bin)-3 else LepPt_bin #for last two MT bins, leppT start from 5 GeV
            for k in range(len(lep)-1):
                cut3 = LepPt>lep[k] and LepPt<=lep[k+1]
                idx += 1
                if (cut1 and cut2 and cut3):
                    pickIdx = idx
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    return pickIdx

def findCTBin(CT):
    idx = -1
    pickIdx = -1
    for i in range(len(CT_bin)-1):
        cut = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
        idx += 1
        if (cut):
            pickIdx = idx+1
            break
    return pickIdx

def findMTBin(MT):
    idx = -1
    pickIdx = -1
    for i in range(len(MT_bin)-1):
        cut = MT>MT_bin[i] if i == len(MT_bin)-2 else MT>MT_bin[i] and MT<=MT_bin[i+1]
        idx += 1
        if (cut):
            pickIdx = idx+1
            break
    return pickIdx

def findLepPtBin(LepPt, MT):
    idx = -1
    pickIdx = -1
    lep = ElePt_bin if MT>95 else LepPt_bin #for lasttwo  MT bins, leppT start from 5 GeV
    for i in range(len(lep)-1):
        cut = LepPt>lep[i] if i == len(lep)-2 else LepPt>lep[i] and LepPt<=lep[i+1]
        idx += 1
        if (cut):
            pickIdx = idx+1
            break
    return pickIdx

def findBin(CT, MT, LepPt):
    b = -1
    if findCTBin(CT)>0 and findMTBin(MT)>0 and findLepPtBin(LepPt, MT)>0:
        b = (EachCT_div * (findCTBin(CT)-1)) + (EachMT_div * (findMTBin(MT)-1)) + findLepPtBin(LepPt, MT)
    return b

def findCR1BinIndex(CT, MT, LepChrg):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        cutchrg = LepChrg==-1 if j < len(MT_bin)-3 else True # -1 charge only for first two MT bins
        for i in range(len(CT_bin)-1):
            cut2 = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
            idx += 1
            if (cut1 and cut2 and LepChrg):
                pickIdx = idx
                break
        else:
            continue
        break
            
    return pickIdx

def findCR2BinIndex(CT, MT):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        for i in range(len(CT_bin)-1):
            cut2 = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
            idx += 1
            if (cut1 and cut2):
                pickIdx = idx
                break
        else:
            continue
        break
            
    return pickIdx

CTBinLabelDict = {
    1 : 'X',
    2 : 'Y',
    }

MTBinLabelDict = {
    1 : 'a',
    2 : 'b',
    3 : 'c',
    4 : 'd',
    }

LepPtBinLabelDict = {
    1 : 'VL',
    2 : 'L',
    3 : 'M',
    4 : 'H',
    }

SRBinLabelList = [
    'SR1VLaX',
    'SR1LaX',
    'SR1MaX',
    'SR1HaX',
    'SR1VLaY',
    'SR1LaY',
    'SR1MaY',
    'SR1HaY',
    'SR1VLbX',
    'SR1LbX',
    'SR1MbX',
    'SR1HbX',
    'SR1VLbY',
    'SR1LbY',
    'SR1MbY',
    'SR1HbY',
    'SR1LcX',
    'SR1McX',
    'SR1HcX',
    'SR1LcY',
    'SR1McY',
    'SR1HcY',
    'SR1LdX',
    'SR1MdX',
    'SR1HdX',
    'SR1LdY',
    'SR1MdY',
    'SR1HdY',
    'SR2VLaX',
    'SR2LaX',
    'SR2MaX',
    'SR2HaX',
    'SR2VLaY',
    'SR2LaY',
    'SR2MaY',
    'SR2HaY',
    'SR2VLbX',
    'SR2LbX',
    'SR2MbX',
    'SR2HbX',
    'SR2VLbY',
    'SR2LbY',
    'SR2MbY',
    'SR2HbY',
    'SR2LcX',
    'SR2McX',
    'SR2HcX',
    'SR2LcY',
    'SR2McY',
    'SR2HcY',
    'SR2LdX',
    'SR2MdX',
    'SR2HdX',
    'SR2LdY',
    'SR2MdY',
    'SR2HdY',
    ]

CRBinLabelList = [
    'CR1aX',
    'CR1aY',
    'CR1bX',
    'CR1bY',
    'CR1cX',
    'CR1cY',
    'CR1dX',
    'CR1dY',
    'CR2aX',
    'CR2aY',
    'CR2bX',
    'CR2bY',
    'CR2cX',
    'CR2cY',
    'CR2dX',
    'CR2dY',
    'CR3aX',
    'CR3aY',
    'CR3bX',
    'CR3bY',
    'CR3cX',
    'CR3cY',
    'CR3dX',
    'CR3dY',
    ]

TotLepPt_bin = [3, 5, 12, 20, 30, -1]
TotElePt_bin = [5, 12, 20, 30, -1]

def findReg1BinIndex(CT, MT, LepPt, LepChrg):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        cutchrg = LepChrg==-1 if j < len(MT_bin)-3 else True # -1 charge only for first two MT bins
        for i in range(len(CT_bin)-1):
            cut2 = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
            lep = TotElePt_bin if j >= len(MT_bin)-3 else TotLepPt_bin #for last two MT bin, leppT start from 5 GeV
            for k in range(len(lep)-1):
                cut3 =LepPt>lep[k] if k==len(lep)-2 else LepPt>lep[k] and LepPt<=lep[k+1]
                idx += 1
                if (cut1 and cut2 and cut3 and cutchrg):
                    pickIdx = idx
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    return pickIdx

def findReg2BinIndex(CT, MT, LepPt):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        for i in range(len(CT_bin)-1):
            cut2 = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
            lep = TotElePt_bin if j >= len(MT_bin)-3 else TotLepPt_bin #for last two MT bins, leppT start from 5 GeV
            for k in range(len(lep)-1):
                cut3 = LepPt>lep[k] if k==len(lep)-2 else LepPt>lep[k] and LepPt<=lep[k+1]
                idx += 1
                if (cut1 and cut2 and cut3):
                    pickIdx = idx
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    return pickIdx

SRCRBinLabelList = [
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'L',
    'M',
    'H',
    'CR',
    'L',
    'M',
    'H',
    'CR',
    'L',
    'M',
    'H',
    'CR',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'L',
    'M',
    'H',
    'CR',
    'L',
    'M',
    'H',
    'CR',
    'L',
    'M',
    'H',
    'CR',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'CR'
]

def getBinlabel(CT, MT, LepPt, reg='SR'):
    ct = CTBinLabelDict[findCTBin(CT)] if findCTBin(CT)>0 else ''
    mt = MTBinLabelDict[findMTBin(MT)] if findMTBin(MT)>0 else ''
    leppt = (LepPtBinLabelDict[findLepPtBin(LepPt, MT)+1] if MT>95 else LepPtBinLabelDict[findLepPtBin(LepPt, MT)]) if findLepPtBin(LepPt, MT)>0 else ''
    return reg+leppt+mt+ct if reg=='SR' else reg+mt+ct

def getHistBinlabel(idx, nbins):
    if nbins==108:
        return SRBinLabelList[idx]
    elif nbins==24:
        return CRBinLabelList[idx]
    else:
        return SRCRBinLabelList[idx]
