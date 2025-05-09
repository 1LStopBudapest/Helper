import ROOT
import math
import os, sys

sys.path.append('../')


class MCWeight():

    def __init__(self, tr, yr, sample):
        self.tr = tr
        self.yr = yr
        self.sample = sample
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
