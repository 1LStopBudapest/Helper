import ROOT
import math
import os, sys

CT_bin = [300, 400, -1]
MT_bin = [0, 60, 95, 130, -1]
LepPt_bin = [3, 5, 12, 20, 30, 50]
ElePt_bin = [5, 12, 20, 30, 50]

EachMT_div = len(LepPt_bin)-1


def findSR1BinIndexVal1(MT, LepPt, LepChrg):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        cutchrg = LepChrg==-1 if j < len(MT_bin)-3 else True # -1 charge only for first two MT bins
        lep = ElePt_bin if j >= len(MT_bin)-3 else LepPt_bin #for last two MT bin, leppT start from 5 GeV
        for k in range(len(lep)-1):
            cut3 = LepPt>lep[k] and LepPt<=lep[k+1]
            idx += 1
            if (cut1 and cut3 and cutchrg):
                pickIdx = idx
                break
        else:
            continue
        break
        
    return pickIdx

def findSR2BinIndexVal1(MT, LepPt):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        lep = ElePt_bin if j >= len(MT_bin)-3 else LepPt_bin #for last two MT bins, leppT start from 5 GeV
        for k in range(len(lep)-1):
            cut3 = LepPt>lep[k] and LepPt<=lep[k+1]
            idx += 1
            if (cut1 and cut3):
                pickIdx = idx
                break
        else:
            continue
        break
            
    return pickIdx

def findCR1BinIndexVal1(MT, LepChrg):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        cutchrg = LepChrg==-1 if j < len(MT_bin)-3 else True # -1 charge only for first two MT bins
        idx += 1
        if (cut1 and LepChrg):
            pickIdx = idx
            break
                            
    return pickIdx

def findCR2BinIndexVal1( MT):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        idx += 1
        if cut1:
            pickIdx = idx
            break
                   
    return pickIdx


def findSR1BinIndexVal2(CT, MT, LepChrg):
    idx = -1
    pickIdx = -1
    for j in range(len(MT_bin)-1):
        cut1 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
        cutchrg = LepChrg==-1 if j < len(MT_bin)-3 else True # -1 charge only for first two MT bins
        for i in range(len(CT_bin)-1):
            cut2 = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
            idx += 1
            if (cut1 and cut2 and cutchrg):
                pickIdx = idx
                break
        else:
            continue
        break
        
    return pickIdx
                      
def findSR2BinIndexVal2(CT, MT):
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

def findCR1BinIndexVal2(CT, MT, LepChrg):
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
                                                                                            
def findCR2BinIndexVal2(CT, MT):
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
    5 : 'VH',
    }

SRBinLabelListVal1 = [
    'SR1VLa',
    'SR1La',
    'SR1Ma',
    'SR1Ha',
    'SR1VHa',
    'SR1VLb',
    'SR1Lb',
    'SR1Mb',
    'SR1Hb',
    'SR1VHb',
    'SR1Lc',
    'SR1Mc',
    'SR1Hc',
    'SR1VHc',
    'SR1Ld',
    'SR1Md',
    'SR1Hd',
    'SR1VHd',
    'SR2VLa',
    'SR2La',
    'SR2Ma',
    'SR2Ha',
    'SR2VHa',
    'SR2VLb',
    'SR2Lb',
    'SR2Mb',
    'SR2Hb',
    'SR2VHb',
    'SR2Lc',
    'SR2Mc',
    'SR2Hc',
    'SR2VHc',
    'SR2Ld',
    'SR2Md',
    'SR2Hd',
    'SR2VHd',
    'SR3VLa',
    'SR3La',
    'SR3Ma',
    'SR3Ha',
    'SR3VHa',
    'SR3VLb',
    'SR3Lb',
    'SR3Mb',
    'SR3Hb',
    'SR3VHb',
    'SR3Lc',
    'SR3Mc',
    'SR3Hc',
    'SR3VHc',
    'SR3Ld',
    'SR3Md',
    'SR3Hd',
    'SR3VHd',
    ]

CRBinLabelListVal1 = [
    'CR1a',
    'CR1b',
    'CR1c',
    'CR1d',
    'CR2a',
    'CR2b',
    'CR2c',
    'CR2d',
    'CR3a',
    'CR3b',
    'CR3c',
    'CR3d',
    ]

SRBinLabelListVal2 = [
    'SR1aX',
    'SR1aY',
    'SR1bX',
    'SR1bY',
    'SR1cX',
    'SR1cY',
    'SR1dX',
    'SR1dY',
    'SR2aX',
    'SR2aY',
    'SR2bX',
    'SR2bY',
    'SR2cX',
    'SR2cY',
    'SR2dX',
    'SR2dY',
    'SR3aX',
    'SR3aY',
    'SR3bX',
    'SR3bY',
    'SR3cX',
    'SR3cY',
    'SR3dX',
    'SR3dY'
    ]

CRBinLabelListVal2 = [
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
    'CR3dY'
    ]


SRCRBinLabelListVal1 = [
    'VL',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'VL',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'L',
    'M',
    'H',
    'VH',
    'CR',
    'L',
    'M',
    'H',
    'VH',
    'CR'
    ]


def getHistBinlabel(idx, nbins):
    if nbins==54:
        return SRBinLabelList[idx]
    elif nbins==12:
        return CRBinLabelList[idx]
    else:
        return SRCRBinLabelList[idx]
