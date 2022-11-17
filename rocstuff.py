import numpy as np
import matplotlib
import argparse
import matplotlib.pyplot as plt
import ROOT as r
from ROOT import gStyle
gStyle.SetOptStat(0)
r.gROOT.SetBatch(True)
import utils as ut
import pandas as pd
from root_numpy import root2array, array2root, fill_hist, array2tree
#import uproot

class rocstuff:
    def __init__(self):
        #general settings
        # self.indir = indir
        self.nbins = 100
        self.xmin = 0.0
        self.xmax = 1.0
        self.treename = 'Events'

    #define signal and background selections and labels
    # def getsels():

    def gethist(self, infiles=[], var='', cutstr=''):
        # inputs rootfiles and outputs combined hists
        #infiles is list of string rootfile names. multiple files will be combined
        #var is the discriminating variable, ie the score
        #cutstr is selection you are applying
        hists=[]
        for f in infiles:
            hist = r.TH1F("hist", "hist", self.nbins, self.xmin, self.xmax)
            rf,t = ut.makeroot(filename, self.treename)
            t.Draw(var+">>hist",cutstr)
            hist.Sumw2() #for errors
            ut.fixref(rf, hist)
            hists.append(hist)
        #if more than one histogram, add them together
        hist = hists[0]
        if len(hists)>1:
            for i,h in enumerate(hists):
                if i==0:
                    continue
                hist=ut.addhists(hist,h)
        return hist

    def getarr(self, infile='', cutstr='', branches=[]):
        #returns array of given var with selection applied
        #will switch to uproot but for now just use root numpy
        #branches = [list of only branches you want to keep, optional]
        # events = uproot.open(self.ifile)[self.treename].arrays(branches, cutstr)
        print 'file',infile
        print 'cutstr',cutstr
        events = pd.DataFrame(root2array(infile, self.treename, selection=cutstr))
        if branches:
                #keep only specified branches
            events = events[branches]
                
        return events

    #outputs truth and prediction arrays for roc_curve inputs
    def preproc(self, var, siglabelarr, bkglabelarr, sigarr, bkgarr):
       # """
       #  We expect all scores to sum up to 1, e.g. given two signals in the event (signal 1 and 2) and one background process (background 1)
       #  score_signal_1 + score_signal_2 + score_background_1 = 1
       #  Then nn_signal_1 = score_signal_1 / (score_signal_1 + score_background_1) = score_signal_1 / (1 - score_signal_2)
       #  """
        #var - disc score
        #siglabel - label for signal to be true
        #bkglabel - label for background to be true
        #sigarr - events coming from signal
        #bkgarr - events coming from background
        
        #may need to add functionality for combining multiple such arrays
        # PROBLEM AREA
        siglabel = siglabelarr[0]+'==1'
        if len(siglabelarr)>1:
            for i in range(1,len(siglabelarr)):
                siglabel += siglabelarr[i]+'==1 &'
        siglabel = siglabel
        print siglabel

        #complaining about masks
        sigscores = sigarr[var]#.to_numpy()
        bkgscores = bkgarr[var]#.to_numpy()
        
        sigmask = sigarr[siglabel]==1
        bkgmask = bkgarr[bkglabel]==1
        print 'siglabel',siglabel
        print len(sigscores), len(sigmask)
        # sigscores = sigarr[var][sigmask].to_numpy()
        # bkgscores = bkgarr[var][bkgmask].to_numpy()
        sigscores = sigscores[sigmask]#.to_numpy()
        bkgscores = bkgscores[bkgmask]#.to_numpy()
        predict = np.concatenate((sigscores, bkgscores), axis=None)

        siglabels = np.ones(sigscores.shape)
        bkglabels = np.zeros(bkgscores.shape)
        truth = np.concatenate((siglabels, bkglabels), axis=None)

        #outputs array of predictions and array of truth values
        return truth, predict

    # takes truth labels and scores, outputs tpr and fpr 
    def getroc(self, truth, predict):
        fpr, tpr, threshold = roc_curve(truth, predict)
        return fpr, tpr

    # takes files, labels and disc value and outputs tpr and fprs for plotting. puts it all together
    def roccy(self, var, sigfile, bkgfile, siglabel, bkglabel, cutstr=''):
        # var is disc score
        #sig/bkgfile is signal/background file
        #siglabel is label that makes signal true
        #bkglabel is label that makes bkg true
        #cutstr is any additional selections
        
        sigarr = self.getarr(sigfile, cutstr)
        bkgarr = self.getarr(bkgfile, cutstr)
        
        truth,pred = self.preproc(var, siglabel, bkglabel, sigarr, bkgarr)
        fpr,tpr = self.getroc(truth, pred)
        
        return fpr, tpr
        
        


