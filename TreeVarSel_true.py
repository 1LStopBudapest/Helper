import ROOT
import math
import os, sys
import collections as coll

from Helper.VarCalc import *


class TreeVarSel():
    
    def __init__(self, tr, yr):
        self.tr = tr
        self.yr = yr

    #GenPart = generated particle vertex, len={0,1,2,...}
    def getGenPartStop(self):
        genStop = []
        for i in range(self.tr.nGenPart): 
            if self.tr.GenPart_pdgId[i]==1000006 and self.tr.GenPart_status[i]==102: # 102==initial location (of collision)
                genStop.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return genStop

    def getGenPartAntiStop(self):
        genAStop = []
        for i in range(self.tr.nGenPart): 
            if self.tr.GenPart_pdgId[i]==-1000006 and self.tr.GenPart_status[i]==102:
                genAStop.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return genAStop

    #GenVt = generated primary vertex, len=1
    def getGenVtx(self):
        return {'x':self.tr.GenVtx_x, 'y':self.tr.GenVtx_y, 'z':self.tr.GenVtx_z}

    # Calculate the difference between stop GenPart_vx - LSP GenPart_vx, similarly for y, z --> this gives the stop decay length
    # \tilde{chi}_1^0 == 1000022
    def getLSP(self):
        L = []
        for i in range(self.tr.nGenPart):
            if abs(self.tr.GenPart_pdgId[i]) == 1000022:
                #print 'i: ', i, 'mother: ', self.tr.GenPart_genPartIdxMother[i], 'status: ', self.tr.GenPart_status[i], 'ID: ', self.tr.GenPart_pdgId[i]
                L.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return L

    def getPV(self):
        return {'x':self.tr.PV_x, 'y':self.tr.PV_y, 'z':self.tr.PV_z}

    def distance(self, v1, v2, coord):
        return abs(v1[coord]-v2[coord])
