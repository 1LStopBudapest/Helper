import ROOT
import os, sys

from Style import *

            
def StackHists(files, samplelist, var, dir, cut, islogy=True, scaleOption='Lumiscaling', canvasX=1600, canvasY=600):
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
    hMC = hs[0].Clone("TotalMC")#assuming fist sample is one of SM MC
    hMC_dby = hs[0].Clone("dbyMC")#assuming fist sample is one of SM MC
    hsig=[]
    sigleg=[]
    hData=[]
    leg = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    leg.SetNColumns(3)
    for i, h in enumerate(hs, 0):
        if 'Sig' in samplelist[i]:
            hsig.append(h)
            h.SetLineColor(len(hs)-i)
            h.SetLineWidth(2)
            sigleg.append(samplelist[i])
        elif 'Data' in samplelist[i]:
            hData.append(h)
        else:
            hStack_MC.Add(h)
            h.SetFillColor(getColor(samplelist[i]))
            h.SetLineColor(getColor(samplelist[i]))
            leg.AddEntry(h, getLegendTitle(samplelist[i]) ,"f")
            if i!=0:
                hMC.Add(h)

    
    ROOT.gStyle.SetErrorX(0)
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas('c', '', canvasX, canvasY)

    if len(hData):
        leg.AddEntry(hData[0], getLegendTitle('Data') ,"pe")
        styleData(hData[0], islogy)
        mVal = hData[0].GetBinContent(hData[0].GetMaximumBin()) if hData[0].GetBinContent(hData[0].GetMaximumBin())>hMC.GetBinContent(hMC.GetMaximumBin()) else hMC.GetBinContent(hMC.GetMaximumBin())
        maxRange = mVal * 100 if islogy else mVal * 1.5
        minRange = 0.01 if islogy else 0.0
        hData[0].GetYaxis().SetRangeUser(minRange , maxRange*1.5)
        
        hRatio = getHistratio(hData[0], hMC, "DataMC", var)
        hRatioFrame = getHistratioframe(hRatio)
        
        p1 = ROOT.TPad("p1", "p1", 0, 0.3, 1, 1.0)
        p1.SetBottomMargin(0)
        p1.Draw()            
        p1.cd()
        hData[0].Draw("PE")
        hStack_MC.Draw("histsame")
        hData[0].DrawCopy("PEsame")
        for i in range(len(hsig)):
            leg.AddEntry(hsig[i], sigleg[i] ,"l")
            hsig[i].Draw('histsame')
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


    else:
        for b in range(hMC_dby.GetNbinsX()):
            hMC_dby.SetBinContent(b+1, 0)
            hMC_dby.SetBinError(b+1, 0)
        hMC_dby.SetTitle('')
        mVal = hMC.GetBinContent(hMC.GetMaximumBin())
        maxRange = mVal * 100 if islogy else mVal * 1.5
        minRange = 0.01 if islogy else 0.0
        hMC_dby.GetYaxis().SetRangeUser(minRange , maxRange*1.5)
        hMC_dby.Draw()
        hStack_MC.Draw("histsame")
        for i in range(len(hsig)):
            leg.AddEntry(hsig[i], sigleg[i] ,"l")
            hsig[i].Draw('histsame')
        leg.Draw("SAME")
        if islogy:ROOT.gPad.SetLogy()



    c.SaveAs(outputdirpath+"/"+var+".png")
    c.Close()
