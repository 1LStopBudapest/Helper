import ROOT
import os, sys 
from math import sqrt


sys.path.append('../')
from Sample.Dir import Xfiles

class SoftbSF:
	def __init__(self, year):
                self.year = year
                self.filepath = Xfiles
                self.softBf = 'DataMCSF_softb.txt'
                
        def getsoftbSF(self):
                SF = {}
                fname = os.path.join(self.filepath, self.softBf)
                with open(fname,'r') as ifile:
                        for line in ifile:
                                line = line.rstrip()
                                linesplit = line.split(',')
                                SF[linesplit[0]] = tuple((float(linesplit[1]), float(linesplit[2])))
                return SF[self.year][0]



