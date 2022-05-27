import ROOT
import math
import os, sys
import collections as coll
from numpy import binary_repr

from Helper.VarCalc import *


class TreeVarSel_true():

    def __init__(self, tr, yr):
        self.tr = tr
        self.yr = yr

    #GenPart = generated particle vertex
    def getGenPartStop(self):
        genStop = []
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i]==1000006 and self.tr.GenPart_status[i]==102: # 102==initial location (of collision), 62 == in case of prompt samples
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

    def kiir(self):
        L = []
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_genPartIdxMother[i] != -1:
                print '\nIdx: %.2d, pdgId: %d \nIdxMother: %.2d, pdgIdMother: %d' % (i, self.tr.GenPart_pdgId[i], self.tr.GenPart_genPartIdxMother[i], self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[i]])
            else:
	            print '\nIdx: %.2d, pdgId: %d \nIdxMother: %d, pdgIdMother: NaN' % (i, self.tr.GenPart_pdgId[i], self.tr.GenPart_genPartIdxMother[i])
            print "Status: %d, StatusFlags: %s" % (self.tr.GenPart_status[i], binary_repr(self.tr.GenPart_statusFlags[i], width=15))
            print "Position: (%.4f, %.4f, %.4f)" % (self.tr.GenPart_vx[i], self.tr.GenPart_vy[i], self.tr.GenPart_vz[i])
        return L #always 2 elements

    def getLSP_S(self): #from stop
        L = {}
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i] == 1000022 and binary_repr(self.tr.GenPart_statusFlags[i], width=15)[1] == '1': #last copy
                if self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[i]] == 1000006:
                    L = {'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]}
                elif self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[self.tr.GenPart_genPartIdxMother[i]]] == 1000006: #grandmother is stop
                    L = {'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]}
        return L 

    def getLSP_A(self): #from antistop
        L = {}
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i] == 1000022 and binary_repr(self.tr.GenPart_statusFlags[i], width=15)[1] == '1': #last copy
                if self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[i]] == -1000006:
                    L = {'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]}
                elif self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[self.tr.GenPart_genPartIdxMother[i]]] == -1000006: #grandmother is antistop
                    L = {'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]}
        return L

    def getPV(self):
        return {'x':self.tr.PV_x, 'y':self.tr.PV_y, 'z':self.tr.PV_z}

    #deprecated
    def getSV(self):
        L = []
        for i in self.selectSoftBIdx():
            L.append({'x':self.tr.SV_x[i], 'y':self.tr.SV_y[i], 'z':self.tr.SV_z[i]})
        return L

    def getB(self):
        L = []
        for i in range(self.tr.nGenPart):
            if abs(self.tr.GenPart_pdgId[i]) == 5 and self.tr.GenPart_genPartIdxMother[i] >=0 and self.tr.GenPart_genPartIdxMother[i]<self.tr.nGenPart:
                if abs(self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[i]])==1000006:
                    L.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return L

    def getB_S(self):
        L = {}
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i] == 5 and binary_repr(self.tr.GenPart_statusFlags[i], width=15)[1] == '1' and self.tr.GenPart_genPartIdxMother[i] > 0:
                    L = {'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]}
        return L #L is not always unique!

    def getB_A(self):
        L = {}
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i] == -5 and binary_repr(self.tr.GenPart_statusFlags[i], width=15)[1] == '1' and self.tr.GenPart_genPartIdxMother[i] > 0:
                    L = {'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]}
        return L

    def distance(self, v1, v2, coord):
        return abs(v1[coord]-v2[coord])

    def listDist(self, L1, L2, coord):
        D = []
        for l1 in L1:
            for l2 in L2:
                D.append(abs(l1[coord]-l2[coord]))
        return D

    def smallestDist(self, v, L, coord):
        D = 1e5
        for l in L:
            D = min(D, abs(l[coord]-v[coord]))
        return D
