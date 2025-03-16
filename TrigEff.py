import os, sys

TrigDict = {
    '2016PreVFP': 0.96,
    '2016PostVFP': 0.96,
    '2016': 0.96,
    '2017': 0.97,
    '2018': 0.97
}

def getTrigEff(yr):
    return TrigDict[yr] if yr in TrigDict.keys() else 1.00
