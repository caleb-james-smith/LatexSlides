import glob
import json
import argparse
    
tex_snippet_1plot = """ 
    \\begin{frame}{%s}
        \\includegraphics[width=0.5\\textwidth]{{"%s"}.pdf}
    \\end{frame}
    """

tex_snippet_2plot = """ 
    \\begin{frame}{%s}
        \\includegraphics[width=0.5\\textwidth]{{"%s"}.pdf}
        \\includegraphics[width=0.5\\textwidth]{{"%s"}.pdf}
    \\end{frame}
    """

tex_snippet_4plot = """ 
    \\begin{frame}{%s}
        \\includegraphics[width=0.25\\textwidth]{{"%s"}.pdf}
        \\includegraphics[width=0.25\\textwidth]{{"%s"}.pdf}
        \\includegraphics[width=0.25\\textwidth]{{"%s"}.pdf}
        \\includegraphics[width=0.25\\textwidth]{{"%s"}.pdf}
    \\end{frame}
    """
# latex versions of variables
variables_tex = {
                    "nj"                                : "$N_{jets}$", 
                    "ht"                                : "$H_T$", 
                    "met"                               : "$\cancel{E}_T$", 
                    "metphi"                            : "$\phi_{MET}$", 
                    "dPhi1"                             : "$\Delta\phi_{1}$", 
                    "dPhi2"                             : "$\Delta\phi_{2}$", 
                    "dPhi3"                             : "$\Delta\phi_{3}$", 
                    "dPhi4"                             : "$\Delta\phi_{4}$",
                    "bestRecoZPt"                       : "$p_{T}(LL)$",
                    "PhotonPt"                          : "$p_{T}^{\gamma}$",
                    "PhotonEta"                         : "$\eta^{\gamma}$",
                    "bestRecoZM_50to250"                : "$m_{LL}$",
                    "bestRecoZM_50to250_NBeq0_NSVeq0"   : "$m_{LL}\ \\left(N_{b} = 0, N_{sv} = 0\\right)$",
                    "bestRecoZM_50to250_NBeq0_NSVge1"   : "$m_{LL}\ \\left(N_{b} = 0, N_{sv} \geq 1\\right)$",
                    "bestRecoZM_50to250_NBeq1_NSVeq0"   : "$m_{LL}\ \\left(N_{b} = 1, N_{sv} = 0\\right)$",
                    "bestRecoZM_50to250_NBeq1_NSVge1"   : "$m_{LL}\ \\left(N_{b} = 1, N_{sv} \geq 1\\right)$",
                    "bestRecoZM_50to250_NBge1_NSVeq0"   : "$m_{LL}\ \\left(N_{b} \geq 1, N_{sv} = 0\\right)$",
                    "bestRecoZM_50to250_NBge1_NSVge1"   : "$m_{LL}\ \\left(N_{b} \geq 1, N_{sv} \geq 1\\right)$",
                    "bestRecoZM_50to250_NBeq1"          : "$m_{LL}\ \\left(N_{b} = 1\\right)$",
                    "bestRecoZM_50to250_NBge2"          : "$m_{LL}\ \\left(N_{b} \geq 2\\right)$",
}
# latex version of cuts
cuts_tex = {
                "jetpt20" : "Jet $p_{T} > 20$ GeV",
                "jetpt30" : "Jet $p_{T} > 30$ GeV",
                "jetpt40" : "Jet $p_{T} > 40$ GeV",
}

def write(f,globString,title):
    plotList = glob.glob(globString)

    for i in range(0, len(plotList), 2):
        if i == len(plotList) - 1:
            f.write(tex_snippet_1plot % (title, plotList[i].replace(".pdf","")))
            print plotList[i]
        else:
            f.write(tex_snippet_2plot % (title, plotList[i].replace(".pdf",""), plotList[i+1].replace(".pdf","")))
            print plotList[i]
            print plotList[i+1]

def writeLine(f, line):
    f.write(line + "\n")

# make slide with multiple eras on one slide
def writeSlideEras(f, runMap, fileString, variable, eras, title):
    n = len(eras)
    width = 1.0 / float(n)
    x = 0
    dx = int(16 / n)
    writeLine(f, "\\begin{frame}{%s}" % (title))
    for e in eras:
        e_tex = e.replace("_", " ")
        # example: "../histos_DataMC_2016_27_Jun_2019_3/DataMC_Electron_LowDM_dPhi1_2016"
        # example: \includegraphics[width=0.25\textwidth]{{"../histos_DataMC_2016_27_Jun_2019_3/DataMC_Electron_LowDM_dPhi1_2016"}.pdf}
        d = runMap[e]
        name = "../%s/%s_%s" % (d, fileString, e)
        writeLine(f, "\\begin{textblock*}{4cm}(%dcm,2cm)" % x)
        writeLine(f, "\\begin{figure}")
        writeLine(f, "\\centering")
        writeLine(f, "\\textbf{%s}\par\medskip" % e_tex)
        writeLine(f, "\\includegraphics[width=1.0\\textwidth]{{\"%s\"}.pdf}" % (name))
        writeLine(f, "\\caption{%s}" % variable)
        writeLine(f, "\\end{figure}")
        writeLine(f, "\\end{textblock*}")
        x += dx
    writeLine(f, "\\end{frame}")

# make slide with multiple cuts
def writeSlideCuts(f, runMap, fileString, variable, cuts, era, title):
    n = len(cuts)
    width = 1.0 / float(n)
    x = 0
    dx = int(16 / n)
    writeLine(f, "\\begin{frame}{%s}" % (title))
    for c in cuts:
        c_tex = cuts_tex[c]
        # example: "../histos_DataMC_2016_27_Jun_2019_3/DataMC_Electron_LowDM_dPhi1_2016"
        # example: \includegraphics[width=0.25\textwidth]{{"../histos_DataMC_2016_27_Jun_2019_3/DataMC_Electron_LowDM_dPhi1_2016"}.pdf}
        d = runMap[era]
        name = "../%s/%s_%s_%s" % (d, fileString, c, era)
        writeLine(f, "\\begin{textblock*}{4cm}(%dcm,2cm)" % x)
        writeLine(f, "\\begin{figure}")
        writeLine(f, "\\centering")
        writeLine(f, "%s\par\medskip" % c_tex)
        writeLine(f, "\\includegraphics[width=1.0\\textwidth]{{\"%s\"}.pdf}" % (name))
        writeLine(f, "\\caption{%s}" % variable)
        writeLine(f, "\\end{figure}")
        writeLine(f, "\\end{textblock*}")
        x += dx
    writeLine(f, "\\end{frame}")

def makeSlidesEras(json_file, verbose):
    eras = ["2016", "2017", "2018_AB", "2018_CD"]
    #eras = ["2016"]
    regions = ["LowDM", "HighDM"]
    #particles = ["Electron", "Muon", "Photon"]
    particles = ["Photon"]
    variables = ["nj", "ht", "met", "metphi", "dPhi1", "dPhi2", "dPhi3", "dPhi4"]
    j = open(json_file)
    f = open("stack_snippet.tex",'w')
    runMap = json.load(j)
    # still using validation selection; update when search seleciton is done for all eras
    variables_lowdm_leptons  = ["bestRecoZPt", "bestRecoZM_50to250", "bestRecoZM_50to250_NBeq0_NSVeq0", "bestRecoZM_50to250_NBeq0_NSVge1", "bestRecoZM_50to250_NBeq1_NSVeq0", "bestRecoZM_50to250_NBeq1_NSVge1", "bestRecoZM_50to250_NBge1_NSVeq0", "bestRecoZM_50to250_NBge1_NSVge1", "bestRecoZM_50to250_NBge2"]
    variables_highdm_leptons = ["bestRecoZPt", "bestRecoZM_50to250", "bestRecoZM_50to250_NBeq1", "bestRecoZM_50to250_NBge2"]
    variables_photon = ["PhotonPt", "PhotonEta"]
    variable_map = {}
    variable_map["Electron"] = {}
    variable_map["Electron"]["LowDM"] = variables + variables_lowdm_leptons
    variable_map["Electron"]["HighDM"] = variables + variables_highdm_leptons
    variable_map["Muon"] = {}
    variable_map["Muon"]["LowDM"] = variables + variables_lowdm_leptons
    variable_map["Muon"]["HighDM"] = variables + variables_highdm_leptons
    variable_map["Photon"] = {}
    variable_map["Photon"]["LowDM"] = variables + variables_photon
    variable_map["Photon"]["HighDM"] = variables + variables_photon
    
    # example: "../histos_DataMC_2016_27_Jun_2019_3/DataMC_Electron_LowDM_dPhi1_2016"

    for p in particles:
        for r in regions:
            variableList = variable_map[p][r]
            for v in variableList:
                if verbose:
                    print "Making slide for %s %s %s" % (p, r, v)
                v_tex = variables_tex[v]
                fileString = "DataMC_%s_%s_%s" % (p, r, v)
                title = "%s CR %s: %s" % (p, r, v_tex)
                writeSlideEras(f, runMap, fileString, v_tex, eras, title)
    
    f.close()
    j.close()

def makeSlidesCuts(json_file, verbose):
    #eras = ["2016", "2017_BE", "2017_F", "2018_PreHEM", "2018_PostHEM"]
    eras = ["2016"]
    #regions = ["LowDM", "HighDM"]
    regions = ["LowDM"]
    #particles = ["Electron", "Muon", "Photon"]
    particles = ["Photon"]
    selections = ["passPhotonSelectionLoose", "passPhotonSelectionMedium", "passPhotonSelectionTight"]
    #variables = ["nj", "ht", "met", "metphi", "dPhi1", "dPhi2", "dPhi3", "dPhi4"]
    variables = ["nj"]
    cuts = ["jetpt20", "jetpt30", "jetpt40"] 
    j = open(json_file)
    f = open("stack_snippet.tex",'w')
    runMap = json.load(j)

    # example: DataMC_Photon_LowDM_nj_passPhotonSelectionLoose_jetpt20_2016
    
    for p in particles:
        for v in variables:
            for e in eras:
                for r in regions:
                    for s in selections:
                        if verbose:
                            print "Making slide for %s %s %s %s %s" % (p, v, e, r, s)
                        v_tex = variables_tex[v]
                        fileString = "DataMC_%s_%s_%s_%s" % (p, r, v, s)
                        title = "%s CR %s: %s, %s - %s" % (p, e, r, s, v_tex)
                        writeSlideCuts(f, runMap, fileString, v_tex, cuts, e, title)
    
    
    f.close()
    j.close()

def main():
    # options
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--json_file",    "-j", default="",                             help="json file containing runs")
    parser.add_argument("--verbose",      "-v", default = False, action = "store_true", help="verbose flag to print more things")
    
    options     = parser.parse_args()
    json_file   = options.json_file
    verbose     = options.verbose

    if not json_file:
        print "Please enter a json file containing runs using the -j option."
        exit(1)

    #makeSlidesEras(json_file, verbose)
    makeSlidesCuts(json_file, verbose)


if __name__ == '__main__':
    main()



