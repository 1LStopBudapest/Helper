import ROOT
import math
import os, sys


from Binning import *

print len(SRBinLabelList), len(CRBinLabelList), len(SRCRBinLabelList)

isr = findSR1BinIndex(499, 96, 4, -1)
csr = findCTBin(400)
msr = findMTBin(100)
lsr = findLepPtBin(26, 100)
b = findBin(400, 50, 3.6)
l = getBinlabel(401, 70, 5, 'SR')
l1 = getBinlabel(400, 100, 50, 'CR')
jsr = findCR2BinIndex(401, 190)

tr1 = findReg1BinIndex(499, 131, 51, -1)
tr2 = findReg2BinIndex(399, 60, 4)
print isr, csr, msr, lsr, b, l, l1, jsr, tr1, tr2 
print SRBinLabelList[isr]
print CRBinLabelList[jsr]
print SRCRBinLabelList[tr1]
print SRCRBinLabelList[tr2]
