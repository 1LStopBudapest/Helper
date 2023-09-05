import ROOT
import numpy as np
import types

class HistInfo( ):

    def __init__(self, hname = None, sample = None, texX = None, texY = None, binning = [], histclass = None, binopt = 'norm'):
        self.hname = hname
        self.sample = sample
        self.texX = texX
        self.texY = texY
        self.binning = binning
        self.histclass = histclass
        self.binopt = binopt
        if isinstance(binning[0], types.ListType):
            self.binArrX = np.array(binning[0], dtype='float64')
            self.binArrY = np.array(binning[1], dtype='float64')
        else:
            self.binArrX = np.array(binning, dtype='float64')
            self.binArrY = np.array(binning, dtype='float64')
        
    def make_hist1D(self):
        if self.binopt == 'norm':
            hist = self.histclass(self.hname+'_'+self.sample, self.hname, self.binning[0], self.binning[1], self.binning[2])
        else:
            nbins = len(self.binning) - 1
            hist = self.histclass(self.hname+'_'+self.sample, self.hname, nbins, self.binArrX)
        hist.Sumw2()
        return hist

    def make_hist2D(self):
        if self.binopt == 'norm':
            hist = self.histclass(self.hname+'_'+self.sample, self.hname, self.binning[0][0], self.binning[0][1], self.binning[0][2], self.binning[1][0], self.binning[1][1], self.binning[1][2])
        else:
            nbinsX = len(self.binning[0]) - 1
            nbinsY = len(self.binning[1]) - 1
            hist = self.histclass(self.hname+'_'+self.sample, self.hname, nbinsX, self.binArrX, nbinsY, self.binArrY)
        hist.Sumw2()
        return hist

    def make_hist(self):
        return self.make_hist1D() if self.histclass == ROOT.TH1F else self.make_hist2D()

    def getType(self):
        return self.histclass
        
