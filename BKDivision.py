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
    argParser.add_argument('--filename',            action='store',                    type=str,            default='CountDCHist',          help="root file name" )
    argParser.add_argument('--filedir',            action='store',                    type=str,            default='1binPromptDCFiles',          help="Which directory input files are located?" )

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

if filename=='CountDCHist':
    hname = ['h_rate', 'h_PU', 'h_PUUp', 'h_PUDown', 'h_WPt', 'h_WPtUp', 'h_WPtDown', 'h_LeptonSF', 'h_LeptonSFUp', 'h_LeptonSFDown', 'h_BTagSF', 'h_BTagSFbUp', 'h_BTagSFbDown', 'h_BTagSFlUp', 'h_BTagSFlDown', 'h_XsecUp'] #these histos should present in the root files
else:
    hname = ['h_rate', 'h_JECUp', 'h_JECDown', 'h_JERUp', 'h_JERDown'] #for JEC unc root files
hpo = []
hnp = []
hw = []
ht = []

if fexists:
    for i, f in enumerate(files,0):
        hpoi = []
        hnpi = []
        for hn in hname:
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
        if len(hpoi): hpo.append(hpoi)
        hnp.append(hnpi)


pfilew = ROOT.TFile(plotDir+filedir+'/'+filename+'_'+Procs[0]+'.root', 'RECREATE')
for h in hw:
    h.SetName(h.GetTitle().replace('_prompt',''))
    h.Write()
pfilet = ROOT.TFile(plotDir+filedir+'/'+filename+'_'+Procs[1]+'.root', 'RECREATE')
for h in ht:
    h.SetName(h.GetTitle().replace('_prompt',''))
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
    h.SetName(h.GetTitle().replace('_prompt',''))
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
    h.SetName(h.GetTitle().replace('_nonprompt',''))
    h.Write()


