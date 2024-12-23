import ROOT

from CosmeticCode import *

def style1D(h, islogy, Ytitle="auto-format", Xtitle = "auto-format"):
    hname = h.GetName()
    htitle = h.GetTitle()
    samplename = hname.replace(htitle+"_", "")

    if(Xtitle == "auto-format"):
        auto_xt = h.GetXaxis().GetTitle()
        if(auto_xt == ""):
            Xtitle = getXTitle(htitle)
        else:
            Xtitle = auto_xt
    if(Ytitle == "auto-format"):
        auto_yt = h.GetYaxis().GetTitle()
        if(auto_yt == ""):
            Ytitle = "Number of Events"
        else:
            Ytitle = auto_yt
    maxRange = h.GetBinContent(h.GetMaximumBin())
    minRange = 0.1 if islogy else 0.0
    h.SetTitle("PostVFP/Displaced, before IVF cut")
    h.GetYaxis().SetRangeUser(minRange , maxRange*1.5)
    h.GetYaxis().SetTitle(Ytitle)
    h.GetYaxis().SetTitleSize(0.035)
    h.GetYaxis().SetTitleOffset(1.2)
    h.GetYaxis().SetLabelSize(0.03)
    h.GetXaxis().SetTitle(Xtitle)
    h.GetXaxis().SetTitleSize(0.04)
    h.GetXaxis().SetTitleOffset(0.8)
    h.GetXaxis().SetLabelSize(0.04)
    h.SetLineColor(getColor(samplename))
    h.SetLineWidth(2)
    h.SetStats(1)


def styleData(h, islogy, Ytitle="Events"):
    h.SetTitle("")
    h.GetYaxis().SetTitle(Ytitle)
    h.GetYaxis().SetTitleSize(0.035)
    h.GetYaxis().SetTitleOffset(1.2)
    h.GetYaxis().SetLabelSize(0.03)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20);
    h.SetMarkerColor(ROOT.kBlack);
    h.SetMarkerSize(0.5);
    h.SetStats(0)

    
def styleh2(h1, h2, islogy):
    hname = h2.GetName()
    htitle = h2.GetTitle()
    samplename = hname.replace(htitle+"_", "")
    h2.SetLineColor(getColor(samplename))
    h2.SetLineWidth(2)
    h2.SetLineStyle(2)
    maxRange = h1.GetBinContent(h1.GetMaximumBin()) if h1.GetBinContent(h1.GetMaximumBin())>h2.GetBinContent(h2.GetMaximumBin()) else h2.GetBinContent(h2.GetMaximumBin())
    minRange = 0.0001 if islogy else 0.0
    h1.GetYaxis().SetRangeUser(minRange , maxRange*1.5)


def getHistratio(h1, h2, comparetype, title):
    hRatio = h1.Clone("Ratio")
    hRatio.Divide(h2)
    hRatio.GetYaxis().SetTitle(getRatioTitle(comparetype))
    hRatio.GetYaxis().SetRangeUser(0,2)
    hRatio.SetTitle("")
    hRatio.SetStats(0)
    hRatio.SetLineColor(ROOT.kRed)
    hRatio.GetYaxis().SetTitleSize(0.08)
    hRatio.GetYaxis().SetTitleOffset(0.5)
    hRatio.GetYaxis().SetLabelSize(0.07)
    xtitle = getXTitle(title)
    hRatio.GetXaxis().SetTitle(xtitle)
    hRatio.GetXaxis().SetTitleSize(0.1)
    hRatio.GetXaxis().SetTitleOffset(0.9)
    hRatio.GetXaxis().SetLabelSize(0.07)
    return hRatio

def getRatioHist(hnum, hden, name, comparetype, Xtitle, ymax, title=''):
    hRatio = hnum.Clone(name)
    hRatio.Divide(hden)
    hRatio.GetYaxis().SetTitle(getRatioTitle(comparetype))
    hRatio.GetYaxis().SetRangeUser(0, ymax)
    hRatio.SetStats(0)
    hRatio.SetLineColor(ROOT.kBlack)
    if not title:
        hRatio.SetTitle(comparetype)
    else:
        hRatio.SetTitle(title)
    hRatio.GetYaxis().SetTitleSize(0.06)
    hRatio.GetYaxis().SetTitleOffset(0.6)
    hRatio.GetYaxis().SetLabelSize(0.04)
    xtitle = getXTitle(Xtitle)
    hRatio.GetXaxis().SetTitle(xtitle)
    hRatio.GetXaxis().SetTitleSize(0.06)
    hRatio.GetXaxis().SetTitleOffset(0.7)
    hRatio.GetXaxis().SetLabelSize(0.04)
    return hRatio

def getHistratioframe(hRatio):
    hRatioFrame = hRatio.Clone("RatioFrame")
    for b in range(1, hRatioFrame.GetNbinsX() + 1):
        hRatioFrame.SetBinContent(b, 1.0)
    hRatioFrame.SetLineStyle(2)
    hRatioFrame.SetLineWidth(2)
    hRatioFrame.SetLineColor(ROOT.kGreen)
    return hRatioFrame
