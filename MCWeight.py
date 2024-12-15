import ROOT
import math
import os, sys

sys.path.append('../')
from Sample.Dir import Xfiles

class MCWeight():

    def __init__(self, tr, yr, sample):
        self.tr = tr
        self.yr = yr
        self.sample = sample
        #self.EWKnorfile = os.path.join(Xfiles, 'EWKNormFactor.txt') 
        #self.TLMufile = os.path.join(Xfiles, 'h_TLratio_2D_Mu.root') 
        #self.TLElefile = os.path.join(Xfiles, 'h_TLratio_2D_Ele.root')
        self.isSignal = True if ('Stop' in self.sample or 'T2tt' in self.sample) else False

    def getPUWeight(self):
        return self.tr.reweightPU if hasattr(self.tr, 'reweightPU') else 1.0

    def getLeptonSF(self):
        return self.tr.reweightLeptonSF if hasattr(self.tr, 'reweightLeptonSF') else 1.0

    def getBTagSF(self):
        return self.tr.reweightBTag_SF if hasattr(self.tr, 'reweightBTag_SF') else 1.0

    def getISRWeight(self):
        if self.isSignal:
            return self.tr.reweight_nISR if hasattr(self.tr, 'reweight_nISR') else 1.0
        else:
            return 1.0 #self.tr.reweightnISR if hasattr(self.tr, 'reweightnISR') else 1.0

    def getWpTWeight(self):
        return self.tr.reweightwPt if hasattr(self.tr, 'reweightwPt') else 1.0

    def getL1PrefireWeight(self):
        return self.tr.reweightL1Prefire if hasattr(self.tr, 'reweightL1Prefire') else 1.0

    
    def getHEMWeight(self):
        return self.tr.reweightHEM if hasattr(self.tr, 'reweightHEM') else 1.0
    
    def getTotalWeight(self):
        return self.getPUWeight() * self.getLeptonSF() * self.getBTagSF() * self.getWpTWeight() * self.getL1PrefireWeight() * self.getHEMWeight()
        #return self.getLeptonSF() * self.getBTagSF() * self.getISRWeight() * self.getWpTWeight() * self.getL1PrefireWeight()

    '''
    def getEWKNorm(self):
        f = open(self.EWKnorfile, 'r')
        s = f.read()#just one value
        return s
    '''
    def getTLvalue(self, lep , leppt , lepeta):
        pt_Binning = [3.5, 5.0, 8, 10, 15, 20, 30, 50]
        eta_Binning = [0.,1.442,1.566,3.142] 
        f = ROOT.TFile.Open("/home/mmoussa/susy/susy_code_fake_rate/AuxFiles/h_TLratio_2D_"+lep+".root")
        hist_TL_values = f.Get("h_TLratio_2D")
        value = 0.0
        for i in range(len(pt_Binning)-1):
            if abs(lepeta)>=eta_Binning[0] and abs(lepeta)<=eta_Binning[1]:
                if leppt >= pt_Binning[i] and leppt < pt_Binning[i+1]:
                    value = hist_TL_values.GetBinContent(i+1 , 1)
            if abs(lepeta)>=eta_Binning[2] and abs(lepeta)<=eta_Binning[3]:
                if leppt >= pt_Binning[i] and leppt < pt_Binning[i+1]:
                    value = hist_TL_values.GetBinContent(i+1 , 3)
        return value 
 







        
