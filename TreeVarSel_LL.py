from traceback import print_tb
import ROOT
import math
import os, sys
import collections as coll

from Helper.VarCalc import *
from ANEle_LL import ANEle

class TreeVarSel():
    
    def __init__(self, tr, isData, yr, eletype='comb', elepref='Std'):
        self.tr = tr
        self.yr = yr
        self.isData = isData
        self.eletype = eletype
        self.elepref = elepref
        
    #selection
    def PreSelection(self):
        ps = self.METcut() and self.HTcut() and self.ISRcut() and self.lepcut() and self.dphicut() and self.XtralepVeto() and self.XtraJetVeto() and self.tauVeto()
        return ps

    def SearchRegion(self):
        if not self.PreSelection():
            return False
        else:
            lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
            if len(lepvar) >= 1 and lepvar[0]['pt']<=30 and self.tr.MET_pt > 300:
                return True
            else:
                return False

    def SR1(self):
        if not self.SearchRegion():
            return False
        else:
            return True if self.cntBtagjet(pt=20)==0 and self.cntBtagjet(pt=60)==0 and self.calHT()>400 and self.calCT(1)>300 and abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['eta']) < 1.5 else False

    def SR2(self):
        if not self.SearchRegion():
            return False
        else:
            return True if self.cntBtagjet(pt=20)>=1 and self.cntBtagjet(pt=60)==0 and len(self.selectjetIdx(325))>0 and self.calCT(2)>300  else False

    def ControlRegion(self):
        if not self.PreSelection():
            return False
        else:
            lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
            if len(lepvar) > 1 and lepvar[0]['pt']>30:
                return True
            else:
                return False

    def CR1(self):
        if not self.ControlRegion():
            return False
        else:
            return True if self.cntBtagjet(pt=20)==0 and self.cntBtagjet(pt=60)==0 and self.calHT()>400 and self.calCT(1)>300 and abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['eta']) < 1.5 else False

    def CR2(self):
        if not self.ControlRegion():
            return False
        else:
            return True if self.cntBtagjet(pt=20)>=1 and self.cntBtagjet(pt=60)==0 and len(self.selectjetIdx(325))>0 and self.calCT(2)>300  else False

    def Dxy1(self):
        if not self.PreSelection():
            return False
        else:
            return True if abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['dxy']) <= 0.02 else False

    def Dxy2(self):
        if not self.PreSelection():
            return False
        else:
            return True if abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['dxy']) > 0.02 and abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['dxy']) <= 1.0 else False

    def Dxy3(self):
        if not self.PreSelection():
            return False
        else:
            return True if abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['dxy']) > 1.0 else False

    #cuts
    def ISRcut(self, thr=100):
        return len(self.selectjetIdx(thr)) > 0

    def METcut(self, thr=200):
        cut = False
        if self.tr.MET_pt > thr:
            cut = True
        return cut
        
    def HTcut(self, thr=300):
        cut = False
        HT = self.calHT()
        if HT > thr:
            cut = True
        return cut
    '''
    def dphicut(self, thr=20):#old cut
        cut = True
        if len(self.selectjetIdx(thr)) >=2 and self.tr.Jet_pt[self.selectjetIdx(thr)[0]]> 100 and self.tr.Jet_pt[self.selectjetIdx(thr)[1]]> 60:
            if DeltaPhi(self.tr.Jet_phi[self.selectjetIdx(thr)[0]], self.tr.Jet_phi[self.selectjetIdx(thr)[1]]) > 2.5:
                cut = False
        return cut
    '''
    def dphicut(self, thr=20):
        cut = True
        if len(self.selectjetIdx(thr)) >=2 and self.tr.Jet_pt[self.selectjetIdx(thr)[0]]> 100 and self.tr.Jet_pt[self.selectjetIdx(thr)[1]]> 60:
            Adphi = min( DeltaPhi(self.tr.Jet_phi[self.selectjetIdx(thr)[0]], self.tr.MET_phi), DeltaPhi(self.tr.Jet_phi[self.selectjetIdx(thr)[1]], self.tr.MET_phi))
        elif len(self.selectjetIdx(thr)) >= 1 and self.tr.Jet_pt[self.selectjetIdx(thr)[0]]> 100:
            Adphi = DeltaPhi(self.tr.Jet_phi[self.selectjetIdx(thr)[0]], self.tr.MET_phi)
        else:
            Adphi = -999
            
        if Adphi < 0.5:
            cut = False
        return cut
                                                                    
                        
    def lepcut(self):
        return len(self.getLepVar(self.selectMuIdx())) >= 1
    
    def SingleElecut(self):
        return self.cntEle()>=1 and self.cntMuon()==0

    def SingleMuoncut(self):
        return self.cntMuon()>=1 and self.cntEle()==0
    
    def XtralepVeto(self):
        cut = True
        lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
        if len(lepvar) > 1 and lepvar[1]['pt']>20:
            cut = False
        return cut

    def XtraJetVeto(self, thrJet=20, thrExtra=60):
        cut = True
        if len(self.selectjetIdx(thrJet)) >= 3 and self.tr.Jet_pt[self.selectjetIdx(thrJet)[2]] > thrExtra:
            cut = False
        return cut

    def tauVeto(self):
        cut = True
        if self.tr.nGoodTaus >= 1: #only applicable to postprocessed sample where lepton(e,mu)-cleaned (dR<0.4) tau collection is stored, https://github.com/HephyAnalysisSW/StopsCompressed/blob/master/Tools/python/objectSelection.py#L303-L316
            cut = False 
        return cut
            
    def getLepMT(self):
        lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
        return MT(lepvar[0]['pt'], lepvar[0]['phi'], self.tr.MET_pt, self.tr.MET_phi) if len(lepvar) else 0

    def calCT(self, i):
        return CT1(self.tr.MET_pt, self.calHT()) if i==1 else CT2(self.tr.MET_pt, self.getISRPt())
        
    def calHT(self):
        HT = 0
        for i in self.selectjetIdx(20):
            HT = HT + self.tr.Jet_pt[i]
        return HT

    def calNj(self, thrsld=20):
        return len(self.selectjetIdx(thrsld))
        
    def getISRPt(self):
        return self.tr.Jet_pt[self.selectjetIdx(100)[0]] if len(self.selectjetIdx(100)) else 0
    
    def cntBtagjet(self, discOpt='DeepCSV', pt=20):
        return len(self.selectBjetIdx(discOpt, pt))

    
    def cntMuon(self):
        return len(self.selectMuIdx())

    def	cntEle(self):
    	return len(self.selectEleIdx())
    
    def selectjetIdx(self, thrsld):
        lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
        idx = []
        d = {}
        for j in range(len(self.tr.Jet_pt)):
            clean = False
            if self.tr.Jet_pt[j] > thrsld and abs(self.tr.Jet_eta[j]) < 2.4 and self.tr.Jet_jetId[j] > 0:
                clean = True
                for l in range(len(lepvar)):
                    dR = DeltaR(lepvar[l]['eta'], lepvar[l]['phi'], self.tr.Jet_eta[j], self.tr.Jet_phi[j])
                    ptRatio = float(self.tr.Jet_pt[j])/float(lepvar[l]['pt'])
                    if dR < 0.4 and ptRatio < 2:
                        clean = False
                        break
                if clean:
                    d[j] = self.tr.Jet_pt[j]
        od = coll.OrderedDict(sorted(d.items(), key=lambda x:x[1], reverse=True))
        for i in od:
            idx.append(i)
        return idx

    def selectBjetIdx(self, discOpt='DeepCSV', ptthrsld=20):
        idx = []
        for i in self.selectjetIdx(ptthrsld):
            if (self.isBtagCSVv2(self.tr.Jet_btagCSVV2[i], self.yr) if discOpt == 'CSVV2' else self.isBtagDeepCSV(self.tr.Jet_btagDeepB[i], self.yr)):
                idx.append(i)
        return idx


    def	selectEleIdx(self):
	return ANEle(self.tr, self.eletype, self.elepref).getANEleIdx() #return a list of tuple where tuple contain index and collection type

    def selectMuIdx(self, lepsel='HybridIso'):
        idx = []
        for i in range(len(self.tr.Muon_pt)):
            if self.muonSelector(pt=self.tr.Muon_pt[i], eta=self.tr.Muon_eta[i], iso=self.tr.Muon_miniPFRelIso_all[i], dxy=self.tr.Muon_dxy[i], dz=self.tr.Muon_dz[i], Id=self.tr.Muon_looseId[i], lepton_selection=lepsel):
                idx.append(i)
        return idx
    
    def getMuVar(self, muId):
        Llist = []
        for id in muId:
            Llist.append({'pt':self.tr.Muon_pt[id], 'eta':self.tr.Muon_eta[id], 'phi':self.tr.Muon_phi[id], 'dxy':self.tr.Muon_dxy[id], 'dxyErr':self.tr.Muon_dxyErr[id], 'dz': self.tr.Muon_dz[id], 'charg':self.tr.Muon_charge[id], 'type':'mu'})
        return Llist

    def getEleVar(self):
        return ANEle(self.tr, self.eletype, self.elepref).getANEleVar()
    
    def getLepVar(self, muId):
        Llist = []
        for id in muId:
            Llist.append({'pt':self.tr.Muon_pt[id], 'eta':self.tr.Muon_eta[id], 'phi':self.tr.Muon_phi[id], 'dxy':self.tr.Muon_dxy[id], 'dxyErr':self.tr.Muon_dxyErr[id], 'dz': self.tr.Muon_dz[id], 'charg':self.tr.Muon_charge[id], 'type':'mu'})
        Llist.extend(ANEle(self.tr, self.eletype, self.elepref).getANEleVar())
        return Llist

    def getSortedLepVar(self):
        lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
        return lepvar

    def getLepZero(self):
        L = self.getLepVar(self.selectMuIdx())
        L2 = []
        for l in range(len(L)):
            L2.append(L[l]['pt'])
        L2.sort(reverse = True)
        return L2[0]

    def isBtagDeepCSV(self, jetb, year):
        if year == '2016PreVFP' or year == '2016PostVFP' or year == '2016':
            return jetb > 0.6321
        elif year == '2017':
            return jetb > 0.4941
        elif year == '2018':
            return jetb > 0.4184
        else:
            return True

    def isBtagCSVv2(self, jetb, year):
        if year == '2016PreVFP' or year == '2016PostVFP' or year == '2016':
            return jetb > 0.8484
        elif year == '2017' or year == '2018':
            return jetb > 0.8838
        else:
            return True
        

    def muonSelector( self, pt, eta, iso, dxy, dz, Id, lepton_selection='HybridIso'):
        if lepton_selection == 'HybridIso':
            def func():
                if pt <= 12 and pt >3: #new transition point 12 GeV
                    return \
                        abs(eta)       < 2.4 \
                        and (iso* pt) < 2.4 \
                        and Id
                elif pt > 12:
                    return \
                        abs(eta)       < 2.4 \
                        and iso < 0.2 \
                        and Id
            
        elif lepton_selection == 'looseHybridIso':
            def func():
                if pt <= 12 and pt >3:
                    return \
                        abs(eta)       < 2.4 \
                        and (iso*pt) < 20.0 \
                        and Id
                elif pt > 12:
                    return \
                        abs(eta)       < 2.4 \
                        and iso < 0.8 \
                        and Id
        else:
            def func():
                return \
                    pt >3 \
                    and abs(eta)       < 2.4 \
                    and Id
        return func()



    def genEle(self):
        L = []
        for i in range(self.tr.nGenPart):
            if abs(self.tr.GenPart_pdgId[i]) ==11 and GenFlagString(self.tr.GenPart_statusFlags[i])[-1]=='1' and GenFlagString(self.tr.GenPart_statusFlags[i])[6]=='1' and self.tr.GenPart_status[i]==1 and self.tr.GenPart_genPartIdxMother[i] != -1:
                if abs(self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[i]])!=21:
                    L.append({'pt':self.tr.GenPart_pt[i], 'eta':self.tr.GenPart_eta[i], 'phi':self.tr.GenPart_phi[i]})
        return L

    def genMuon(self):
        L = []
        for i in range(self.tr.nGenPart):
            if abs(self.tr.GenPart_pdgId[i]) ==13 and GenFlagString(self.tr.GenPart_statusFlags[i])[-1]=='1' and GenFlagString(self.tr.GenPart_statusFlags[i])[6]=='1' and self.tr.GenPart_status[i]==1 and self.tr.GenPart_genPartIdxMother[i] != -1:
                if abs(self.tr.GenPart_pdgId[self.tr.GenPart_genPartIdxMother[i]])!=22:
                    L.append({'pt':self.tr.GenPart_pt[i], 'eta':self.tr.GenPart_eta[i], 'phi':self.tr.GenPart_phi[i]})
        return L


    def passFilters(self):
        return (self.tr.Flag_goodVertices if hasattr(self.tr, 'Flag_goodVertices') else True) and (self.tr.Flag_globalSuperTightHalo2016Filter if hasattr(self.tr, 'Flag_globalSuperTightHalo2016Filter') else True) and (self.tr.Flag_HBHENoiseIsoFilter if hasattr(self.tr, 'Flag_HBHENoiseIsoFilter') else True) and (self.tr.Flag_HBHENoiseFilter if hasattr(self.tr, 'Flag_HBHENoiseFilter') else True) and (self.tr.Flag_EcalDeadCellTriggerPrimitiveFilter if hasattr(self.tr, 'Flag_EcalDeadCellTriggerPrimitiveFilter') else True) and (self.tr.Flag_eeBadScFilter if hasattr(self.tr, 'Flag_eeBadScFilter') else True) and (self.tr.Flag_BadPFMuonFilter if hasattr(self.tr, 'Flag_BadPFMuonFilter') else True)
