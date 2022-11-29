import ROOT
import math
import os, sys

from Helper.VarCalc import eleVID

class ANEle():

    def __init__(self, tr, objtype, pref):
        self.tr = tr
        self.objtype = objtype #its a string: 'Std' for standard PF ele, 'LowPt' for low pT ele and 'comb' for combination of both satrting from low pT ele
        self.pref = pref # pref is string which defines the preference between standard and low pT ele while using the 'comb' objtype


    def getTheType(self):
        return "type"# need to fix
    
    def getANEleIdx(self):
        if self.objtype=='comb':
            return self.CombEleIdx(self.pref)
        elif self.objtype=='Std':
            return self.StdselectEleIdx()
        else:
            return self.LowselectEleIdx()

    def getANEleVar(self):
        if self.objtype=='comb':
            return self.getCombEleVar(self.CombEleIdx())
        elif self.objtype=='Std':
            return self.getStdEleVar(self.StdselectEleIdx())
        else:
            return self.getLowPtEleVar(self.LowselectEleIdx())
        
    def getCombEleVar(self, eId):
        Llist = []
        for id, tp in eId:
            if tp =='LowPtElectron':
                Llist.append({'pt':self.tr.LowPtElectron_pt[id], 'eta':self.tr.LowPtElectron_eta[id], 'deltaEtaSC':self.tr.LowPtElectron_deltaEtaSC[id], 'phi':self.tr.LowPtElectron_phi[id], 'dxy':self.tr.LowPtElectron_dxy[id], 'dz': self.tr.LowPtElectron_dz[id], 'charg':self.tr.LowPtElectron_charge[id]})
            else:
                Llist.append({'pt':self.tr.Electron_pt[id], 'eta':self.tr.Electron_eta[id], 'deltaEtaSC':self.tr.Electron_deltaEtaSC[id], 'phi':self.tr.Electron_phi[id], 'dxy':self.tr.Electron_dxy[id], 'dz': self.tr.Electron_dz[id], 'charg':self.tr.Electron_charge[id]})
        return Llist

    def CombEleIdx(self, pref):
        idx = {}
        if pref=='Standard':
            for id in self.StdselectEleIdx():
                idx[id] = 'Electron'
            if not idx:
                for id in self.LowselectEleIdx():
                    idx[id] = 'LowPtElectron'
        else:
            for id in self.LowselectEleIdx():
                idx[id] = 'LowPtElectron'
            if not idx:
                for id in self.StdselectEleIdx():
                    idx[id] = 'Electron'
        return idx

    def getLowPtEleVar(self, eId):
        Llist = []
        for id in eId:
            Llist.append({'pt':self.tr.LowPtElectron_pt[id], 'eta':self.tr.LowPtElectron_eta[id], 'deltaEtaSC':self.tr.LowPtElectron_deltaEtaSC[id], 'phi':self.tr.LowPtElectron_phi[id], 'dxy':self.tr.LowPtElectron_dxy[id], 'dz': self.tr.LowPtElectron_dz[id], 'charg':self.tr.LowPtElectron_charge[id]})
        return Llist

        def getStdEleVar(self, eId):
            Llist = []
            for id in eId:
                Llist.append({'pt':self.tr.Electron_pt[id], 'eta':self.tr.Electron_eta[id], 'deltaEtaSC':self.tr.Electron_deltaEtaSC[id], 'phi':self.tr.Electron_phi[id], 'dxy':self.tr.Electron_dxy[id], 'dz': self.tr.Electron_dz[id], 'charg':self.tr.Electron_charge[id]})
            return Llist

    def LowselectEleIdx(self):
            idx = {}
            for i in range(len(self.tr.LowPtElectron_pt)):
                if self.LoweleSelector(pt=self.tr.LowPtElectron_pt[i], eta=self.tr.LowPtElectron_eta[i], deltaEtaSC=self.tr.LowPtElectron_deltaEtaSC[i], iso=self.tr.LowPtElectron_miniPFRelIso_all[i], dxy=self.tr.LowPtElectron_dxy[i], dz=self.tr.LowPtElectron_dz[i], Id=self.tr.LowPtElectron_ID[i],lepton_selection='HybridIso'):
                    idx[i]='LowPtElectron'
            return idx

    def StdselectEleIdx(self):
            idx = []
            for i in range(len(self.tr.Electron_pt)):
                if self.StdeleSelector(pt=self.tr.Electron_pt[i], eta=self.tr.Electron_eta[i], deltaEtaSC=self.tr.Electron_deltaEtaSC[i], iso=self.tr.Electron_pfRelIso03_all[i], dxy=self.tr.Electron_dxy[i], dz=self.tr.Electron_dz[i], Id=self.tr.Electron_vidNestedWPBitmap[i],lepton_selection='HybridIso'):
                    idx[i]='Electron'
            return idx



    def LoweleSelector(self, pt, eta, deltaEtaSC, iso, dxy, dz, Id, lepton_selection='HybridIso', isolationType='mini'):
        isolationWeight = 1.0
        if(isolationType == 'mini'):
            # below 50 GeV, 0.2 cone size
            # 50 < pt < 200: cone size = 10 / pt(lepton)
            # pt > 200: 0.05 cone size
            # calculated by weighting with cone area, from different cone sizes (0.3 -> 0.2)
            if(pt < 50):
                isolationWeight = 0.42942652
            elif( pt < 200):
                isolationWeight = math.tan(10.0 / pt)**2 / math.tan(0.3)**2
            else:
                isolationWeight = 0.02616993
                
        if lepton_selection == 'HybridIso':
            def func():
                if pt <= 25 and pt >5:
                    return \
                        abs(eta)       < 2.5 \
                        and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                        and (iso* pt) < 5.0 * isolationWeight \
                        and abs(dxy)       < 0.02 \
                        and abs(dz)        < 0.1 \
                        and Id > 0 #BDT score larger than 0
                elif pt > 25:
                    return \
                        abs(eta)       < 2.5 \
                        and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                        and iso < 0.2 * isolationWeight \
                        and abs(dxy)       < 0.02 \
                        and abs(dz)        < 0.1 \
                        and Id > 0
        elif lepton_selection == 'looseHybridIso':
            def func():
                if pt <= 25 and pt >5:
                    return \
                        abs(eta)       < 2.5 \
                        and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                        and (iso*pt) < 20.0 * isolationWeight \
                        and abs(dxy)       < 0.1 \
                        and abs(dz)        < 0.5 \
                        and Id > 0
                elif pt > 25:
                    return \
                        abs(eta)       < 2.5 \
                        and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                        and iso < 0.8 * isolationWeight \
                        and abs(dxy)       < 0.1 \
                        and abs(dz)        < 0.5 \
                        and Id > 0
                
                    
        else:
            def func():
                return \
                    pt >5 \
                    and abs(eta)       < 2.5 \
                    and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                    and Id > 0
        return func()
                
    def StdeleSelector(self, pt, eta, deltaEtaSC, iso, dxy, dz, Id, lepton_selection='HybridIso', isolationType='standard'):
        isolationWeight = 1.0
        if(isolationType == 'mini'):
            # below 50 GeV, 0.2 cone size
            # calculated by weighting with cone area, from different cone sizes (0.3 -> 0.2)
            if(pt < 50):
                isolationWeight = 0.42942652
                
        if lepton_selection == 'HybridIso':
            def func():
                if pt <= 25 and pt >5:
                    return \
                        abs(eta)       < 2.5 \
                        and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                        and (iso* pt) < 5.0 * isolationWeight \
                        and abs(dxy)       < 0.02 \
                        and abs(dz)        < 0.1 \
                        and eleVID(Id, 1, removedCuts=['pfRelIso03_all']) #cutbased id: 0:fail, 1:veto, 2:loose, 3:medium, 4:tight
                elif pt > 25:
                    return \
                        abs(eta)       < 2.5 \
                        and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                        and iso < 0.2 * isolationWeight \
                        and abs(dxy)       < 0.02 \
                        and abs(dz)        < 0.1 \
                        and eleVID(Id, 1, removedCuts=['pfRelIso03_all'])
                                                                                                                        
        elif lepton_selection == 'looseHybridIso':
            def func():
                if pt <= 25 and pt >5:
                    return \
                        abs(eta)       < 2.5 \
                        and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                        and (iso*pt) < 20.0 * isolationWeight \
                        and abs(dxy)       < 0.1 \
                        and abs(dz)        < 0.5 \
                        and eleVID(Id,1,removedCuts=['pfRelIso03_all'])
                elif pt > 25:
                    return \
                        abs(eta)       < 2.5 \
                        and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                        and iso < 0.8 * isolationWeight \
                        and abs(dxy)       < 0.1 \
                        and abs(dz)        < 0.5 \
                        and eleVID(Id,1,removedCuts=['pfRelIso03_all'])
                
                    
        else:
            def func():
                return \
                    pt >5 \
                    and abs(eta)       < 2.5 \
                    and (abs(eta+deltaEtaSC)<1.4442 or abs(eta+deltaEtaSC)>1.566) \
                    and eleVID(Id,1)
        return func()
