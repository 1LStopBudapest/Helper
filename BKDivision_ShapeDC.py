import os, sys
import ROOT

sys.path.append('../')
from Sample.Dir import plotDir


def get_parser():
    ''' Argument parser.                                                                                                                                                 
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument(
    '-l', '--samplelist',                   # either of this switches
    nargs='+',                              # one or more parameters to this switch
    type=str,                               # /parameters/ are ints
    dest='alist',                           # store in 'list'.
        default=['VV', 'TTV', 'ZJetsToNuNu', 'QCD', 'DYJetsToLL', 'ST', 'TTbar', 'WJetsToLNu'],     # all the BK samples
    )
    argParser.add_argument('--filename',            action='store',                    type=str,            default='ShapeDCHistJEC_SR+CR',          help="root file name" )
    argParser.add_argument('--filedir',            action='store',                    type=str,            default='PromptDCFiles',          help="Which directory input files are located?" )

    return argParser

options = get_parser().parse_args()

samplelists = options.alist
filedir = options.filedir
filename = options.filename

XtraPrompt = ['VV', 'TTV', 'DYJetsToLL', 'ST']
TotFake = ['ZJetsToNuNu', 'QCD']
Procs = ['WJets', 'ttbar', 'OtherPrompt', 'Fake']
files = []
fexists = True

for sl in samplelists:
    if os.path.exists(filename+'_'+sl+'.root'):
        files.append(ROOT.TFile.Open(filename+'_'+sl+'.root'))
    elif os.path.exists(plotDir+filedir+'/'+filename+'_'+sl+'.root'):
        files.append(ROOT.TFile.Open(plotDir+filedir+'/'+filename+'_'+sl+'.root'))
    else:
        fexists = False        
        print 'Root files for', sl, 'sample does not exist. Please run python '+filename+'.py --sample', sl, 'inside the correspoding directory'

histname = []
for i in range(24):
    histname.append('Bin'+str(i))

if 'JEC' in filename:
    sysname = ['Nom', 'JECUp', 'JECDown', 'JERUp', 'JERDown'] #for JEC unc root files
else:
    sysname  = ['PU', 'PUUp', 'PUDown', 'wPt', 'wPtUp', 'wPtDown', 'LeptonSF', 'LeptonSFUp', 'LeptonSFDown', 'BTag_SF', 'BTag_SF_b_Up', 'BTag_SF_b_Down', 'BTag_SF_l_Up', 'BTag_SF_l_Down', 'L1Prefire', 'L1PrefireUp', 'L1PrefireDown', 'XSec', 'XSecUp', 'XSecDown'] #these histos should present in the root files


hpo = []
hnp = []
hw = []
ht = []

if fexists:
    for i, f in enumerate(files,0):
        hpoi = []
        hnpi = []
        for hn in histname:
            if not 'JEC' in filename:
                if samplelists[i] in XtraPrompt: 
                    hpoi.append(f.Get(hn+'_prompt_'+samplelists[i]))
                if samplelists[i]=='WJetsToLNu':
                    hw.append(f.Get(hn+'_prompt_'+samplelists[i]))
                if samplelists[i]=='TTbar':
                    ht.append(f.Get(hn+'_prompt_'+samplelists[i]))
                if samplelists[i] in TotFake:
                    hnpi.append(f.Get(hn+'_'+samplelists[i]))
                else:
                    hnpi.append(f.Get(hn+'_nonprompt_'+samplelists[i]))

            for sn in sysname:
                if samplelists[i] in XtraPrompt: 
                    hpoi.append(f.Get(hn+'_prompt_'+sn+'_'+samplelists[i]))
                if samplelists[i]=='WJetsToLNu':
                    hw.append(f.Get(hn+'_prompt_'+sn+'_'+samplelists[i]))
                if samplelists[i]=='TTbar':
                    ht.append(f.Get(hn+'_prompt_'+sn+'_'+samplelists[i]))
                if samplelists[i] in TotFake:
                    hnpi.append(f.Get(hn+'_'+sn+'_'+samplelists[i]))
                else:
                    hnpi.append(f.Get(hn+'_nonprompt_'+sn+'_'+samplelists[i]))
        if len(hpoi): hpo.append(hpoi)
        hnp.append(hnpi)


pfilew = ROOT.TFile(plotDir+filedir+'/'+filename+'_'+Procs[0]+'.root', 'RECREATE')
for h in hw:
    h.SetName(h.GetTitle().replace('prompt',Procs[0]))
    h.Write()
pfilet = ROOT.TFile(plotDir+filedir+'/'+filename+'_'+Procs[1]+'.root', 'RECREATE')
for h in ht:
    h.SetName(h.GetTitle().replace('prompt',Procs[1]))
    h.Write()


hprompt=[]
for h in hpo[0]:
    hprompt.append(h.Clone())
hpcut = hpo[1:]
for hpi in hpcut:
    for i in range(len(hpi)):
        hprompt[i].Add(hpi[i])

pfileop = ROOT.TFile(plotDir+filedir+'/'+filename+'_'+Procs[2]+'.root', 'RECREATE')
for h in hprompt:
    h.SetName(h.GetTitle().replace('prompt',Procs[2]))
    h.Write()
    
hnprompt=[]
for h in hnp[0]:
    hnprompt.append(h.Clone())
hnpcut = hnp[1:]
for hnpi in hnpcut:
    for i in range(len(hnpi)):
        hnprompt[i].Add(hnpi[i])
npfile = ROOT.TFile(plotDir+filedir+'/'+filename+'_'+Procs[3]+'.root', 'RECREATE')
for h in hnprompt:
    h.SetName(h.GetTitle().replace('nonprompt',Procs[3]))
    h.Write()

