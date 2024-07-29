''' 
gen filter efficiecny for mStop and mNeu for prompt signal samples.
'''
import ROOT
import os, sys 
import pandas as pd
#import pickle


sys.path.append('../')
from Sample.Dir import Xfiles

class GenFilterEff:
	def __init__(self, year):
                self.filepath = Xfiles
                self.name = "csv_appended_filterEff.csv"
                self.csvFile    = os.path.join(self.filepath,self.name)
                
                #self.name = "filterEffs_T2tt_dM_10to80_genHT_160_genMET_80_mWMin0p1"
		#pklFile= os.path.join(self.filepath,"filterEffs_T2tt_dM_10to80_genHT_160_genMET_80_mWMin0p1.pkl")
		#self.eff=pickle.load(file(pklFile))

        def getEff(self, mStop, mNeu):
                df = pd.read_csv(self.csvFile, usecols= ["m","dm","filterEff"])
                if mStop%5 != 0:
                        mStop = mStop-1
                dM = mStop - mNeu
                filterEff = df.loc[(df.m==mStop ) & (df.dm==dM ),'filterEff'].values[0]
                return filterEff

        '''        
	def getEffFromPkl(self, mStop, mNeu):
		print mStop,mNeu
		genEff=self.eff[mStop][mNeu]
		print genEff
		return genEff 	
	def getEff(self, mStop, mNeu) :
		effFile = ROOT.TFile("{}{}.root".format(self.filepath,self.name))
		canvas = effFile.Get("c1")
		hist2D = canvas.GetPrimitive(self.name)
		shift_x = 0.
		shift_y = 0.
		mStop = mStop - mStop%25
		mNeu = mNeu - mNeu%5
		bin_x, bin_y = hist2D.GetXaxis().FindBin(mStop-shift_x), hist2D.GetYaxis().FindBin(mNeu-shift_y)
		genEff = hist2D.GetBinContent(bin_x, bin_y)
		return genEff
        '''
