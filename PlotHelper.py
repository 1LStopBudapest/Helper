import ROOT
import os, sys, io
import numpy as np
import math
import subprocess

from Style import *

def Plot1D(h, dir, drawOption="hist", islogy=False, canvasX=600, canvasY=800, Xtitle = "auto-format", Ytitle = "auto-format"):
    hname = h.GetName()
    htitle = h.GetTitle()
    sname = hname.replace(htitle+"_", "")
    outputdirpath = os.path.join(dir,"Test",sname)
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

def Plot1DExt(var, hext, fname, dir, drawOption="hist", islogy=False, canvasX=600, canvasY=800, Xtitle = "auto-format", Ytitle = "auto-format"):
    doplot = True
    if os.path.exists(os.path.join(dir,fname)):
        f=ROOT.TFile.Open(os.path.join(dir,fname))
    else:
        doplot = False
        print 'Root file ',os.path.join(dir,fname),' does not exist'
    if doplot:
        h=f.Get(var+'_'+hext)
        htitle = h.GetTitle()
        outputdirpath = os.path.join(dir,"Test",hext)
        if not os.path.exists(outputdirpath):
            os.makedirs(outputdirpath)

        leg = ROOT.TLegend(0.5, 0.85, 0.9, 0.9)
        leg.AddEntry(h, hext ,"l")

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
    leg.AddEntry(h1, getRatioLegendTitle(h1, h2, comparetype)[1] ,"l")
    leg.AddEntry(h2, getRatioLegendTitle(h1, h2, comparetype)[0] ,"l")
    
    c = ROOT.TCanvas('c', '', 600, 800)
    p1 = ROOT.TPad("p1", "p1", 0, 0.3, 1, 1.0)
    p1.SetBottomMargin(0) # Upper and lower plot are joined
    p1.Draw()             # Draw the upper pad: p1
    p1.cd()
    h1.Draw(drawOption+"E")
    h2.Draw(drawOption+"ESAME")
    leg.Draw("SAME")
    if islogy:ROOT.gPad.SetLogy()
    if 'dxy' in htitle:ROOT.gPad.SetLogx()
    c.cd()
    p2 = ROOT.TPad("p2", "p2", 0, 0.01, 1, 0.3)
    p2.SetTopMargin(0)
    p2.SetBottomMargin(0.2)
    p2.Draw()
    p2.cd()
    hRatio.SetMarkerSize(0.6)
    hRatio.GetYaxis().SetRangeUser(0.6,1.4)
    hRatio.Draw("PE")
    hRatioFrame.Draw("HISTsame")
    c.SaveAs(outputdirpath+"/"+htitle+".png")
    c.Close()


def CompareHistExt(files, samplelist, var, comparetype, dir, drawOption="hist", islogy=False, scaleOption='unitscaling', canvasX=600, canvasY=800):
    outputdirpath = os.path.join(dir,"ComparisonPlots",comparetype)
    if not os.path.exists(outputdirpath):
        if os.path.exists(os.path.join(dir,"RatioPlots")):
            os.mkdir(outputdirpath)
        else:
            os.makedirs(outputdirpath)

    ht=[]
    for i, f in enumerate(files,0):
        ht.append(f.Get(var+'_'+samplelist[i]))
            
    if 'unit' in scaleOption:
        for h in ht:
            if h.Integral(): h.Scale(1/h.Integral())

    hRatio=[]
    leg = ROOT.TLegend(0.7, 0.75, 0.9, 0.9)        
    leg.AddEntry(ht[0], samplelist[0],"l")
    style1D(ht[0], islogy, "a.u.")
    for i, h2 in enumerate(ht[1:], 1):
        h2.SetLineColor(getColor(samplelist[i]))
        h2.SetLineWidth(2)
        leg.AddEntry(h2, samplelist[i],"l")
        hRatio.append(getHistratio(ht[0], h2, comparetype, var))
    hRatioFrame = getHistratioframe(hRatio[0])
    hRatioFrame.GetYaxis().SetTitle(hRatio[0].GetYaxis().GetTitle())
    hRatioFrame.GetXaxis().SetTitle(hRatio[0].GetXaxis().GetTitle())
    
    c = ROOT.TCanvas('c', '', 600, 800)
    p1 = ROOT.TPad("p1", "p1", 0, 0.3, 1, 1.0)
    p1.SetBottomMargin(0) # Upper and lower plot are joined
    p1.Draw()             # Draw the upper pad: p1
    p1.cd()
    ht[0].Draw(drawOption+"E")
    for h2 in ht[1:]:
        h2.Draw(drawOption+"ESAME")
    leg.Draw("SAME")
    if islogy:ROOT.gPad.SetLogy()
    c.cd()
    p2 = ROOT.TPad("p2", "p2", 0, 0.01, 1, 0.3)
    p2.SetTopMargin(0)
    p2.SetBottomMargin(0.2)
    p2.Draw()
    p2.cd()
    hRatioFrame.GetYaxis().SetRangeUser(0.6,1.4)
    hRatioFrame.Draw("HIST")
    for i, hR in enumerate(hRatio, 1):
        hR.SetLineColor(getColor(samplelist[i]))
        hR.SetMarkerSize(0.6)
        hR.Draw("PEsame")
    
    c.SaveAs(outputdirpath+"/"+var+".png")
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
    '''
    #to plot upto some bins, usually only SR bins
    for h in hs_MC:
        h.GetXaxis().SetRangeUser(0,54)
    hs[-1].GetXaxis().SetRangeUser(0,54)
    '''
    hStack_MC = ROOT.THStack("hStack_MC","hStack_MC")
    hMC = hs_MC[0].Clone("TotalMC")
    leg = ROOT.TLegend(0.4, 0.6, 0.9, 0.9)
    leg.SetNColumns(3)
    for i, h in enumerate(hs_MC, 0):
        hStack_MC.Add(h)
        h.SetFillColor(getColor(samplelist[i]))
        h.SetLineColor(getColor(samplelist[i]))
        leg.AddEntry(h, getLegendTitle(samplelist[i])+' ('+str(round(h.Integral(), 2))+')',"f")
        if i!=0:
            hMC.Add(h)
                
    leg.AddEntry(hs[-1], getLegendTitle('Data')+' ('+str(round(hs[-1].Integral(), 2))+')',"pe")
    styleData(hs[-1], islogy)

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

#stackhist with signal overlay
def StackHistsExt(files, samplelist, var, dir, cut, islogy=True, scaleOption='Lumiscaling', canvasX=600, canvasY=800):
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
    hBK=[]
    hsig=[]
    leg = ROOT.TLegend(0.5, 0.6, 0.9, 0.9)
    leg.SetNColumns(3)
    hMC = hs_MC[0].Clone("TotalMC")
    hStack_MC = ROOT.THStack("hStack_MC","hStack_MC")
    for i, h in enumerate(hs_MC, 0):
        if 'T2tt' in samplelist[i] or 'Sig' in samplelist[i]:
            hsig.append(h)
            h.SetLineColor(len(hs)-i)
            h.SetLineWidth(2)
            leg.AddEntry(h, getLegendTitle(samplelist[i]), "l")
        else:
            hBK.append(h)
            hStack_MC.Add(h)
            h.SetFillColor(getColor(samplelist[i]))
            h.SetLineColor(getColor(samplelist[i]))
            leg.AddEntry(h, getLegendTitle(samplelist[i]) ,"f")
            if i!=0:
                hMC.Add(h)
                
    leg.AddEntry(hs[-1], getLegendTitle('Data') ,"pe") #last entry in hs is data
    styleData(hs[-1], islogy)
    mVal = hs[-1].GetBinContent(hs[-1].GetMaximumBin()) if hs[-1].GetBinContent(hs[-1].GetMaximumBin())>hMC.GetBinContent(hMC.GetMaximumBin()) else hMC.GetBinContent(hMC.GetMaximumBin())
    maxRange = mVal * 100 if islogy else mVal * 1.5
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
    for i in range(len(hsig)):
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
    c.SaveAs(outputdirpath+"/"+var+".png")
    c.Close()
                                                                                                                    
    
# Functions to print out a pdf-quality png file:
def SaveAsQualityPng(canvas,filename,import_scale=1.5):
    if not isinstance(canvas, ROOT.TCanvas):
        print "Error in <PlotHelper.SaveAsQualityPng>: invalid input canvas"
        return

    oldignore = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    canvas.SaveAs("./temp_pdffile.pdf")
    ROOT.gErrorIgnoreLevel = oldignore
    printNicePng("./temp_pdffile.pdf",filename,import_scale)
    os.remove("./temp_pdffile.pdf")

def printNicePng(filename,outfile = "",import_scale=1.5,silent=True):
    if ".pdf" in filename or ".png" in filename:
        filename = filename[:-4]

    if not os.path.exists(filename+".pdf"):
        print "Error: in <PlotHelper.printNicePng>: input "+filename+".pdf not found or not accessible!"
        return

    if not outfile:
        outfile = filename
    elif ".png" in outfile:
        outfile = outfile[:-4]

    if not import_scale:
        import_scale = 1.0

    with open(os.devnull, 'wb') as devnull:
        bashCall = '/big_data/kadlec/tools/cdpf/cpdf -scale-page "'+str(import_scale)+' '+str(import_scale)+'" '+filename+'.pdf -o temp_upscaled.pdf'
        if(silent):
            subprocess.check_call(bashCall, shell=True,stdout=devnull, stderr=subprocess.STDOUT)
        else:
            subprocess.check_call(bashCall, shell=True)

        bashCall =  "gimp -i -b '(let* ((image (car (gimp-file-load RUN-NONINTERACTIVE \"temp_upscaled.pdf\" \"temp_upscaled.pdf\"))) (drawable (car (gimp-image-get-active-layer image))))  (set! drawable (car (gimp-image-get-active-layer image)))      (gimp-file-save RUN-NONINTERACTIVE image drawable \""+outfile+".png\" \""+outfile+".png\") (gimp-image-delete image))' -b '(gimp-quit 0)'"
        if(silent):
            subprocess.check_call(bashCall, shell=True,stdout=devnull, stderr=subprocess.STDOUT)
        else:
            subprocess.check_call(bashCall, shell=True)
            
        os.remove('temp_upscaled.pdf')
        print "Info in <PlotHelper.printNicePng>: png file "+outfile+".png has been created"



# ROC curve plot 
# This function is capable of plotting a combination of points and lines on a ROC curve.
def plotROC(signal_pass, signal_total, bk_pass, bk_total, markdown, legTitle, path, name, samplename, BKsamplename, xmin = "auto", ymin = "auto", xmax = "auto", ymax = "auto", title = "auto", ptcut = -1, xtitle = "Signal efficiency", ytitle ="BK rejection (1-eff)", cmssimwip = True, legendpos = "br", legendscale = 1.0, fileformat = "png"):
    plotROCLines(signal_pass, signal_total, bk_pass, bk_total, [], markdown, legTitle, path, name, samplename, BKsamplename, xmin, ymin, xmax, ymax, title, ptcut, xtitle, ytitle, cmssimwip, legendpos, legendscale, fileformat)


def plotROCLines(signal_pass, signal_total, bk_pass, bk_total, line_info, markdown, legTitle, path, name, samplename, BKsamplename, xmin = "auto", ymin = "auto", xmax = "auto", ymax = "auto", title = "auto", ptcut = -1, xtitle = "Signal efficiency", ytitle ="BK rejection (1 - BKeff)", cmssimwip = True, legendpos = "br", legendscale = 1.0, fileformat = "png"):
    if(len(signal_pass) != len(bk_pass) or len(signal_pass) < len(signal_total) or len(bk_pass) < len(bk_total)):
        print 'Error in plotROCLines: arrays are incompatible'
        return -1
    
    required_length = len(line_info) + (len(signal_pass) - sum(line_info))
    if(len(legTitle) < required_length):
        print 'Error in plotROCLines: not enough labels: '+str(len(legTitle))+', required: '+str(required_length)
        return -1


    if(not isinstance(markdown, list)):
        print 'Error in plotROCLines: markdown must be a list of colors, or a joint list of markdown options, refer to manual'
        return -1
    

    colors_processed = markdown
    complex_markdown = isinstance(markdown[0], list)

    markers_specified = False
    linestyle_specified = False
    if(complex_markdown):
        if(len(markdown[0]) > 0):
            colors_processed = markdown[0]
        else:
            colors_processed = [ROOT.kBlack] * len(required_length)
        
        if(len(markdown) > 1 and len(markdown[1]) > 0):
            markers_processed = markdown[1]
            markers_specified = True
        
        if(len(markdown) > 2 and len(markdown[2]) > 0):
            linestyle_processed = markdown[2]
            linestyle_specified = True


    if(len(colors_processed) < required_length):
        print 'Warning in plotROCLines: not enough colors specified, cycling. Make sure this is what you intended!'
        while(len(colors_processed) < required_length):
            for i in range(len(markdown[0] if markers_specified else markdown)):
                colors_processed.append(markdown[0][i] if markers_specified else markdown[i])

    if(markers_specified and len(markers_processed) < required_length):
        print 'Warning in plotROCLines: not enough marker styles specified, cycling. Make sure this is what you intended!'
        while(len(markers_processed) < required_length):
            for i in range(len(markdown[1])):
                markers_processed.append(markdown[1][i])

    if(linestyle_specified and len(linestyle_processed) < required_length):
        print 'Warning in plotROCLines: not enough linestyles specified, cycling. Make sure this is what you intended!'
        while(len(linestyle_processed) < required_length):
            for i in range(len(markdown[2])):
                linestyle_processed.append(markdown[2][i])


    effs = []
    Deffs_low = []
    Deffs_high = []

    for i in range(len(signal_pass)):
        if(signal_pass[i] == None):
            print 'Warning: None object in signal pass at: '+str(i)
        if(signal_total[i] == None):
            print 'Warning: None object in signal total at: '+str(i)
        
        signal_pass[i].Rebin(signal_pass[i].GetNbinsX())
        signal_total[i].Rebin(signal_total[i].GetNbinsX())
        teff = ROOT.TEfficiency(signal_pass[i],signal_total[i])


        effs.append(teff.GetEfficiency(teff.GetGlobalBin(1)))
        Deffs_low.append(teff.GetEfficiencyErrorLow(teff.GetGlobalBin(1)))
        Deffs_high.append(teff.GetEfficiencyErrorUp(teff.GetGlobalBin(1)))

    rejs = []
    Drejs_low = []
    Drejs_high = []

    for i in range(len(bk_pass)):
        if(bk_pass[i] == None):
            print 'Warning: None object in bk pass at: '+str(i)
        if(bk_total[i] == None):
            print 'Warning: None object in bk total at: '+str(i)


        bk_pass[i].Rebin(bk_pass[i].GetNbinsX())
        bk_total[i].Rebin(bk_total[i].GetNbinsX())
        teff = ROOT.TEfficiency(bk_pass[i],bk_total[i])

        rejs.append(teff.GetEfficiency(teff.GetGlobalBin(1)))
        Drejs_low.append(teff.GetEfficiencyErrorLow(teff.GetGlobalBin(1)))
        Drejs_high.append(teff.GetEfficiencyErrorUp(teff.GetGlobalBin(1)))

    if(title == "auto"):
        if(-1 != ptcut):
            title = "#splitline{ROC for signal: "+samplename+"}{BK: "+BKsamplename+", pt > "+str(ptcut)+" GeV}"
        else:
            title = "#splitline{ROC for signal: "+samplename+"}{BK: "+BKsamplename+"}"

    roc = {}
    absolute_min_x = 1
    absolute_max_x = 0
    absolute_min_y = 1
    absolute_max_y = 0
    lineidx = 0
    i = 0
    next_roc = 0
    while(i < len(effs)):
        x = []
        y = []
        Dx_high = []
        Dx_low = []
        Dy_high = []
        Dy_low = []
        isline = False
        if(lineidx < len(line_info)):
            isline = True
            for k in range(i,i+line_info[lineidx],1):
                x.append(effs[k])
                y.append(rejs[k])
                #Dx_high.append(Deffs_high[k])
                #Dx_low.append(Deffs_low[k])
                #Dy_high.append(Drejs_high[k])
                #Dy_low.append(Drejs_low[k])
                # if line, don't put errorbars:
                Dx_high.append(0)
                Dx_low.append(0)
                Dy_high.append(0)
                Dy_low.append(0)

        else:
            x = [effs[i]]
            y = [rejs[i]]
            Dx_high = [Deffs_high[i]]
            Dx_low = [Deffs_low[i]]
            Dy_high = [Drejs_high[i]]
            Dy_low = [Drejs_low[i]]

        for j in range(len(x)):
            if(x[j] + Dx_high[j] > 1):
                Dx_high[j] = 1 - x[j]
            if(x[j] - Dx_low[j] < 0):
                Dx_low[j] = x[j]
            if(y[j] + Dy_high[j] > 1):
                Dy_high[j] = 1 - y[j]
            if(y[j] - Dy_low[j] < 0):
                Dy_low[j] = y[j]

            if x[j] - Dx_low[j] < absolute_min_x:
                absolute_min_x = x[j] - Dx_low[j]
            if x[j] + Dx_high[j] > absolute_max_x:
                absolute_max_x = x[j] + Dx_high[j]
            if y[j] - Dy_low[j] < absolute_min_y:
                absolute_min_y = y[j] - Dy_low[j]
            if y[j] + Dy_high[j] > absolute_max_y:
                absolute_max_y = y[j] + Dy_high[j]
            
        roc[next_roc] = ROOT.TGraphAsymmErrors(len(x),np.array(x),np.array(y),np.array(Dx_low),np.array(Dx_high),np.array(Dy_low),np.array(Dy_high))
    
        roc[next_roc].SetLineColor(colors_processed[next_roc])
        roc[next_roc].SetLineWidth(2)
        if(isline):
            roc[next_roc].SetLineStyle(linestyle_processed[next_roc] if linestyle_specified else 2)
        roc[next_roc].SetMarkerSize(1.2 if markers_specified else 0.8)
        roc[next_roc].SetMarkerStyle(markers_processed[next_roc] if markers_specified else 20)
        roc[next_roc].SetMarkerColor(colors_processed[next_roc])
        roc[next_roc].SetTitle(title)
        next_roc += 1

        if(lineidx < len(line_info) ):
            i += line_info[lineidx]
            lineidx += 1
        else:
            i += 1

    legxl = 0.5
    legxu = 0.9
    legyl = 0.1
    legyu = 0.3 * legendscale
    if(legendpos == "bl"):
        legxl = 0.1
        legxu = 0.5


    if(legendpos == "separate"):
        legxl = 0.1
        legxu = 0.9
        legyl = 0.1
        legyu = 0.9






    leg = ROOT.TLegend(legxl, legyl, legxu, legyu)
    for i in range(len(roc)):
        leg.AddEntry(roc[i], legTitle[i] ,"p")
    ROOT.gStyle.SetLegendTextSize(0.019)


    valuerange_x = absolute_max_x - absolute_min_x
    valuerange_y = absolute_max_y - absolute_min_y
    if(xmin == "auto"):
        xmin = absolute_min_x - valuerange_x * 0.05
    if(xmax == "auto"):
        xmax = absolute_max_x + valuerange_x * 0.05
    if(ymin == "auto"):
        ymin = absolute_min_y - valuerange_y * 0.05
    if(ymax == "auto"):
        ymax = absolute_max_y + valuerange_y * 0.05


    #c = ROOT.TCanvas('c', 'Title', 600, 800)
    if(legendpos == "separate"):
        ROOT.gStyle.SetPaperSize(40,26.6666)
        canvas = ROOT.TCanvas('c', 'Title', 1200, 800)
        figurepad = ROOT.TPad("figurepad", "figurepad",0.5,0.0,1.0,1.0)
        figurepad.SetGrid()
        figurepad.Draw()
        figurepad.cd()
        fr = figurepad.DrawFrame(xmin,ymin,xmax,ymax)
    else:
        canvas = ROOT.TCanvas('c', 'Title', 600, 800)
        canvas.SetGrid()
        fr = canvas.DrawFrame(xmin,ymin,xmax,ymax)

    fr.SetTitle(title)
    fr.SetTitleSize(0.01)

    fr.GetYaxis().SetTitle(ytitle)
    fr.GetYaxis().SetTitleSize(0.04)
    fr.GetYaxis().SetTitleOffset(1.25)
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
        if(i < len(line_info)): 
            roc[i].Draw("LP,SAME")
        else:
            roc[i].Draw("P,SAME")


    if(legendpos == "separate"):
        canvas.cd()
        legendpad = ROOT.TPad("legendpad", "legendpad",0.0,0.0,0.5,1.0)
        legendpad.Draw()
        legendpad.cd()
    if(legendpos != "no" and legendpos != "disable" and legendpos != False):
        leg.Draw("SAME")
    


    if(name == ""):
        name = "ROCfigure_Sig_"+samplename+"_BK_"+BKsamplename
        if(ptcut != -1):
            name += "_pt"+str(ptcut)

    if(not isinstance(fileformat, list)):
        fileformat = [fileformat]

    for fform in fileformat:
        if(fform == "png"):
            SaveAsQualityPng(canvas,path+"/"+name+"."+fform)
        else:
            canvas.SaveAs(path+"/"+name+"."+fform)

    canvas.Close()
    return 0


