import ROOT
import math
import os, sys
import collections as coll

from Helper.VarCalc import *


class TreeVarSel():
    
    def __init__(self, tr, isData, yr):
        self.tr = tr
        self.yr = yr
        self.isData = isData

    #GenPart = generated particle vertex, len={0,1,2,...}
    def getGenPartStop(self):
        genStop = []
        for i in range(self.tr.nGenPart): 
            if self.tr.GenPart_pdgId[i]==1000006 and self.tr.GenPart_status[i]==102: #antistop==-1000006, 102==initial location (of collision)
                genStop.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return genStop

    #GenVt = generated primary vertex, len=1
    def getGenVtx(self):
        return {'x':self.tr.GenVtx_x, 'y':self.tr.GenVtx_y, 'z':self.tr.GenVtx_z}

    def tmp(self):
        for i in range(self.tr.nGenPart):
            #print  'pdgId: ', self.tr.GenPart_pdgId[i], 'status:', self.tr.GenPart_status[i], 'mother: ', self.tr.GenPart_genPartIdxMother[i]
            print  'i: ', i, 'mother: ', self.tr.GenPart_genPartIdxMother[i]

    def xDist(self, v1, v2, coord):
        return abs(v1[coord]-v2[coord])
