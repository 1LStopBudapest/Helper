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
    def PreSelection(self, jettp = 'Nom'):
        ps = self.METcut() and self.HTcut(tp=jettp) and self.ISRcut(tp=jettp) and self.lepcut() and self.dphicut(tp=jettp) and self.XtralepVeto() and self.XtraJetVeto(tp=jettp) and self.tauVeto()
        #print jettp, self.HTcut(tp=jettp)
        return ps

    def SearchRegion(self, jettp = 'Nom'):
        if not self.PreSelection(jettp):
            return False
        else:
            lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
            if len(lepvar) >= 1 and lepvar[0]['pt']<=50 and self.tr.MET_pt > 300:
                return True
            else:
                return False

    def SR1(self, jettp = 'Nom'):
        if not self.SearchRegion(jettp):
            return False
        else:
            return True if self.cntBtagjet(20, jettp)==0 and self.cntBtagjet(60, jettp)==0 and self.calHT(tp=jettp)>400 and self.calCT(1, jettp)>300 and abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['eta']) < 1.5 and self.R1R3NoOvrlp(jettp) else False

    def SR2(self, jettp = 'Nom'):
        if not self.SearchRegion(jettp):
            return False
        else:
            return True if self.cntBtagjet(20, jettp)>=1 and self.cntBtagjet(60, jettp)==0 and len(self.selectjetIdx(325, jettp))>0 and self.calCT(2, jettp)>300  else False

    def SR3(self, jettp = 'Nom'):#softb (SV) region, extension of SR2 in term of CT and other cuts but requires softbjets == 0 and softb (SV) >= 1
        if not self.SearchRegion(jettp):
            return False
        else:
            return True if self.cntBtagjet(20, jettp)==0 and self.cntBtagjet(60, jettp)==0 and len(self.selectjetIdx(325, jettp))>0 and self.calCT(2, jettp)>300 and self.cntSoftB(tp=jettp)>=1 else False

    def R1R3NoOvrlp(self, jettp='Nom'):
        if len(self.selectjetIdx(325, jettp))>0:
            if self.cntSoftB(jettp)==0:
                return True
            else:
                return False
        else:
            return True

        
    def ControlRegion(self, jettp='Nom'):
        if not self.PreSelection(jettp):
            return False
        else:
            lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
            if len(lepvar) > 1 and lepvar[0]['pt']>50:
                return True
            else:
                return False

    def CR1(self, jettp='Nom'):
        if not self.ControlRegion(jettp):
            return False
        else:
            return True if self.cntBtagjet(20, jettp)==0 and self.cntBtagjet(60, jettp)==0 and self.calHT(tp=jettp)>400 and self.calCT(1, jettp)>300 and abs(sortedlist(self.getLepVar(self.selectMuIdx()))[0]['eta']) < 1.5 and self.R1R3NoOvrlp(jettp) else False

    def CR2(self, jettp='Nom'):
        if not self.ControlRegion(jettp):
            return False
        else:
            return True if self.cntBtagjet(20, jettp)>=1 and self.cntBtagjet(60, jettp)==0 and len(self.selectjetIdx(325, jettp))>0 and self.calCT(2, jettp)>300  else False

    def CR3(self, jettp='Nom'):
        if not self.ControlRegion(jettp):
            return False
        else:
            return True if self.cntBtagjet(20, jettp)==0 and self.cntBtagjet(60, jettp)==0 and len(self.selectjetIdx(325, jettp))>0 and self.calCT(2, jettp)>300  and self.cntSoftB(tp=jettp)>=1 else False

    #cuts
    def ISRcut(self, thr=100, tp='Nom'):
        return len(self.selectjetIdx(thr, tp)) > 0

    def METcut(self, thr=200):
        cut = False
        if self.tr.MET_pt > thr:
            cut = True
        return cut
        
    def HTcut(self, thr=300, tp='Nom'):
        cut = False
        HT = self.calHT(tp)
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
    def dphicut(self, thr=20, tp='Nom'):
        cut = True
        if tp == 'JECUp': Jet_pt = self.tr.Jet_pt_jerUp
        elif tp == 'JECDown': Jet_pt = self.tr.Jet_pt_jerDown
        elif tp == 'JERUp': Jet_pt = self.tr.Jet_pt_jesTotalUp
        elif tp == 'JERDown': Jet_pt = self.tr.Jet_pt_jesTotalDown
        else: Jet_pt = self.tr.Jet_pt
        
        if len(self.selectjetIdx(thr, tp)) >=2 and Jet_pt[self.selectjetIdx(thr, tp)[0]]> 100 and Jet_pt[self.selectjetIdx(thr, tp)[1]]> 60:
            Adphi = min( DeltaPhi(self.tr.Jet_phi[self.selectjetIdx(thr, tp)[0]], self.tr.MET_phi), DeltaPhi(self.tr.Jet_phi[self.selectjetIdx(thr, tp)[1]], self.tr.MET_phi))
        elif len(self.selectjetIdx(thr, tp)) >= 1 and Jet_pt[self.selectjetIdx(thr, tp)[0]]> 100:
            Adphi = DeltaPhi(self.tr.Jet_phi[self.selectjetIdx(thr, tp)[0]], self.tr.MET_phi)
        else:
            Adphi = -999
            
        if Adphi < 0.5:
                cut = False
        return cut

    def lepcut(self):
        return len(self.getLepVar(self.selectMuIdx())) >= 1
    
    
    def XtralepVeto(self):
        cut = True
        lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
        if len(lepvar) > 1 and lepvar[1]['pt']>20:
            cut = False
        return cut

    def XtraJetVeto(self, thrJet=20, thrExtra=60, tp='Nom'):
        cut = True
        if tp == 'JECUp': Jet_pt = self.tr.Jet_pt_jerUp
        elif tp == 'JECDown': Jet_pt = self.tr.Jet_pt_jerDown
        elif tp == 'JERUp': Jet_pt = self.tr.Jet_pt_jesTotalUp
        elif tp == 'JERDown': Jet_pt = self.tr.Jet_pt_jesTotalDown
        else: Jet_pt = self.tr.Jet_pt
        
        if len(self.selectjetIdx(thrJet, tp)) >= 3 and Jet_pt[self.selectjetIdx(thrJet, tp)[2]] > thrExtra:
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

    def calCT(self, i, tp='Nom'):
        return CT1(self.tr.MET_pt, self.calHT(tp)) if i==1 else CT2(self.tr.MET_pt, self.getISRPt(tp))
        
    def calHT(self, tp='Nom'):
        HT = 0
        if tp == 'JECUp': Jet_pt = self.tr.Jet_pt_jerUp
        elif tp == 'JECDown': Jet_pt = self.tr.Jet_pt_jerDown
        elif tp == 'JERUp': Jet_pt = self.tr.Jet_pt_jesTotalUp
        elif tp == 'JERDown': Jet_pt = self.tr.Jet_pt_jesTotalDown
        else: Jet_pt = self.tr.Jet_pt
        
        for i in self.selectjetIdx(20, tp):
            HT = HT + Jet_pt[i]
        return HT

    def calNj(self, thrsld=20, tp='Nom'):
        return len(self.selectjetIdx(thrsld, tp))
        
    def getISRPt(self, tp='Nom'):
        if tp == 'JECUp': Jet_pt = self.tr.Jet_pt_jerUp
        elif tp == 'JECDown': Jet_pt = self.tr.Jet_pt_jerDown
        elif tp == 'JERUp': Jet_pt = self.tr.Jet_pt_jesTotalUp
        elif tp == 'JERDown': Jet_pt = self.tr.Jet_pt_jesTotalDown
        else: Jet_pt = self.tr.Jet_pt
        return Jet_pt[self.selectjetIdx(100, tp)[0]] if len(self.selectjetIdx(100, tp)) else 0
    
    def cntBtagjet(self, discOpt='DeepCSV', pt=20, tp='Nom'):
        return len(self.selectBjetIdx(discOpt, pt, tp))

    def cntSoftB(self, tp='Nom'):
        return len(self.selectSoftBIdx(tp))
    
    
    def selectjetIdx(self, thrsld, tp='Nom'):
        if tp == 'JECUp': Jet_pt = self.tr.Jet_pt_jerUp
        elif tp == 'JECDown': Jet_pt = self.tr.Jet_pt_jerDown
        elif tp == 'JERUp': Jet_pt = self.tr.Jet_pt_jesTotalUp
        elif tp == 'JERDown': Jet_pt = self.tr.Jet_pt_jesTotalDown
        else: Jet_pt = self.tr.Jet_pt
        lepvar = sortedlist(self.getLepVar(self.selectMuIdx()))
        idx = []
        d = {}
        for j in range(len(Jet_pt)):
            clean = False
            if Jet_pt[j] > thrsld and abs(self.tr.Jet_eta[j]) < 2.4 and self.tr.Jet_jetId[j] > 0:
                clean = True
                for l in range(len(lepvar)):
                    dR = DeltaR(lepvar[l]['eta'], lepvar[l]['phi'], self.tr.Jet_eta[j], self.tr.Jet_phi[j])
                    ptRatio = float(Jet_pt[j])/float(lepvar[l]['pt'])
                    if dR < 0.4 and ptRatio < 2:
                        clean = False
                        break
                if clean:
                    d[j] = Jet_pt[j]
        od = coll.OrderedDict(sorted(d.items(), key=lambda x:x[1], reverse=True))
        for i in od:
            idx.append(i)
        return idx

    def selectBjetIdx(self, discOpt='DeepCSV', ptthrsld=20, tp='Nom'):
        idx = []
        for i in self.selectjetIdx(ptthrsld, tp):
            if self.isBtagDeepCSV(self.tr.Jet_btagDeepB[i], self.yr):
                idx.append(i)
        return idx

    def selectSoftBIdx(self, tp='Nom'):
        indx = []
        for idx in self.IVFIdx():
            if self.tr.SV_pt[idx] < 20.0 \
               and self.jetcleanedB(idx,tp) :
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
            Llist.append({'pt':self.tr.Muon_pt[id], 'eta':self.tr.Muon_eta[id], 'phi':self.tr.Muon_phi[id], 'dxy':self.tr.Muon_dxy[id], 'dxyErr':self.tr.Muon_dxyErr[id], 'dz': self.tr.Muon_dz[id], 'charg':self.tr.Muon_charge[id], 'idx': id, 'type':'mu'})
        return Llist

    def getEleVar(self):
        return ANEle(self.tr, self.eletype, self.elepref).getANEleVar()
    
    def getLepVar(self, muId):
        Llist = []
        for id in muId:
            Llist.append({'pt':self.tr.Muon_pt[id], 'eta':self.tr.Muon_eta[id], 'phi':self.tr.Muon_phi[id], 'dxy':self.tr.Muon_dxy[id], 'dxyErr':self.tr.Muon_dxyErr[id], 'dz': self.tr.Muon_dz[id], 'charg':self.tr.Muon_charge[id], 'idx': id, 'type':'mu'})
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
               

    def jetcleanedB(self, idx, tp='Nom'):
        ret = True
        for j in self.selectjetIdx(20, tp):
            if DeltaR(self.tr.SV_eta[idx], self.tr.SV_phi[idx], self.tr.Jet_eta[j], self.tr.Jet_phi[j]) < 0.4 :
                ret = False
                break
        return ret
            

    def passFilters(self):
        return (self.tr.Flag_goodVertices if hasattr(self.tr, 'Flag_goodVertices') else True) and (self.tr.Flag_globalSuperTightHalo2016Filter if hasattr(self.tr, 'Flag_globalSuperTightHalo2016Filter') else True) and (self.tr.Flag_HBHENoiseIsoFilter if hasattr(self.tr, 'Flag_HBHENoiseIsoFilter') else True) and (self.tr.Flag_HBHENoiseFilter if hasattr(self.tr, 'Flag_HBHENoiseFilter') else True) and (self.tr.Flag_EcalDeadCellTriggerPrimitiveFilter if hasattr(self.tr, 'Flag_EcalDeadCellTriggerPrimitiveFilter') else True) and (self.tr.Flag_eeBadScFilter if hasattr(self.tr, 'Flag_eeBadScFilter') else True) and (self.tr.Flag_BadPFMuonFilter if hasattr(self.tr, 'Flag_BadPFMuonFilter') else True)
