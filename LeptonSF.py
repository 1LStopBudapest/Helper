''' 
Lepton Scale factor
'''
import ROOT
import os, sys 
from math import sqrt


sys.path.append('../')
from Sample.Dir import Xfiles

class LeptonSF:
	def __init__(self, year):
                self.filepath = Xfiles
                if '2018' in year:
                        self.mukey = [('mu_SF_2D_LooseWP_cent_LooseWP_priv_3p5-20_2018_merged.root', 'mu_SF_2D_LooseWP_cent_LooseWP_priv_3p5-20_2018_merged'), ('2018_mu_sf_merged.root', 'muon_SF_IpIsoSpec_2D_merged')]
                        self.elekey = [('el_SF_2D_VetoWP_cent_VetoWP_priv_5-10_2018_merged.root', 'el_SF_2D_VetoWP_cent_VetoWP_priv_5-10_2018_merged'), ('2018_el_sf_merged.root', 'ele_SF_IpIso_2D_merged')]
                elif '2017' in year:
                        self.mukey = [('mu_SF_2D_LooseWP_cent_LooseWP_priv_3p5-20_2018_merged.root', 'mu_SF_2D_LooseWP_cent_LooseWP_priv_3p5-20_2018_merged'), ('2018_mu_sf_merged.root', 'muon_SF_IpIsoSpec_2D_merged')]
                        self.elekey = [('el_SF_2D_VetoWP_cent_VetoWP_priv_5-10_2018_merged.root', 'el_SF_2D_VetoWP_cent_VetoWP_priv_5-10_2018_merged'), ('2018_el_sf_merged.root', 'ele_SF_IpIso_2D_merged')]
                else:
                        self.mukey = [('mu_SF_2D_LooseWP_cent_LooseWP_priv_3p5-20_2018_merged.root', 'mu_SF_2D_LooseWP_cent_LooseWP_priv_3p5-20_2018_merged'), ('2018_mu_sf_merged.root', 'muon_SF_IpIsoSpec_2D_merged')]
                        self.elekey = [('el_SF_2D_VetoWP_cent_VetoWP_priv_5-10_2018_merged.root', 'el_SF_2D_VetoWP_cent_VetoWP_priv_5-10_2018_merged'), ('2018_el_sf_merged.root', 'ele_SF_IpIso_2D_merged')]


        def axisVar(self, pt, eta, tp):
                return (pt, abs(eta)) if 'mu' in tp else (abs(eta), pt)

        def getLepSF(self, pt, eta, tp):
                lepsf = 1
                lepsferr = 0
                lepkey = self.mukey if 'mu' in tp else self.elekey
                for key in lepkey:
                        fname = os.path.join(self.filepath, key[0])
                        sff = ROOT.TFile(fname)
                        hist = sff.Get(key[1])
                        bin_x, bin_y = hist.GetXaxis().FindBin(self.axisVar(pt, eta, tp)[0]), hist.GetYaxis().FindBin(self.axisVar(pt, eta, tp)[1])
                        sf = hist.GetBinContent(bin_x, bin_y) if hist.GetBinContent(bin_x, bin_y) != 0 else 1
                        sferr = hist.GetBinError(bin_x, bin_y)
                        lepsf = lepsf * sf
                        lepsferr = lepsferr + (sferr * sferr)

                return (lepsf, lepsf+sqrt(lepsferr), lepsf-sqrt(lepsferr))


