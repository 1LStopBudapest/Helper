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
        self.colloc = 62 #initial location (of collision), 102=displaced, 62=prompt samples

    #GenPart = generated particle vertex
    def getGenPartStop(self):
        genStop = []
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i]==1000006 and self.tr.GenPart_status[i]==self.colloc: 
                genStop.append({'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]})
        return genStop[0] #this list always has only 1 element

    def get106(self):
        genStop = {}
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i]==1000006 and self.tr.GenPart_status[i]==106:
                genStop = {'x':self.tr.GenPart_vx[i], 'y':self.tr.GenPart_vy[i], 'z':self.tr.GenPart_vz[i]}
        return genStop

    def getGenPartAntiStop(self):
        genAStop = []
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i]==-1000006 and self.tr.GenPart_status[i]==self.colloc:
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

    def smallestDist(self, v, L, coord): #v: vector, L: list of vectors
        D = 1e5
        for l in L:
            D = min(D, abs(l[coord]-v[coord]))
        return D

    def smallestDist2D(self, v, L):
        D = 1e5
        for l in L:
            D = min(D, sqrt((v['x'] - l['x'])**2 + (v['y'] - l['y'])**2))
        return D

    def smallestDist3D(self, v, L):
        D = 1e5
        for l in L:
            D = min(D, sqrt((v['x'] - l['x'])**2 + (v['y'] - l['y'])**2 + (v['z'] - l['z'])**2))
        return D

    def distance3D(self, v, L):
        D = {}
        for l in L:
            D[sqrt((v['x'] - l['x'])**2 + (v['y'] - l['y'])**2 + (v['z'] - l['z'])**2)] = l #{distance : reference SV}
        return {k: v for k, v in sorted(D.items(), key=lambda item: item[0])} 

    def smallestUniqueDist3D(self, L, SV): #LSP, SV
        D1 = self.distance3D(L[0], SV) #S
        D2 = self.distance3D(L[1], SV) #A
        if list(D1.values())[0] != list(D2.values())[0]:
            return [list(D1.keys())[0], list(D2.keys())[0]]
        elif list(D1.values())[0] < list(D2.values())[0]:
            return [list(D1.keys())[0], list(D2.keys())[1]]
        else:
            return [list(D1.keys())[1], list(D2.keys())[0]]

    def only1SV(self, S, A, SV): #LSP from (S)top and (A)ntistop
        d1 = list(self.distance3D(S,SV).keys())[0]
        d2 = list(self.distance3D(A,SV).keys())[0]
        if d1 < d2:
            return [d1, 1e5] #[S,A]
        else:
            return [1e5, d2]

    def getStopPt(self):
        pT = -1.0
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i]==1000006 and self.tr.GenPart_status[i]==self.colloc:
                pT = self.tr.GenPart_pt[i]
        return pT

    def getLSPStopPt(self):
        pT_stop = -1.0
        pT_lsp = -1.0
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i]==1000006 and self.tr.GenPart_status[i]==self.colloc:
                pT_stop = self.tr.GenPart_pt[i]
        for i in range(self.tr.nGenPart):
            if self.tr.GenPart_pdgId[i] == 1000022 and binary_repr(self.tr.GenPart_statusFlags[i], width=15)[1] == '1': #last copy
                if abs(self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[i]]) == 1000006 or abs(self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[self.tr.GenPart_genPartIdxMother[i]]]) == 1000006:
                    pT_lsp = self.tr.GenPart_pt[i]
        return abs(pT_stop-pT_lsp)
