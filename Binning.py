import ROOT
import math
import os, sys


CT_bin = [300, 400, -1]
MT_bin = [0, 60, 95, -1]
LepPt_bin = [3.5, 5, 12, 20, 30]
ElePt_bin = [5, 12, 20, 30]

EachMT_div = len(LepPt_bin)-1
EachCT_div = (len(LepPt_bin)-1) * (len(MT_bin)-1) - 1 #for last MT bin, leppT start from 5 GeV

def findBinIndex(CT, MT, LepPt):
    idx = -1
    pickIdx = -1
    for i in range(len(CT_bin)-1):
        cut1 = CT>CT_bin[i] if i == len(CT_bin)-2 else CT>CT_bin[i] and CT<=CT_bin[i+1]
        for j in range(len(MT_bin)-1):
            cut2 = MT>MT_bin[j] if j == len(MT_bin)-2 else MT>MT_bin[j] and MT<=MT_bin[j+1]
            lep = ElePt_bin if j == len(MT_bin)-2 else LepPt_bin #for last MT bin, leppT start from 5 GeV
            for k in range(len(lep)-1):
                cut3 = LepPt>lep[k] if k == len(lep)-2 else LepPt>lep[k] and LepPt<=lep[k+1]
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
    lep = ElePt_bin if MT>95 else LepPt_bin #for last MT bin, leppT start from 5 GeV
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
        
CTBinLabelDict = {
    1 : 'X',
    2 : 'Y',
    }

MTBinLabelDict = {
    1 : 'a',
    2 : 'b',
    3 : 'c',
    }

LepPtBinLabelDict = {
    1 : 'VL',
    2 : 'L',
    3 : 'M',
    4 : 'H',
    }

def getBinlabel(CT, MT, LepPt, reg='SR'):
    ct = CTBinLabelDict[findCTBin(CT)] if findCTBin(CT)>0 else ''
    mt = MTBinLabelDict[findMTBin(MT)] if findMTBin(MT)>0 else ''
    leppt = (LepPtBinLabelDict[findLepPtBin(LepPt, MT)+1] if MT>95 else LepPtBinLabelDict[findLepPtBin(LepPt, MT)]) if findLepPtBin(LepPt, MT)>0 else ''
    return reg+leppt+mt+ct if reg=='SR' else reg+mt+ct
