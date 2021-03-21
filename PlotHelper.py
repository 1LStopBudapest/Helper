import ROOT
import os, sys

from Style import *

def Plot1D(h, dir, drawOption="hist", islogy=False, canvasX=600, canvasY=800):
    hname = h.GetName()
    htitle = h.GetTitle()
    sname = hname.replace(htitle+"_", "")
    outputdirpath = os.path.join(dir,"1DPlots",sname)
    if not os.path.exists(outputdirpath):
        os.makedirs(outputdirpath)

    leg = ROOT.TLegend(0.5, 0.85, 0.9, 0.9)
    leg.AddEntry(h, sname ,"l")

    style1D(h, islogy)
    
    c = ROOT.TCanvas('c', '', canvasX, canvasY)
    c.cd()
    h.Draw(drawOption)
    leg.Draw("SAME")
    if islogy:ROOT.gPad.SetLogy()
    c.SaveAs(outputdirpath+"/"+htitle+".png")
    c.Close()
    
def CompareHist(h1, h2, comparetype, dir, drawOption="hist", islogy=False, scaleOption='unitscaling', canvasX=600, canvasY=800):
    hname = h1.GetName()
    htitle = h1.GetTitle()
    sname = hname.replace(htitle+"_", "")
    outputdirpath = os.path.join(dir,"RatioPlots",comparetype)
    if not os.path.exists(outputdirpath):
        if os.path.exists(os.path.join(dir,"RatioPlots")):
            os.mkdir(outputdirpath)
        else:
            os.makedirs(outputdirpath)
    if 'unit' in scaleOption:
        if h1.Integral(): h1.Scale(1/h1.Integral())
        if h2.Integral(): h2.Scale(1/h2.Integral())
    style1D(h1, islogy, "a.u.")
    styleh2(h1, h2, islogy)
    hRatio = getHistratio(h1, h2, comparetype, htitle)
    hRatioFrame = getHistratioframe(hRatio)

    leg = ROOT.TLegend(0.7, 0.75, 0.9, 0.9)
    leg.AddEntry(h1, getRatioLegendTitle(h1, h2, comparetype)[0] ,"l")
    leg.AddEntry(h2, getRatioLegendTitle(h1, h2, comparetype)[1] ,"l")
    
    c = ROOT.TCanvas('c', '', 600, 800)
    p1 = ROOT.TPad("p1", "p1", 0, 0.3, 1, 1.0)
    p1.SetBottomMargin(0) # Upper and lower plot are joined
    p1.Draw()             # Draw the upper pad: p1
    p1.cd()
    h1.Draw(drawOption+"E")
    h2.Draw(drawOption+"ESAME")
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
    c.SaveAs(outputdirpath+"/"+htitle+".png")
    c.Close()

            
def StackHists(files, samplelist, var, dir, cut, islogy=True, scaleOption='Lumiscaling', canvasX=800, canvasY=800):
    outputdirpath = os.path.join(dir,"StackPlots",cut)
    if not os.path.exists(outputdirpath):
        if os.path.exists(os.path.join(dir,"StackPlots")):
            os.mkdir(outputdirpath)
        else:
            os.makedirs(outputdirpath)
    hs=[]
    for i, f in enumerate(files,0):
        hs.append(f.Get(var+'_'+samplelist[i]))

    hStack_MC = ROOT.THStack("hStack_MC","hStack_MC")
    hMC = hs[0].Clone("TotalMC")
    hMC_dby = hs[0].Clone("dbyMC")#assuming fist sample is one of SM MC
    hsig=[]
    sigleg=[]
    hData=[]
    leg = ROOT.TLegend(0.35, 0.7, 0.87, 0.87)
    leg.SetNColumns(4)
    for i, h in enumerate(hs, 0):
        if 'T2tt' in samplelist[i]:
            hsig.append(h)
            if 'T2tt_500_420' in samplelist[i]: h.SetLineColor(ROOT.kRed)
            if 'T2tt_500_490' in samplelist[i]: h.SetLineColor(ROOT.kAzure+1)
            h.SetLineWidth(3)
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
        minRange = 0.1 if islogy else 0.0
        hData[0].GetYaxis().SetRangeUser(minRange , maxRange*1.5)
        
        hRatio = getHistratio(hData[0], hMC, "DataMC", var)
        hRatioFrame = getHistratioframe(hRatio)
        ROOT.gStyle.SetErrorX(0)
        ROOT.gStyle.SetOptStat(0)
        p1 = ROOT.TPad("p1", "p1", 0, 0.3, 1, 1.0)
        p1.SetBottomMargin(0)
        p1.Draw()            
        p1.cd()
        hData[0].SetTitle('Distribution after preselection (p_T(jet) > 30 GeV)')
        hData[0].Draw("PE")
        hStack_MC.Draw("histsame")
        hData[0].DrawCopy("PEsame")
        for i in range(len(hsig)):
            leg.AddEntry(hsig[i], sigleg[i] ,"l")
            hsig[i].Draw('histsame')
        leg.Draw("SAME")
        ROOT.gPad.SetTicks()
        ROOT.gPad.RedrawAxis()
        hData[0].Draw("sameaxis") 
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
        hMC_dby.SetTitle('Distribution after preselection (p_T(jet) > 30 GeV)')
        mVal = hMC.GetBinContent(hMC.GetMaximumBin())
        maxRange = mVal * 100 if islogy else mVal * 1.5
        minRange = 0.1 if islogy else 0.0
        hMC_dby.GetYaxis().SetRangeUser(minRange , maxRange*1.5)
        hMC_dby.Draw()
        hStack_MC.Draw("histsame")
        for i in range(len(hsig)):
            leg.AddEntry(hsig[i], sigleg[i] ,"l")
            hsig[i].Draw('histsame')
        leg.Draw("SAME")
        ROOT.gPad.SetTicks()
        ROOT.gPad.RedrawAxis()
        hMC_dby.Draw("sameaxis") 
        if islogy:ROOT.gPad.SetLogy()



    c.SaveAs(outputdirpath+"/"+var+".png")
    c.Close()
