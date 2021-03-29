
import ROOT

XlabelDict = {

    'MET' : 'p^{miss}_{T} [GeV]',
    'HT'  : 'H_{T} [GeV]',
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
    'LepMT' : 'M_{T}(l, p^{miss}_{T})[GeV]',
    'CT1' : 'C_{T1} [GeV]',
    'CT2' : 'C_{T2} [GeV]',
    'GenMuonpt' : 'Gen #mu p_{T}[GeV]',
    'GenElept' : 'Gen e p_{T}[GeV]',
    'GenBpt_fstop' : 'Gen b p_{T}[GeV]',
    'GenBpt_istop' : 'Gen b p_{T}[GeV]',
    'GenStoppt' : 'Gen #tilde{t} p_{T}[GeV]',
    'GenLSPpt' : 'Gen #tilde{#chi_{1}^{0}} p_{T}[GeV]',
    'GenBpt' : 'Gen b p_{T}[GeV]',
    'GenBjetpt' : 'Gen b-jet p_{T}[GeV]',
    'NGenBjets' : 'N_{gen b-jet}',
    'MuondxyErr' : '#mu d_{xy}Error[cm]',
    'MuondzErr' : '#mu d_{z}Error[cm]',
    'MuondxySig' : '#mu d_{xy}Sig',
    'MuondzSig' : '#mu d_{z}Sig',
    'EledxyErr' : 'e d_{xy}[cm]Error',
    'EledzErr' : 'e d_{z}[cm]Error',
    'EledxySig' : 'e d_{xy}Sig',
    'EledzSig' : 'e d_{z}Sig',
    'Leppt'   : 'p_{T}(l) [GeV]',
    'Mupt'    : 'p_{T}(#mu)',
    'Elept'   : 'p_{T}(e)',
    'LepPt_loose'   : 'p_{T}(loose l) [GeV]',
    'LepPt_tight'   : 'p_{T}(tight l) [GeV]',
    'MuPt_loose'    : 'Loose #mu p_{T}',
    'MuPt_tight'    : 'Tight #mu p_{T}',
    'ElePt_loose'   : 'Loose e p_{T}',
    'ElePt_tight'   : 'Tight e p_{T}',
    'ISRJetEta' : 'ISR Jet #eta',
    'BjetPt' : 'b jet p_{T} [GeV]',
    '2ndJetPt' : '2nd jet p_{T} [GeV]',
    '2ndJetEta' : '2nd jet #eta',
    '3rdJetPt' : '3rd jet p_{T} [GeV]',
    '3rdJetEta' : '3rd jet #eta',
    'JetPt' : 'Jet p_{T} [GeV]',
    'JetEta' : 'Jet #eta',
    'DeltaPhi_Jets' : '#Delta#phi(1st jet, 2nd jet)',
    'DeltaPhi_Jets60' : '#Delta#phi(1st jet, 2nd jet > 60 GeV)',
    '1stBjetPt' : '1st b jet p_{T} [GeV]',
    '1stBjetEta' : '1st b jet #eta',
    'JetPhi' : 'Jet #phi',

}

colDict = {
    'Signal' : ROOT.kBlack,
    'TTSingleLep_pow'  :  ROOT.kBlue+3,
    'TTLep_pow' : ROOT.kYellow,
    'ST' : 29,
    'WJetsToLNu' : ROOT.kSpring,
    'ZJetsToNuNu' : ROOT.kOrange-3,
    'DYJetsToLL' : ROOT.kViolet-4,
    'QCD' : ROOT.kMagenta+3,
    'TTV' : ROOT.kCyan-9,
    'VV' : ROOT.kGreen+3,
    'Data': ROOT.kBlack,

}

TrigcolDict = {
    'HLT_PFMET90_PFMHT90_IDTight' : ROOT.kYellow,
    'HLT_PFMET100_PFMHT100_IDTight' : ROOT.kViolet,
    'HLT_PFMET110_PFMHT110_IDTight' : ROOT.kGreen,
    'HLT_PFMET120_PFMHT120_IDTight' : ROOT.kRed,
    'HLT_MET_Inclusive' : ROOT.kBlue,

}

RatioTitleDict = {
    'fastfull' : 'fast / full',
    'DataMC' : 'Data/MC',
    'FakeRate' : '#epsilon_{TL}'
}

RatioLegendDict = {
'fastfull' : ['FastSim', 'FullSim']

}

LegendTitleDict = {
    'TTSingleLep_pow' : 't#bar{t}_1l',
    'TTLep_pow' : 't#bar{t}_2l',
    'ST' : 'Single Top',
    'WJetsToLNu' : 'W + Jets',
    'ZJetsToNuNu' : 'Z(#nu#nu) + Jets',
    'DYJetsToLL' : 'DY + Jets',
    'QCD' : 'QCD', 
    'TTV' : 't#bar{t}X',
    'VV' : 'Diboson',
    'Data': 'Data',
    'T2tt_500_420' : '#tilde{t}_{1} #rightarrow bff\'#tilde{#chi}_{0}^{1}(500,420)',
    'T2tt_500_490' : '#tilde{t}_{1} #rightarrow bff\'#tilde{#chi}_{0}^{1}(500,490)',
    }

vidNestedWPBitMapNamingList = [
    'GsfEleMissingHitsCut',
    'GsfEleConversionVetoCut',
    'GsfEleRelPFIsoScaledCut',
    'GsfEleEInverseMinusPInverseCut',
    'GsfEleHadronicOverEMEnergyScaledCut',
    'GsfEleFull5x5SigmaIEtaIEtaCut',
    'GsfEleDPhiInCut',
    'GsfEleDEtaInSeedCut',
    'GsfEleSCEtaMultiRangeCut',
    'MinPtCut'
]

def getXTitle(title):
    return XlabelDict[title] if title in XlabelDict.keys() else 'x axis'

def getColor(sample):
    if "Stop" in sample:
        return colDict['Signal'] if 'Signal' in colDict.keys() else ROOT.kBlack
    else:
        return colDict[sample] if sample in colDict.keys() else ROOT.kBlack

def getRatioTitle(comp):
    return RatioTitleDict[comp] if comp in RatioTitleDict.keys() else 'Ratio'

def getRatioLegendTitle(h1, h2, comp):
    if 'fastfull' in comp:
        return RatioLegendDict['fastfull']
    else:
        return [h1.GetName().strip(h1.GetTitle()+"_"), h2.GetName().strip(h2.GetTitle()+"_")]

def getLegendTitle(sample):
    return LegendTitleDict[sample] if sample in LegendTitleDict.keys() else 'other'

def getTrigColor(trig):
        return TrigcolDict[trig] if trig in TrigcolDict.keys() else ROOT.kBlack
