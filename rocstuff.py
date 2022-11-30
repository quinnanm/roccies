import numpy as np
import matplotlib
import argparse
import matplotlib.pyplot as plt

import pandas as pd
import uproot
import matplotlib.colors as mcolors
import hist as hist
plt.rcParams.update({'font.size': 20})
from sels import *

class rocstuff:
    def __init__(self):
        #general settings
        self.treename = 'Events'

    def getlabel(self, labelarr):
        label = labelarr[0]+'==1'
        if len(labelarr)>1:
            for i in range(1,len(labelarr-1)):
                label += labelarr[i]+'==1 &'

        label += labelarr[i]+'==1' #last one
        print(label)
        return label
        
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
        siglabel=self.getlabel(siglabelarr)
        bkglabel=self.getlabel(bkglabelarr)

        #complaining about masks
        sigscores = sigarr[var]#.to_numpy()
        bkgscores = bkgarr[var]#.to_numpy()
        
        sigmask = sigarr[siglabel]==1
        bkgmask = bkgarr[bkglabel]==1
        print('siglabel '+siglabel)
        print(len(sigscores)+' '+len(sigmask))
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
        
        


