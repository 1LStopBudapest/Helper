import ROOT
import os, sys

from Style import *

            
def StackHists(files, samplelist, var, dir, cut, islogy=True, scaleOption='Lumiscaling', canvasX=1400, canvasY=800):
    outputdirpath = os.path.join(dir, "RegionPlots", cut)
    if not os.path.exists(outputdirpath):
        if os.path.exists(os.path.join(dir,"RegionPlots")):
            os.mkdir(outputdirpath)
        else:
            os.makedirs(outputdirpath)
    hs=[]
    for i, f in enumerate(files,0):
        hs.append(f.Get(var+'_'+samplelist[i]))

    hStack_MC = ROOT.THStack("hStack_MC","hStack_MC")
    hMC = hs[0].Clone("TotalMC")
    leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
    leg.SetNColumns(3)
    for i, h in enumerate(hs, 0):
        if i!=len(hs)-1:
            hStack_MC.Add(h)
            h.SetFillColor(getColor(samplelist[i]))
            h.SetLineColor(getColor(samplelist[i]))
            leg.AddEntry(h, getLegendTitle(samplelist[i]) ,"f")
            if i!=0:
                hMC.Add(h)
                
    leg.AddEntry(hs[-1], getLegendTitle('Data') ,"pe")
    styleData(hs[-1], islogy)
    mVal = hs[-1].GetBinContent(hs[-1].GetMaximumBin()) if hs[-1].GetBinContent(hs[-1].GetMaximumBin())>hMC.GetBinContent(hMC.GetMaximumBin()) else hMC.GetBinContent(hMC.GetMaximumBin())
    maxRange = mVal * 100 if islogy else mVal * 1.5
    minRange = 0.0001 if islogy else 0.0
    hs[-1].GetYaxis().SetRangeUser(minRange , maxRange*1.5)
    
    hRatio = getHistratio(hs[-1], hMC, "DataMC", var)
    hRatioFrame = getHistratioframe(hRatio)

    ROOT.gStyle.SetErrorX(0)
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas('c', '', canvasX, canvasY)
    p1 = ROOT.TPad("p1", "p1", 0, 0.3, 1, 1.0)
    p1.SetBottomMargin(0)
    p1.Draw()            
    p1.cd()
    hs[-1].Draw("PE")
    hStack_MC.Draw("histsame")
    hs[-1].DrawCopy("PEsame")
    leg.Draw("SAME")
    if islogy:ROOT.gPad.SetLogy()
    c.cd()
    p2 = ROOT.TPad("p2", "p2", 0, 0.01, 1, 0.3)
    p2.SetTopMargin(0)
    p2.SetBottomMargin(0.2)
    p2.Draw()
    p2.cd()
    hRatio.SetMarkerSize(0.6)
    hRatio.Draw("PE")
    hRatioFrame.Draw("HISTsame")
    c.SaveAs(outputdirpath+"/"+var+".png")
    c.Close()
