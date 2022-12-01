# Helper

Various helper functions.
  
<b>Manual for printing png images:</b>

The SaveAsQualityPng(canvas, filename) function can be used to save a TCanvas object as a png image with included anti-aliasing for near vectorgraphics-quality. Parameters of the function:
- canvas: the TCanvas object to save
- filename: the output filename (string)
- import_scale (default=1.5): An internal upscaling parameter used by the tools that create the image. The higher it is, the clearer written text is on the image, and also the image becomes larger. Not recommended to set below ~1.2, then text can become blurry.



The printNicePng(filename,outfile = "",import_scale=1.5,silent=True) function can be used to export a png image from an existing pdf file. Parameters:
- filename: The input filename of the existing pdf. (can be with or without the ".pdf" extension)
- outfile: The output filename of the new png. Can be with or without the ".png" extension. If left empty, the outfile name will be identical to the input filename.
- import_scale (default=1.5): An internal upscaling parameter used by the tools that create the image. The higher it is, the clearer written text is on the image, and also the image becomes larger. Not recommended to set below ~1.2, then text can become blurry.
- silent (default=True): A boolean, specifying whether to suppress the stdout and stderr of external tools used in the conversion.
Example of very simple usage, supposing we already have an "images/example.pdf" file:
PlotHelper.printNicePng("images/example.pdf")
This will create an "images/example.png" in near-matching fidelity.
  
  
  
<b>Manual for ROC plotting:</b>

You can use plotROC to plot a ROC figure that contains points, or you can use plotROCLines for a figure that contains lines, or both lines and points.
Parameters:
- signal_pass: list of TH1 (or derivative) objects: these are the histograms used for the numerator of the efficiency
- signal_total: list of TH1 objects: histograms used for denominator of the efficiency. Length of list must equal that of signal_pass
- bk_pass: list of TH1, numerator of bk efficiency. Length must equal signal_pass
- bk_total: list of TH1, denominator of bk efficiency. Length must equal signal_pass

The histograms can be in any binning.
- line_info: A list of integers, showing how many points should form each line. For example, line_info = [2,3,3] implies that you have at least 2+3+3=8 histograms in your input and you have three lines: the first two histograms form one line, the next 3 histograms form the second, the next 3 histograms form the third, and any further histograms in the input are considered separate points.

plotROC doesn't have a line_info parameter. In fact, plotROC is a shorthand function for plotROClines with line_info = []

- markdown: a list of colors, or a list of lists of markdown options.
  - If it is a list of colors (f.e. [ROOT.kBlack, ROOT.kBlue, ...]), then this specifies the colors of the lines and separate points. If there are not enough colors, the list will be looped over and the code will warn you about this.
  - If it is a complex markdawn list, it must have the form of [[list of colors],[list of marker styles],[list of line styles]]. If a list of options is not long enough, it will be looped over, and an empty list corresponds to "not specified". So for example if you have 3 lines, and you want to specify 3 colors and want to have the second line to have a different marker, you can do: markdown = [[color1,color2,color3],[style1,style2]]. Or if you want to have all lines with the default color, default marker, but with different lines: markdown = [[],[],[line1,line2,line3]].

- legTitle: list of line and point names for the legend. The list must be as long as the number of lines and separate points
- path: path to the output
- name: name of the output file
- samplename: name of the sample used for efficiency. This parameter is used by the automatic title
- BKsamplename: name of the background sample. This parameter is used by the automatic title
- xmin  (default="auto"): float value for the minimum value of the x-axis. If set to "auto", it will autoscale
- ymin  (default="auto"): float value for the minimum value of the y-axis. If set to "auto", it will autoscale
- xmax  (default="auto"): float value for the maximum value of the x-axis. If set to "auto", it will autoscale
- ymax  (default="auto"): float value for the maximum value of the y-axis. If set to "auto", it will autoscale
- title  (default="auto"): the title of the output figure. If set to "auto", it will set up a title based on the input information and parameters
- ptcut  (default=-1): float value for the ptcut used in the samples. If set to -1, it means no ptcut was used
- xtitle (default="Signal efficiency"): label of the x-axis
- ytitle (default="BK rejection (1 - BKeff)"): label of the y-axis
- cmssimwip (default=True): if True, there will be a "CMS Simulation work in progress" label  on the figure
- legendpos (default="br"): sets the position of the legend. Options are:
  - "br": bottom right
  - "bl": bottom left
  - "no": no legend
- legendscale (default=1.0): sets the overall size of the legend
- fileformat (default="png"): sets the output format of the file, can be "png" or "pdf"
