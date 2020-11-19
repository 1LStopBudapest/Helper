import ROOT
import math
import os, sys


from Binning import *

isr = findSR1BinIndex(401, 66, 30, -1)
csr = findCTBin(400)
msr = findMTBin(100)
lsr = findLepPtBin(26, 100)
b = findBin(401, 70, 5)
l = getBinlabel(401, 70, 5, 'SR')
l1 = getBinlabel(400, 100, 50, 'CR')
jsr = findCR2BinIndex(401, 100)
print isr, csr, msr, lsr, b, l, l1, jsr
