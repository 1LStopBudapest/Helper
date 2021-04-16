import ROOT
import math
import os, sys


from Binning import *

isr = findSR1BinIndex(499, 100, 31, -1)
csr = findCTBin(400)
msr = findMTBin(100)
lsr = findLepPtBin(26, 100)
b = findBin(400, 50, 3.6)
l = getBinlabel(401, 70, 5, 'SR')
l1 = getBinlabel(400, 100, 50, 'CR')
jsr = findCR2BinIndex(401, 190)
print isr, csr, msr, lsr, b, l, l1, jsr
