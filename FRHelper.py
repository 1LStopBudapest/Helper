import ROOT
import math
import os, sys

sys.path.append('../')
from Sample.Dir import Xfiles
from Sample.FileList_Fake_UL2016PostVFP import samples as samples_2016Post
from Sample.SampleChain import SampleChain

class FRHelper():

    def __init__(self, yr, sample):
        self.year_str = str(yr)
        self.sample = sample
        self.MuSample = ['DoubleMuon', 'DoubleMuon', 'DoubleMuon', 'DoubleMuon', 'SingleMuon', 'SingleMuon']
        self.EleSample = ['JetHT', 'JetHT', 'DoubleEG', 'DoubleEG', 'DoubleEG', 'DoubleEG']
        self.MuTrig16 = ['HLT_Mu3_PFJet40', 'HLT_Mu3_PFJet40', 'HLT_Mu8', 'HLT_Mu17', 'HLT_Mu27', 'HLT_Mu27']
        self.EleTrig16 = ['HLT_PFJet40', 'HLT_PFJet40', 'HLT_Ele8_CaloIdM_TrackIdM_PFJet30', 'HLT_Ele17_CaloIdM_TrackIdM_PFJet30', 'HLT_Ele23_CaloIdM_TrackIdM_PFJet30', 'HLT_Ele23_CaloIdM_TrackIdM_PFJet30']
        self.MuLumi16 = [SampleChain.luminosity_2016_HLT_Mu3_PFJet40, SampleChain.luminosity_2016_HLT_Mu3_PFJet40, SampleChain.luminosity_2016_HLT_Mu8, SampleChain.luminosity_2016_HLT_Mu17, SampleChain.luminosity_2016_HLT_Mu27, SampleChain.luminosity_2016_HLT_Mu27]
        self.EleLumi16 = [SampleChain.luminosity_2016_HLT_PFJet40, SampleChain.luminosity_2016_HLT_PFJet40, SampleChain.luminosity_2016_HLT_Ele8_CaloIdM_TrackIdM_PFJet30,  SampleChain.luminosity_2016_HLT_Ele17_CaloIdM_TrackIdM_PFJet30, SampleChain.luminosity_2016_HLT_Ele23_CaloIdM_TrackIdM_PFJet30, SampleChain.luminosity_2016_HLT_Ele23_CaloIdM_TrackIdM_PFJet30]


    def getSamplelist(self):
        if self.year_str=='2016PreVFP':
            samplelist = samples_2016Pre 
        elif self.year_str=='2016PostVFP':
            samplelist = samples_2016Post 
        elif self.year_str=='2016':
            samplelist = FileList_Fake_2016_janik.samples 
        elif self.year_str=='2017':
            samplelist = samples_2017 
        else:
            samplelist = samples_2018 
        return samplelist

    def getSample(self, pTbin, lep):
        if 'Run' in self.sample or 'Data' in self.sample:
            if lep == 'Mu':
                sample = self.MuSample[pTbin] + '_Data' if self.sample=='Data' else self.MuSample[pTbin] + self.sample[self.sample.find('_'):]
                
            else:
                sample = self.EleSample[pTbin] + '_Data' if self.sample=='Data' else self.EleSample[pTbin] + self.sample[self.sample.find('_'):]
        else:
            sample = self.sample
        return sample
    
    def getLumiTrig(self, pTbin, lep):
        if self.year_str=='2016PreVFP':
            if lep == 'Mu':
                lumitrig = [self.MuLumi16[pTbin] * (SampleChain.luminosity_2016PreVFP/SampleChain.luminosity_2016), self.MuTrig16[pTbin]]
            else:
                lumitrig = [self.EleLumi16[pTbin] * (SampleChain.luminosity_2016PreVFP/SampleChain.luminosity_2016), self.EleTrig16[pTbin]]
        elif self.year_str=='2016PostVFP':
            if lep == 'Mu':
                lumitrig = [self.MuLumi16[pTbin] * (SampleChain.luminosity_2016PostVFP/SampleChain.luminosity_2016), self.MuTrig16[pTbin]]
            else:
                lumitrig = [self.EleLumi16[pTbin] * (SampleChain.luminosity_2016PostVFP/SampleChain.luminosity_2016), self.EleTrig16[pTbin]]
        elif self.year_str=='2017':
            if lep == 'Mu':
                lumitrig = [self.MuLumi17[pTbin], self.MuTrig16[pTbin]]
            else:
                lumitrig = [self.EleLumi17[pTbin], self.EleTrig16[pTbin]]
        else:
            if lep == 'Mu':
                lumitrig = [self.MuLumi17[pTbin], self.MuTrig16[pTbin]]
            else:
                lumitrig = [self.EleLumi17[pTbin], self.EleTrig16[pTbin]]
        return lumitrig
            
    def get_PU_weight( ntruint ):
        if self.year_str=='2016PreVFP' or self.year_str=='2016PostVFP':
            pufile = os.path.join(Xfiles, 'normalized_data_MC_PU.root')
        elif self.year_str=='2017':
            pufile = os.path.join(Xfiles, 'normalized_data_MC_PU.root')
        else:
            pufile = os.path.join(Xfiles, 'normalized_data_MC_PU.root')
        f1 = ROOT.TFile.Open(pufile)
        hist_PU_reweight = f1.Get("ratio_PU_data_MC")
        return hist_PU_reweight.GetBinContent(hist_PU_reweight.FindBin(ntruint))

    def getTLvalue(self, lep , leppt , lepeta):
        pt_Binning = [3.5, 5.0, 8, 10, 15, 20, 30, 50]
        eta_Binning = [0.,1.442,1.566,3.142]
        fname = 'h_TLratio_2D_'+lep+'.root'
        TLfile = os.path.join(Xfiles, fname)
        f = ROOT.TFile.Open(TLfile)
        hist_TL_values = f.Get("h_TLratio_2D")
        value = 0.0
        for i in range(len(pt_Binning)-1):
            if abs(lepeta)>=eta_Binning[0] and abs(lepeta)<=eta_Binning[1]:
                if leppt >= pt_Binning[i] and leppt < pt_Binning[i+1]:
                    value = hist_TL_values.GetBinContent(i+1 , 1)
            if abs(lepeta)>=eta_Binning[2] and abs(lepeta)<=eta_Binning[3]:
                if leppt >= pt_Binning[i] and leppt < pt_Binning[i+1]:
                    value = hist_TL_values.GetBinContent(i+1 , 3)
        return value
                                                                                                                                                                                     
