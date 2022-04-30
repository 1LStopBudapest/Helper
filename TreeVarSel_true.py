import ROOT
import math
import os, sys
import collections as coll

from Helper.VarCalc import *


class TreeVarSel():

    def __init__(self, tr, yr):
        self.tr = tr
        self.yr = yr

    #GenPart = generated particle vertex
    def getGenPartStop(self):
        genStop = []
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i]==1000006 and self.tr.GenPart_status[i]==102: # 102==initial location (of collision)
                genStop.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return genStop[0] #this list always has only 1 element

    def getGenPartAntiStop(self):
        genAStop = []
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i]==-1000006 and self.tr.GenPart_status[i]==102:
                genAStop.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return genAStop[0] #this list always has only 1 element

    #GenVt = generated primary vertex
    def getGenVtx(self):
        return {'x':self.tr.GenVtx_x, 'y':self.tr.GenVtx_y, 'z':self.tr.GenVtx_z}

    def getLSP(self):
        L = []
        for i in range(self.tr.nGenPart):
            if abs(self.tr.GenPart_pdgId[i]) == 1000022: # \tilde{chi}_1^0 == 1000022
                L.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return L #always 2 elements

    def getPV(self):
        return {'x':self.tr.PV_x, 'y':self.tr.PV_y, 'z':self.tr.PV_z}

    def getSV(self):
        L = []
        for i in range(self.tr.nSV):
            L.append({'x':self.tr.SV_x[i], 'y':self.tr.SV_y[i], 'z':self.tr.SV_z[i]})
        return L

    def distance(self, v1, v2, coord):
        return abs(v1[coord]-v2[coord])

    def listDist(self, L1, L2, coord):
        D = []
        for l1 in L1:
            for l2 in L2:
                D.append(abs(l1[coord]-l2[coord]))
        return D
