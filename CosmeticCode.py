
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
    'MuPt_loose'    : 'Loose #mu p_{T} [GeV]',
    'MuPt_tight'    : 'Tight #mu p_{T} [GeV]',
    'ElePt_loose'   : 'Loose e p_{T} [GeV]',
    'ElePt_tight'   : 'Tight e p_{T} [GeV]',
    'gStop_dx' : 'genStop x [mm]',
    'gStop_dy' : 'genStop y [mm]',
    'gStop_dz' : 'genStop z [cm]',
    'gVtx_dx' : 'genVtx x [mm]',
    'gVtx_dy' : 'genVtx y [mm]',
    'gVtx_dz' : 'genVtx z [cm]',
    'gStop_gVtx_dx' : 'd_{x}(genStop,genVtx) [#mum]',
    'gStop_gVtx_dy' : 'd_{y}(genStop,genVtx) [#mum]',
    'gStop_gVtx_dz' : 'd_{z}(genStop,genVtx) [#mum]',
    'gStop_gAStop_dx' : 'd_{x}(genStop,genAntiStop) [#mum]',
    'gStop_gAStop_dy' : 'd_{y}(genStop,genAntiStop) [#mum]',
    'gStop_gAStop_dz' : 'd_{z}(genStop,genAntiStop) [#mum]',
    'gLSP_gStop_dx' : 'd_{x}(genStop,genLSP) [cm]',
    'gLSP_gStop_dy' : 'd_{y}(genStop,genLSP) [cm]',
    'gLSP_gStop_dz' : 'd_{z}(genStop,genLSP) [cm]',
    'PV_gVtx_dx' : 'd_{x}(PV,genVtx) [mm]',
    'PV_gVtx_dy' : 'd_{y}(PV,genVtx) [mm]',
    'PV_gVtx_dz' : 'd_{z}(PV,genVtx) [mm]',
    'PV_gLSP_dx' : 'd_{x}(PV,genLSP) [cm]',
    'PV_gLSP_dy' : 'd_{y}(PV,genLSP) [cm]',
    'PV_gLSP_dz' : 'd_{z}(PV,genLSP) [cm]',
    'gStop_gVtx_2D': 'd_{xy}(genStop,genVtx) [#mum]',
    'gStop_gAStop_2D' : 'd_{xy}(genStop,genAntiStop) [#mum]',
    'gLSP_gStop_2D' : 'd_{xy}(genLSP,genStop) [cm]',
    'PV_gVtx_2D' : 'd_{xy}(PV,genVtx) [mm]',
    'PV_gLSP_2D' : 'd_{xy}(PV,genLSP) [cm]',
    'gStop_gVtx_3D': 'd_{xyz}(genStop,genVtx) [#mum]',
    'gStop_gAStop_3D' : 'd_{xyz}(genStop,genAntiStop) [#mum]',
    'gLSP_gStop_3D' : 'd_{xyz}(genLSP,genStop) [cm]',
    'PV_gVtx_3D' : 'd_{xyz}(PV,genVtx) [mm]',
    'PV_gLSP_3D' : 'd_{xyz}(PV,genLSP) [cm]',
    'gVtx_gLSP_dx' : 'd_{x}(genVtx,genLSP) [cm]',
    'gVtx_gLSP_dy' : 'd_{y}(genVtx,genLSP) [cm]',
    'gVtx_gLSP_dz' : 'd_{z}(genVtx,genLSP) [cm]',
    'gVtx_gLSP_2D' : 'd_{xy}(genVtx,genLSP) [cm]',
    'gVtx_gLSP_3D' : 'd_{xyz}(genVtx,genLSP) [cm]',
    'SV_gLSP_dx' : 'd_{x}(SV,genLSP) [cm]',
    'SV_gLSP_dy' : 'd_{y}(SV,genLSP) [cm]',
    'SV_gLSP_dz' : 'd_{z}(SV,genLSP) [cm]',
    'SV_gLSP_2D' : 'd_{xy}(SV,genLSP) [cm]',
    'SV_gLSP_3D' : 'd_{xyz}(SV,genLSP) [cm]',
    'Ntracks' : 'N_{tracks}',
    'nSV' : 'N_{SV}',
    'Ntracks' : 'N_{tracks}',
    'SVdxy' : 'SV_{dxy} [cm]',
    'SVdxySig' : 'S_{2D}',
    'SVmass' : 'SV_{mass} [GeV]',
    'SVdlenSig' : 'S_{3D}',
    'SVpAngle' : 'cos(PV-SV, SVp)',
    'SVpT' : 'p_{T}(SV) [Gev]',
    'SVdR' : '#Delta R(SV, jet)',
    'SV_gVtx_dx' : 'd_{x}(SV,genVtx) [cm]',
    'SV_gVtx_dy' : 'd_{y}(SV,genVtx) [cm]',
    'SV_gVtx_dz' : 'd_{z}(SV,genVtx) [cm]',
    'SV_gVtx_2D' : 'd_{xy}(SV,genVtx) [cm]',
    'SV_gVtx_3D' : 'd_{xyz}(SV,genVtx) [cm]',
    'SV_gB_dx' : 'd_{x}(SV,genB) [cm]',
    'SV_gB_dy' : 'd_{y}(SV,genB) [cm]',
    'SV_gB_dz' : 'd_{z}(SV,genB) [cm]',
    'SV_gB_2D' : 'd_{xy}(SV,genB) [cm]',
    'SV_gB_3D' : 'd_{xyz}(SV,genB) [cm]',
    'gB_dx' : 'genB x [cm]',
    'gB_dy' : 'genB y [cm]',
    'gB_dz' : 'genB z [cm]',
    'gB_gLSP_dx' : 'd_{x}(genB,genLSP) [cm]',
    'gB_gLSP_dy' : 'd_{y}(genB,genLSP) [cm]',
    'gB_gLSP_dz' : 'd_{z}(genB,genLSP) [cm]',
    'gB_gLSP_2D' : 'd_{xy}(genB,genLSP) [cm]',
    'gB_gLSP_3D' : 'd_{xyz}(genB,genLSP) [cm]',
    'SV_dx' : 'SV x [cm]',
    'SV_dy' : 'SV y [cm]',
    'SV_dz' : 'SV z [cm]',
    'PV_dx' : 'PV x [cm]',
    'PV_dy' : 'PV y [cm]',
    'PV_dz' : 'PV z [cm]',
    'SV_PV_dx' : 'd_{x}(SV,PV) [cm]',
    'SV_PV_dy' : 'd_{y}(SV,PV) [cm]',
    'SV_PV_dz' : 'd_{z}(SV,PV) [cm]',
    'SV_PV_2D' : 'd_{xy}(SV,PV) [cm]',
    'SV_PV_3D' : 'd_{xyz}(SV,PV) [cm]',
    'dec_dx' : 'L(gStop) x [cm]',
    'dec_dy' : 'L(gStop) y [cm]',
    'dec_dz' : 'L(gStop) z [cm]',
    'dec_2D' : 'L(gStop) xy [cm]',
    'dec_3D' : 'L(gStop) xyz [cm]',
    'PV_gStop_dx' : 'd_{x}(PV,gStop) [cm]',
    'PV_gStop_dy' : 'd_{y}(PV,gStop) [cm]',
    'PV_gStop_dz' : 'd_{z}(PV,gStop) [cm]',
    'PV_gStop_2D' : 'd_{xy}(PV,gStop) [cm]',
    'PV_gStop_3D' : 'd_{xyz}(PV,gStop) [cm]',
    'SV_gStop_dx' : 'd_{x}(SV,gStop) [cm]',
    'SV_gStop_dy' : 'd_{y}(SV,gStop) [cm]',
    'SV_gStop_dz' : 'd_{z}(SV,gStop) [cm]',
    'SV_gStop_2D' : 'd_{xy}(SV,gStop) [cm]',
    'SV_gStop_3D' : 'd_{xyz}(SV,gStop) [cm]',

}

colDict = {
    'Signal' : ROOT.kBlack,
    'TTSingleLep_pow'  : ROOT.kAzure+2,
    'TTLep_pow' : ROOT.kAzure+1,
    'ST' : 7,
    'WJetsToLNu' : 8,
    'ZJetsToNuNu' : ROOT.kOrange-3,
    'DYJetsToLL' : ROOT.kMagenta-6,
    'QCD' : ROOT.kMagenta+3,
    'TTV' : ROOT.kAzure-7,
    'VV' : ROOT.kOrange,
    'Data': ROOT.kBlack,
    'UL17V9_Full99mm' : ROOT.kAzure+2,
    'TTToSemiLeptonic' : 8,
    'TTTo2L2Nu' : ROOT.kOrange,

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
    'fastfull' : ['FastSim', 'FullSim'],
    'IVF' : ['Before IVF cut', 'After IVF cut']
}

LegendTitleDict = {
    'TTSingleLep_pow' : 't#bar{t}_1l',
    'TTLep_pow' : 't#bar{t}_2l',
    'ST' : 'Single Top',
    'WJetsToLNu' : 'W + Jets',
    'WJetsToLNu_comb' : 'W + Jets',
    'ZJetsToNuNu' : 'Z(#nu#nu) + Jets',
    'DYJetsToLL' : 'DY + Jets',
    'QCD' : 'QCD', 
    'TTV' : 't#bar{t}X',
    'VV' : 'Diboson',
    'Data': 'Data',
    'DoubleMuon_Data': 'Data(Double#mu)',
    'SingleMuon_Data': 'Data(Single#mu)',
    'UL17V9_Full99mm' : 'UL17V9_Full99mm',
    'TTToSemiLeptonic' : 'TTToSemiLeptonic',
    'TTTo2L2Nu' : 'TTTo2L2Nu', 
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
    #return XlabelDict[title] if title in XlabelDict.keys() else 'x axis'
    return XlabelDict[title] if title in XlabelDict.keys() else title

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
    elif 'IVF' in comp:
        return RatioLegendDict['IVF']
    else:
        return [h1.GetName().strip(h1.GetTitle()+"_"), h2.GetName().strip(h2.GetTitle()+"_")]

def getLegendTitle(sample):
    return LegendTitleDict[sample] if sample in LegendTitleDict.keys() else 'other'

def getTrigColor(trig):
        return TrigcolDict[trig] if trig in TrigcolDict.keys() else ROOT.kBlack
