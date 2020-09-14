import ROOT
import math
import os, sys

class MCWeight():

    def __init__(self, tr, yr):
        self.tr = tr
        self.yr = yr



    def getPUWeight(self):
        return self.tr.reweightPU if hasattr(self.tr, 'reweightPU') else 1.0

    def getLeptonSF(self):
        return self.tr.reweightLeptonSF if hasattr(self.tr, 'reweightLeptonSF') else 1.0

    def getBTagSF(self):
        return self.tr.reweightBTag_SF if hasattr(self.tr, 'reweightBTag_SF') else 1.0

    def getISRWeight(self):
        return self.tr.reweightnISR if hasattr(self.tr, 'reweightnISR') else 1.0

    def getWpTWeight(self):
        return self.tr.reweightwPt if hasattr(self.tr, 'reweightwPt') else 1.0

    def getTotalWeight(self):
        return self.getPUWeight() * self.getLeptonSF() * self.getBTagSF() * self.getISRWeight() * self.getWpTWeight()
