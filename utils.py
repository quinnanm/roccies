import os
import numpy as np
import ROOT as r

def makeroot(infile, treename, options="read"):
    rfile = r.TFile(infile, options)
    tree = rfile.Get(treename)
    return rfile, tree

def getyield(hist, verbose=False):
    errorVal = r.Double(0)
    minbin=0
    maxbin=hist.GetNbinsX()+1
    hyield = hist.IntegralAndError(minbin, maxbin, errorVal)
    if verbose:
        print 'yield:', round(hyield, 3), '+/-', round(errorVal, 3), '\n'
    return hyield,  errorVal

def fixref(rootfile, hist):
    hist.SetDirectory(0)
    rootfile.Close()

def addhists(hist1, hist2):
    hist = hist1.Clone('hist')
    hist.Add(hist2)
    hist.SetDirectory(0)
    return hist
