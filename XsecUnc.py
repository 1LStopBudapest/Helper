import os, sys
import ROOT

sys.path.append('../')
from Sample.Dir import Xfiles


BKXecUncDict = {
    'TTSingleLep_pow': (2.18/88.51),
    'TTLep_pow' : (9.00/366.29),
    'T_tch_pow': (5.4/136.02),
    'TBar_tch_pow': (4.06/80.95),
    'T_tWch_ext':  (0.9/35.85),
    'TBar_tWch_ext': (0.9/35.85),
    'WJetsToLNu_HT70to100': (1.26/1353.0),
    'WJetsToLNu_HT100to200': (1.275/1346.0),
    'WJetsToLNu_HT200to400': (0.3444/360.1),
    'WJetsToLNu_HT400to600': (0.04687/48.8),
    'WJetsToLNu_HT600to800': (0.01161/12.07),
    'WJetsToLNu_HT800to1200': (0.005288/5.497),
    'WJetsToLNu_HT1200to2500': (0.001278/1.329),
    'WJetsToLNu_HT2500toInf': (0.00003077/0.03209),
    'DYJetsToLL_M50_HT70to100': (0.5/169.9),
    'DYJetsToLL_M50_HT100to200': (0.09/147.40),
    'DYJetsToLL_M50_HT200to400': (0.04/40.99),
    'DYJetsToLL_M50_HT400to600': (0.005/5.678),
    'DYJetsToLL_M50_HT600to800': (0.001307/1.358),
    'DYJetsToLL_M50_HT800to1200': (0.0005996/0.6229),
    'DYJetsToLL_M50_HT1200to2500': (0.0001884/0.1512),
    'DYJetsToLL_M50_HT2500toInf': (0.000005548/0.003659),
    'ZJetsToNuNu_HT100to200': (0.12/280.35),
    'ZJetsToNuNu_HT200to400': (0.03/77.67),
    'ZJetsToNuNu_HT400to600': (0.01/10.73),
    'ZJetsToNuNu_HT600to800': (0.007269/2.559),
    'ZJetsToNuNu_HT800to1200': (0.00336/1.1796),
    'ZJetsToNuNu_HT1200to2500': (0.000726/0.28833),
    'ZJetsToNuNu_HT2500toInf': (0.000021/0.006945),
    'QCD_HT50to100': (218700.0/246300000.0),
    'QCD_HT100to200': (26130.0/28060000.0),
    'QCD_HT200to300': (1626.0/1710000.0),
    'QCD_HT300to500': (332.9/347500.0),
    'QCD_HT500to700': (98.03/32260.0),
    'QCD_HT700to1000': (20.88/6830.0),
    'QCD_HT1000to1500': (3.682/1207.0),
    'QCD_HT1500to2000': (0.1159/120.0),
    'QCD_HT2000toInf': (0.07681/25.16),
    'TTWToLNu': (0.0020/0.2043),
    'TTWToQQ': (0.0021/0.4062),
    'TTW_LO': (0.001268/0.4611),
    'TTZ_LO': (0.001713/0.6529),
    'TTG': (0.0013/3.697),
    'WWTo2L2Nu': (0.00704/11.09),
    'WWTo1L1Nu2Q': (0.5404/51.65),
    'WZTo1L1Nu2Q': (0.09682/9.119),
    'WZTo1L3Nu': (0.0366/3.414),
    'WZTo2L2Q': (0.05904/6.565),
    'WZTo3LNu': (0.0175/5.052),
    'ZZTo2L2Nu': (0.0009971/0.9738),
    'ZZTo2L2Q': (0.03147/3.676),
    'ZZTo2Q2Nu': (0.04731/4.545),
    'ZZTo4L': (0.00122/1.325),
    'WW': (0.1123/75.8),
}

def getXsecUnc(sample):
    return BKXecUncDict[sample] if sample in BKXecUncDict.keys() else 0.01

def getSigXsecUnc(ms):
    fname = os.path.join(Xfiles, 'StopXsecUnc.root')
    uncfile = ROOT.TFile(fname)
    hist = uncfile.Get('hUnc')
    unc = hist.GetBinContent(hist.GetXaxis().FindBin(ms))
    return unc/100.0
