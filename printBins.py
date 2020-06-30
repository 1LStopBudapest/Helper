import ROOT
import math
import os, sys


from Helper.Binning import *

isr = findBinIndex(400, 100, 25)
csr = findCTBin(400)
msr = findMTBin(100)
lsr = findLepPtBin(26, 100)
b = findBin(401, 70, 5)
l = getBinlabel(401, 70, 5, 'CR')
print isr, csr, msr, lsr, b, l
