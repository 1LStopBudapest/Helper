
import ROOT

XlabelDict = {

    'MET' : 'MET (GeV)',
    'HT'  : 'HT (GeV)',
    'ISRJetPt' : 'ISR Jet p_{T} [GeV]',
    'Njet20' : 'N_{jets}(>20 GeV)',
    'Njet30' : 'N_{jets}(>30 GeV)',
    'Nbjet30' : 'N_{bjets}(>30 GeV)',
    'Nbjet20' : 'N_{bjets}(>20 GeV)',
    'jet1pt' : 'Leading jet p_{T} [GeV]',
    'jet2pt' : '2nd leading jet p_{T} [GeV]',
    'Muonpt' : '#mu p_{T}[GeV]',
    'Muondxy' : '#mu d_{xy}[cm]',
    'Muondz' : '#mu d_{z}[cm]',
    'Elept' : 'e p_{T}[GeV]',
    'Eledxy' : 'e d_{xy}[cm]',
    'Eledz' : 'e d_{z}[cm]',
    'Nmu'   : 'N_{#mu}',
    'Ne'  :  'N_{e}',
    'LepMT' : 'M_{T}(l, met)[GeV]',
    'CT1' : 'CT1 [GeV]',
    'CT2' : 'CT2 [GeV]',
    'GenMuonpt' : 'Gen #mu p_{T}[GeV]',
    'GenElept' : 'Gen e p_{T}[GeV]',
    'GenBpt_fstop' : 'Gen b p_{T}[GeV]',
    'GenBpt_istop' : 'Gen b p_{T}[GeV]',
    'GenStoppt' : 'Gen #tilde{t} p_{T}[GeV]',
    'GenLSPpt' : 'Gen #tilde{#chi_{1}^{0}} p_{T}[GeV]',
    'GenBpt' : 'Gen b p_{T}[GeV]',
    'GenBjetpt' : 'Gen b-jet p_{T}[GeV]',
    'NGenBjets' : 'N_{gen b-jet}',

}

colDict = {
    'Signal' : ROOT.kBlack,
    'TTSingleLep_pow'  : ROOT.kAzure+2,
    'TTLep_pow' : ROOT.kAzure+1,
    'SingleTop' : 7,
    'WJetsToLNu' : 8,
    'ZJetsToNuNu' : ROOT.kOrange-3,
    'DYJetsToLL' : ROOT.kMagenta-6,
    'QCD' : ROOT.kMagenta+3,
    'TTX' : ROOT.kAzure-7,
    'Diboson' : ROOT.kOrange,
    'Data': ROOT.kBlack,

}

RatioTitleDict = {
    'fastfull' : 'fast / full',
    'DataMC' : 'Data/MC',

}

RatioLegendDict = {
'fastfull' : ['FastSim', 'FullSim']

}

LegendTitleDict = {
    'TTSingleLep_pow' : 't#bar{t}_1l',
    'TTLep_pow' : 't#bar{t}_2l',
    'SingleTop' : 'Single Top',
    'WJetsToLNu' : 'W + Jets',
    'ZJetsToNuNu' : 'Z(#nu#nu) + Jets',
    'DYJetsToLL' : 'DY + Jets',
    'QCD' : 'QCD', 
    'TTX' : 't#bar{t}X',
    'Diboson' : 'Diboson',
    'Data': 'Data',
    }

def getXTitle(title):
    return XlabelDict[title]

def getColor(sample):
    if "Stop" in sample:
        return colDict['Signal']
    else:
        return colDict[sample]

def getRatioTitle(comp):
    return RatioTitleDict[comp]

def getRatioLegendTitle(h1, h2, comp):
    if 'fastfull' in comp:
        return RatioLegendDict['fastfull']
    else:
        return [h1.GetName().strip(h1.GetTitle()+"_"), h2.GetName().strip(h2.GetTitle()+"_")]

def getLegendTitle(sample):
    return LegendTitleDict[sample]
