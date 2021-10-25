import ROOT
import math
import os, sys
from Helper.VarCalc import *

class IVFhelper():
    
    def __init__(self, tr, isData, yr):
        self.tr = tr
        self.yr = yr
        self.isData = isData

    #IVF selection
    def IVFSelection(self):
        sel = False
        for i in range(self.tr.nSV):
            sel = self.NtracksCut and self.SVdxyCut(i) and self.S2Dcut(i) and self.SVmassCut(i)
            if sel:
                break
        return sel

    #Selection in Hadronic Stop AN (On top of IVF selection)
    def HadronicSelection(self):
        sel = False
        for i in range(self.tr.nSV):
            sel = self.S3Dcut(i) and self. angleCut(i) and self.ptCut(i) and self.deltaRcut(i)
            if sel:
                break
        return sel

    #cuts
    def NtracksCut(self): 
        return len(self.tr.SV_ntracks) >= 3

    def SVdxyCut(self, i):
        return self.tr.SV_dxy[i] < 2.5

    def S2Dcut(self, i):
        return self.tr.SV_dxySig[i] > 3.0

    def SVmassCut(self, i):
        return self.tr.SV_mass[i] < 6.5

    def S3Dcut(self, i):
        return self.tr.SV_dlenSig[i] > 4.0
    
    def angleCut(self, i): 
        return self.tr.SV_pAngle[i] > 0.98

    def ptCut(self, i):
        return self.tr.SV_pt[i] < 20.0 #GeV      

    def deltaRcut(self, i):
        if self.tr.nJet > 0:
            dR = DeltaR(self.tr.SV_eta[i], self.tr.SV_phi[i], self.tr.Jet_eta[0], self.tr.Jet_phi[0])
            #is comparison with jet[0] ok?
        return dR > 0.4


    #plotting
    def getSVdxy(self):
        dxy = []
        for i in range(self.tr.nSV):        
            if self.SVdxyCut(i):
                dxy.append(self.tr.SV_dxy)
        return dxy

    def getS2D(self):
        dxySig = []
        for i in range(self.tr.nSV):        
            if self.S2Dcut(i):
                dxySig.append(self.tr.SV_dxySig)
        return dxySig

    def getSVmass(self):
        mass = []
        for i in range(self.tr.nSV):        
            if self.SVmassCut(i):
                mass.append(self.tr.SV_mass)
        return mass

    def getS3D(self):
        dlenSig = []
        for i in range(self.tr.nSV):        
            if self.S3Dcut(i):
                dlenSig.append(self.tr.SV_dlenSig)
        return dlenSig


    def getSVangle(self):
        angle = []
        for i in range(self.tr.nSV):        
            if self.angleCut(i):
                angle.append(self.tr.SV_pAngle)
        return angle


    def getSVpT(self):
        pT = []
        for i in range(self.tr.nSV):        
            if self.ptCut(i):
                pT.append(self.tr.SV_pt)
        return pT

    def getSVdR(self):
        dR = []
        for i in range(self.tr.nSV):        
            if self.SVdxyCut(i) and self.tr.nJet > 0:
                dR.append(DeltaR(self.tr.SV_eta[i], self.tr.SV_phi[i], self.tr.Jet_eta[0], self.tr.Jet_phi[0]))
        return dR
