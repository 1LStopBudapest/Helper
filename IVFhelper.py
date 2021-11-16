import ROOT
import math
import os, sys
from Helper.VarCalc import *
from Helper.TreeVarSel import TreeVarSel

class IVFhelper():
    
    def __init__(self, tr, isData, yr):
        self.tr = tr
        self.yr = yr
        self.isData = isData
        self.getsel = TreeVarSel(tr, isData, yr)

        self.ivfList = self.IVFSelection()
        self.hadronicList = self.HadronicSelection()
        self.cut_indices = list(set(self.ivfList).intersection(self.hadronicList)) # ==> before cut
        #self.cut_indices = list(range(self.tr.nSV)) # ==> after cut

    #IVF selection
    def IVFSelection(self):
        indexlist = []
        for i in range(self.tr.nSV):
            if self.NtracksCut(i) and self.SVdxyCut(i) and self.S2Dcut(i) and self.SVmassCut(i):
                indexlist.append(i)
        return indexlist

    #Selection in Hadronic Stop AN (On top of IVF selection)
    def HadronicSelection(self):
        indexlist = []
        for i in range(self.tr.nSV):
            if self.S3Dcut(i) and self. angleCut(i) and self.ptCut(i) and self.deltaRcut(i):
                indexlist.append(i)
        return indexlist

    #cuts
    def NtracksCut(self, i): 
        return bytearray(self.tr.SV_ntracks[i])[0] >= 3

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
        ret = True
        for j in self.getsel.selectjetIdx(20):
            if DeltaR(self.tr.SV_eta[i], self.tr.SV_phi[i], self.tr.Jet_eta[j], self.tr.Jet_phi[j]) <= 0.4:
                ret = False
        return ret


    #plotting
    def getNtracks(self):
        Nt = []
        for i in self.cut_indices:
            ntracks = bytearray(self.tr.SV_ntracks[i])[0]
            Nt.append(ntracks)
        return Nt

    def getSVdxy(self):
        dxy = []
        for i in self.cut_indices:
            dxy.append(self.tr.SV_dxy[i])
        return dxy

    def getS2D(self):
        dxySig = []
        for i in self.cut_indices:
            dxySig.append(self.tr.SV_dxySig[i])
        return dxySig

    def getSVmass(self):
        mass = []
        for i in self.cut_indices:
            mass.append(self.tr.SV_mass[i])
        return mass

    def getS3D(self):
        dlenSig = []
        for i in self.cut_indices:
            dlenSig.append(self.tr.SV_dlenSig[i])
        return dlenSig


    def getSVangle(self):
        angle = []
        for i in self.cut_indices:
            angle.append(self.tr.SV_pAngle[i])
        return angle


    def getSVpT(self):
        pT = []
        for i in self.cut_indices:
            pT.append(self.tr.SV_pt[i])
        return pT

    def getSVdR(self):
        dR = []
        for i in self.cut_indices:        
            if self.tr.nJet > 0:
                dR.append(DeltaR(self.tr.SV_eta[i], self.tr.SV_phi[i], self.tr.Jet_eta[0], self.tr.Jet_phi[0]))
        return dR
