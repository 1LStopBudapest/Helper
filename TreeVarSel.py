from traceback import print_tb
import ROOT
import math
import os, sys
import collections as coll

from Helper.VarCalc import *
from ANEle import ANEle

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
            if len(lepvar) >= 1 and lepvar[0]['pt']<=50 and self.tr.MET_pt > 300:
                return True
            else:
                return False

    def SR1(self):
        if not self.SearchRegion():
            return False
        else:
            return True if self.cntBtagjet(pt=20)==0 and self.cntBtagjet(pt=60)==0 and self.calHT()>400 and self.calCT(1)>300 and abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['eta']) < 1.5 and self.SR1Veto() else False

    def SR2(self):
        if not self.SearchRegion():
            return False
        else:
            return True if self.cntBtagjet(pt=20)>=1 and self.cntBtagjet(pt=60)==0 and len(self.selectjetIdx(325))>0 and self.calCT(2)>300  else False

    def SR2extension(self):
        if not self.SearchRegion():
            return False
        else:
            return True if self.cntBtagjet(pt=20)==0 and self.cntBtagjet(pt=60)==0 and len(self.selectjetIdx(325))>0 and self.calCT(2)>300 and self.cntSoftB()>=1 else False

    def ControlRegion(self):
        if not self.PreSelection():
            return False
        else:
            lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
            if len(lepvar) > 1 and lepvar[0]['pt']>50:
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
                
    def SR1Veto(self):
        if len(self.selectjetIdx(325))>0:
            if self.cntSoftB()==0:
                return True
            else:
                return False
        else:
            return True

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
    def dphicut(self, thr=20): #old cut
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

    def calNj(self, thrsld):
        return len(self.selectjetIdx(thrsld))
        
    def getISRPt(self):
        return self.tr.Jet_pt[self.selectjetIdx(100)[0]] if len(self.selectjetIdx(100)) else 0
    
    def getISRJetEta(self):
        return self.tr.Jet_eta[self.selectjetIdx(100)[0]] if len(self.selectjetIdx(100)) else -99

    def getNthJetPt(self, thr=20, N=2):
        return self.tr.Jet_pt[self.selectjetIdx(thr)[N-1]] if len(self.selectjetIdx(thr)) >= N else -1

    def getNthJetEta(self, thr=20, N=2):
        return self.tr.Jet_eta[self.selectjetIdx(thr)[N-1]] if len(self.selectjetIdx(thr)) >= N else -99

    def getJetPt(self):
        pT = []
        for i in range(len(self.selectjetIdx(20))):
            pT.append(self.tr.Jet_pt[self.selectjetIdx(20)[i]])
        return pT

    def getDeltaPhiJets(self, thr=20):
        if len(self.selectjetIdx(100)) and len(self.selectjetIdx(thr)) >= 2:
            return DeltaPhi(self.tr.Jet_phi[self.selectjetIdx(100)[0]], self.tr.Jet_phi[self.selectjetIdx(thr)[1]])
        else:
            return -1

    def getJetPhi(self):
        phi = []
        for i in range(len(self.selectjetIdx(20))):
            phi.append(self.tr.Jet_phi[self.selectjetIdx(20)[i]])
        return phi

    def getJetEta(self):
        eta = []
        for i in range(len(self.selectjetIdx(20))):
            eta.append(self.tr.Jet_eta[self.selectjetIdx(20)[i]])
        return eta

    def getBjetPt(self, discOpt='DeepCSV', pt=20):
        b_pt = []
        for i in range(len(self.selectBjetIdx(discOpt, pt))):
            b_pt.append(self.tr.Jet_pt[self.selectBjetIdx(discOpt, pt)[i]])
        return b_pt #if len(b_pt) else 0

    def get1stBjetPt(self, discOpt='DeepCSV', pt=20):
        return self.tr.Jet_pt[self.selectBjetIdx(discOpt, pt)[0]] if len(self.selectBjetIdx(discOpt, pt)) else -1

    def get1stBjetEta(self, discOpt='DeepCSV', pt=20):
        return self.tr.Jet_eta[self.selectBjetIdx(discOpt, pt)[0]] if len(self.selectBjetIdx(discOpt, pt)) else -99


    def cntBtagjet(self, discOpt='DeepCSV', pt=20):
        return len(self.selectBjetIdx(discOpt, pt))

    def cntSoftB(self):
        return len(self.selectSoftBIdx())
    
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
            if self.isBtagDeepCSV(self.tr.Jet_btagDeepB[i], self.yr):
                idx.append(i)
        return idx

    def selectSoftBIdx(self):
        indx = []
        for idx in self.IVFIdx():
            if self.tr.SV_pt[idx] < 20.0 \
               and self.jetcleanedB(idx) :
                indx.append(idx)
        return indx


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


    def muonSelector( self, pt, eta, iso, dxy, dz, Id, lepton_selection='HybridIso'):
        if lepton_selection == 'HybridIso':
            def func():
                if pt <= 12 and pt >3: #new transition point 12 GeV
                    return \
                        abs(eta)       < 2.4 \
                        and (iso* pt) < 2.4 \
                        and abs(dxy)       < 0.02 \
                        and abs(dz)        < 0.1 \
                        and Id
                elif pt > 12:
                    return \
                        abs(eta)       < 2.4 \
                        and iso < 0.2 \
                        and abs(dxy)       < 0.02 \
                        and abs(dz)        < 0.1 \
                        and Id
            
        elif lepton_selection == 'looseHybridIso':
            def func():
                if pt <= 12 and pt >3:
                    return \
                        abs(eta)       < 2.4 \
                        and (iso*pt) < 20.0 \
                        and abs(dxy)       < 0.1 \
                        and abs(dz)        < 0.5 \
                        and Id
                elif pt > 12:
                    return \
                        abs(eta)       < 2.4 \
                        and iso < 0.8 \
                        and abs(dxy)       < 0.1 \
                        and abs(dz)        < 0.5 \
                        and Id
        else:
            def func():
                return \
                    pt >3 \
                    and abs(eta)       < 2.4 \
                    and Id
        return func()



    def IVFIdx(self):
        idx = []
        for i in range(self.tr.nSV):
            if bytearray(self.tr.SV_ntracks[i])[0] >= 3 \
               and self.tr.SV_dxy[i] < 2.5 \
               and self.tr.SV_dxySig[i] > 3.0 \
               and self.tr.SV_mass[i] < 6.5 \
               and self.tr.SV_dlenSig[i] > 4.0 \
               and self.tr.SV_pAngle[i] > 0.98 :
                idx.append(i)
        return idx
               

    def jetcleanedB(self, idx):
        ret = True
        for j in self.selectjetIdx(20):
            if DeltaR(self.tr.SV_eta[idx], self.tr.SV_phi[idx], self.tr.Jet_eta[j], self.tr.Jet_phi[j]) < 0.4 :
                ret = False
                break
        return ret
            
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

# good taus in IVF
    def getGoodTaus(self):
        taus = sortedlist(self.getTauVar(self.selectTauIdx()))
        leptons = sortedlist(self.getLepVar(self.selectMuIdx(), self.selectEleIdx()))
        res  =  []
        for tau in taus:
            clean = True
            for lepton in leptons:
                if DeltaPhi(lepton['phi'], tau['phi'])**2 + (lepton['eta'] - tau['eta'])**2 < 0.4:
                    clean = False
                    break
            if clean:
                res.append(tau)
        return res

    def getTauVar(self, tauId):
        Llist = []
        for id in tauId:
            Llist.append({'pt':self.tr.Tau_pt[id], 'eta':self.tr.Tau_eta[id], 'phi':self.tr.Tau_phi[id], 'dxy':self.tr.Tau_dxy[id], 'dz': self.tr.Tau_dz[id], 'charg':self.tr.Tau_charge[id]})
        return Llist

    def selectTauIdx(self):
        idx = []
        for i in range(self.tr.nTau):
            if (self.tr.Tau_pt[i] >= 20 and abs(self.tr.Tau_eta[i]) < 2.3): # and ord(self.tr.Tau_idMVAnewDM2017v2) >=2 ???
                idx.append(i)
        return idx
