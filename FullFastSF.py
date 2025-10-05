''' 
Fullsim/Fastsim Scale factor
'''
import ROOT
import os, sys 
from math import sqrt


sys.path.append('../')
from Sample.Dir import Xfiles

class FullFastSF:
	def __init__(self, year):
                self.year = year
                self.filepath = Xfiles
                self.softBf = 'FullFastSF_softb.txt'
                if '2018' in year:
                        self.mukey = ['FastFullLepSF_mu_2018.root', 'hsfmu_2018']
                        self.elekey = ['FastFullLepSF_ele_2018.root','hsfele_2018']
                elif '2017' in year:
                        self.mukey = ['FastFullLepSF_mu_2017.root', 'hsfmu_2017']
                        self.elekey = ['FastFullLepSF_ele_2017.root','hsfele_2017']
                elif '2016PostVFP' in year:
                        self.mukey = ['FastFullLepSF_mu_2016PostVFP.root', 'hsfmu_2016PostVFP']
                        self.elekey = ['FastFullLepSF_ele_2016PostVFP.root','hsfele_2016PostVFP']
                else:
                        self.mukey = ['FastFullLepSF_mu_2016PreVFP.root', 'hsfmu_2016PreVFP']
                        self.elekey = ['FastFullLepSF_ele_2016PreVFP.root','hsfele_2016PreVFP']

        def getsoftbSF(self):
                SF = {}
                fname = os.path.join(self.filepath, self.softBf)
                with open(fname,'r') as ifile:
                        for line in ifile:
                                line = line.rstrip()
                                linesplit = line.split(',')
                                SF[linesplit[0]] = tuple((float(linesplit[1]), float(linesplit[2])))
                return SF[self.year][0]


        def getLepSF(self, pt, eta, tp):
                if pt>=100: pt = 99
                lkey = self.mukey if 'mu' in tp else self.elekey
                fname = os.path.join(self.filepath, lkey[0])
                sff = ROOT.TFile(fname)
                hist = sff.Get(lkey[1])
                bin_x, bin_y = hist.GetXaxis().FindBin(pt), hist.GetYaxis().FindBin(abs(eta))
                sf = hist.GetBinContent(bin_x, bin_y) if hist.GetBinContent(bin_x, bin_y) != 0 else 1
                sferr = hist.GetBinError(bin_x, bin_y)
                
                return sf


