import ROOT
import os, sys
import numpy as np
import math

from Style import *

def Plot1D(h, dir, drawOption="hist", islogy=False, canvasX=600, canvasY=800, Xtitle = "auto-format", Ytitle = "auto-format"):
    hname = h.GetName()
    htitle = h.GetTitle()
    sname = hname.replace(htitle+"_", "")
    outputdirpath = os.path.join(dir,"1DPlots/final",sname)
    if not os.path.exists(outputdirpath):
        os.makedirs(outputdirpath)

    leg = ROOT.TLegend(0.5, 0.85, 0.9, 0.9)
    leg.AddEntry(h, sname ,"l")

    style1D(h, islogy, Ytitle, Xtitle)
    
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

            
def StackHists(files, samplelist, var, dir, cut, islogy=True, scaleOption='Lumiscaling', canvasX=600, canvasY=800):
    outputdirpath = os.path.join(dir,"StackPlots",cut)
    if not os.path.exists(outputdirpath):
        if os.path.exists(os.path.join(dir,"StackPlots")):
            os.mkdir(outputdirpath)
        else:
            os.makedirs(outputdirpath)
    hs=[]
    for i, f in enumerate(files,0):
        hs.append(f.Get(var+'_'+samplelist[i]))
        
    hs_MC = hs[:-1]#assuming last one is from data
    if 'Area' in scaleOption or 'Unit' in scaleOption:
        MCtot = 0.0
        for h in hs_MC:
            MCtot = MCtot + h.Integral()
        scale = hs[-1].Integral()/MCtot
        for h in hs_MC:
            h.Scale(scale)
                
    hStack_MC = ROOT.THStack("hStack_MC","hStack_MC")
    hMC = hs_MC[0].Clone("TotalMC")
    leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
    leg.SetNColumns(3)
    for i, h in enumerate(hs_MC, 0):
        hStack_MC.Add(h)
        h.SetFillColor(getColor(samplelist[i]))
        h.SetLineColor(getColor(samplelist[i]))
        leg.AddEntry(h, getLegendTitle(samplelist[i]) ,"f")
        if i!=0:
            hMC.Add(h)
                
    leg.AddEntry(hs[-1], getLegendTitle('Data') ,"pe")
    styleData(hs[-1], islogy)
    
    print 'total MC: ', hMC.Integral(), '  data: ', hs[-1].Integral()
        

    mVal = hs[-1].GetBinContent(hs[-1].GetMaximumBin()) if hs[-1].GetBinContent(hs[-1].GetMaximumBin())>hMC.GetBinContent(hMC.GetMaximumBin()) else hMC.GetBinContent(hMC.GetMaximumBin())
    maxRange = mVal * 100 if islogy else mVal * 1.5
    #minRange = 0.0001 if islogy else 0.0
    minRange = 0.1 if islogy else 0.0
    hs[-1].GetYaxis().SetRangeUser(minRange , maxRange*1.5)
    
    hRatio = getHistratio(hs[-1], hMC, "DataMC", var)
    hRatioFrame = getHistratioframe(hRatio)

    ROOT.gStyle.SetErrorX(0);
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas('c', '', 600, 800)
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


# ROC plotting
def plotROC(signal_pass, signal_total, bk_pass, bk_total, colors, legTitle, path, name, samplename, BKsamplename, xmin = 0, ymin = 0, xmax = 1, ymax = 1, title = "", ptcut = -1, xtitle = "Average signal efficiency", ytitle ="Average BK rejection (1-eff)", cmssimwip = True):
    # signal_pass, signal_total: nominator and denominator TH1F's, from which signal eff is calculated
    # bk_pass, bk_total: same for BK rejection
    # colors: array of colors for each point on ROC
    # legTitle: array of legend names for points
    # path, name: file is named <path>/name.png. Leave name empty ("") to auto-format with samplename and BKsamplename
    # title: the title of the figure. Leave empty ("") to auto-format 
    # samplename, BKsamplename, ptcut: Auto-formatted uses this name of the signal sample (string), the BK samplename (string), and stating a ptcut (int), if any
    # xtitle, ytitle: lables of axes
    # xmin, ymin, xmax, ymax: ranges of axes
    # cmssimwip: if true, also prints "CMS Simulation Work In Progress" on figure



    if(len(signal_pass) != len(bk_pass) or len(signal_pass) < len(signal_total) or len(bk_pass) < len(bk_total) or len(colors) < len(signal_pass)):
        print 'Error in plotROC: arrays are incompatible'
        return -1
    

    effs = []
    Deffs = []

    for i in range(len(signal_pass)):
        Nbins = signal_pass[i].GetNbinsX()
        bineffs = []
        Dbineffs = []
        for j in range (Nbins):
            num = signal_pass[i].GetBinContent(j+1)
            den = signal_total[i].GetBinContent(j+1) 
            if(den == 0 or num == 0):
                continue
            eff = num / den 
            if(eff > 1):
                print 'Warning in ROC: eff > 1'

            Dden = signal_total[i].GetBinError(j+1)
            Dnum = signal_pass[i].GetBinError(j+1)
            Deff = eff*math.sqrt((Dnum/num)**2 + (Dden/den)**2)

            bineffs.append(eff)
            Dbineffs.append(Deff)
        
        # take average, and take average corrected empirical deviation as errorbars:
        aveff = sum(bineffs)/len(bineffs)
        devi = 0
        for j in range(len(bineffs)):
            devi += (bineffs[j] - aveff)**2
        devi /= len(bineffs)*(len(bineffs)-1)
        devi = math.sqrt(devi)

        effs.append(aveff)
        Deffs.append(devi)


    rejs = []
    Drejs = []

    for i in range(len(bk_pass)):
        Nbins = bk_pass[i].GetNbinsX()
        bineffs = []
        Dbineffs = []
        for j in range (Nbins):
            num = bk_pass[i].GetBinContent(j+1)
            den = bk_total[i].GetBinContent(j+1) 
            if(den == 0):
                continue
            eff = num / den 
            if(eff > 1):
                print 'Warning in ROC: eff > 1'

            Dden = bk_total[i].GetBinError(j+1)
            Dnum = bk_pass[i].GetBinError(j+1)
            Deff = eff*math.sqrt((Dnum/num)**2 + (Dden/den)**2)

            bineffs.append(eff)
            Dbineffs.append(Deff)
        
        # take average, and take average corrected empirical deviation as errorbars:
        aveff = sum(bineffs)/len(bineffs)
        devi = 0
        for j in range(len(bineffs)):
            devi += (bineffs[j] - aveff)**2
        devi /= len(bineffs)*(len(bineffs)-1)
        devi = math.sqrt(devi)

        rejs.append(aveff)
        Drejs.append(devi)


    if(title == ""):
        if(-1 != ptcut):
            title = "#splitline{ROC for signal: "+samplename+"}{BK: "+BKsamplename+", pt > "+str(ptcut)+" GeV}"
        else:
            title = "#splitline{ROC for signal: "+samplename+"}{BK: "+BKsamplename+"}"

    roc = {}
    for i in range(len(effs)):
        x = [effs[i]]
        y = [rejs[i]]
        Dx = [Deffs[i]]
        Dy = [Drejs[i]]
        roc[i] = ROOT.TGraphAsymmErrors(1,np.array(x),np.array(y),np.array(Dx),np.array(Dx),np.array(Dy),np.array(Dy))
    
        roc[i].SetLineColor(colors[i])
        roc[i].SetLineWidth(2)
        roc[i].SetMarkerSize(0.8)
        roc[i].SetMarkerStyle(20)
        roc[i].SetMarkerColor(colors[i])
        roc[i].SetTitle(title)

    leg = ROOT.TLegend(0.5, 0.1, 0.9, 0.3)
    for i in range(len(roc)):    
        leg.AddEntry(roc[i], legTitle[i] ,"p")

    c = ROOT.TCanvas('c', 'Title', 600, 800)

    c.SetGrid()
    fr = c.DrawFrame(xmin,ymin,xmax,ymax)

    fr.SetTitle(title)
    fr.SetTitleSize(0.01)

    fr.GetYaxis().SetTitle(ytitle)
    fr.GetYaxis().SetTitleSize(0.04)
    fr.GetYaxis().SetTitleOffset(1.15)
    fr.GetYaxis().SetLabelSize(0.03)
    fr.GetXaxis().SetTitle(xtitle)
    fr.GetXaxis().SetTitleSize(0.04)
    fr.GetXaxis().SetTitleOffset(0.9)
    fr.GetXaxis().SetLabelSize(0.03)



    if(cmssimwip):
        tex = ROOT.TLatex(0.43,0.875,"CMS Simulation work in progress")
        tex.SetNDC()
        tex.SetTextFont(42)
        tex.SetTextSize(0.035)
        tex.SetLineWidth(2)
        tex.Draw()

    for i in range(len(roc)):
        roc[i].Draw("P,SAME")
    leg.Draw("SAME")


    if(name == ""):
        name = "ROCfigure_Sig_"+samplename+"_BK_"+BKsamplename
        if(ptcut != -1):
            name += "_pt"+str(ptcut)

    c.SaveAs(path+"/"+name+".png")
    c.Close()
    return 0

    
