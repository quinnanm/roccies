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

 #   def getlabel(self, labelarr):
 #       label = labelarr[0]+'==1'
 #       if len(labelarr)>1:
 #           for i in range(1,len(labelarr-1)):
 #               label += labelarr[i]+'==1 &'

 #       label += labelarr[i]+'==1' #last one
 #       print(label)
 #       return label
        
       # takes truth scores, outputs tpr and fpr 
    def rocrates(self, sigscores, bkgscores):
       # """
       #  We expect all scores to sum up to 1, e.g. given two signals in the event (signal 1 and 2) and one background process (background 1)
       #  score_signal_1 + score_signal_2 + score_background_1 = 1
       #  Then nn_signal_1 = score_signal_1 / (score_signal_1 + score_background_1) = score_signal_1 / (1 - score_signal_2)
       #  """
        #must be per one score
        #sigscores - events coming from signal, label applied
        #bkgscores - events coming from background, label applied
                
        #sigmask = sigarr[siglabel]==1
        #bkgmask = bkgarr[bkglabel]==1
        #print('siglabel '+siglabel)
        #print(len(sigscores)+' '+len(sigmask))
        # sigscores = sigarr[var][sigmask].to_numpy()             
        # bkgscores = bkgarr[var][bkgmask].to_numpy()
        #sigscores = sigscores[sigmask]#.to_numpy()
        #bkgscores = bkgscores[bkgmask]#.to_numpy()
        predict = np.concatenate((sigscores, bkgscores), axis=None)

        siglabels = np.ones(sigscores.shape)
        bkglabels = np.zeros(bkgscores.shape)
        truth = np.concatenate((siglabels, bkglabels), axis=None)
 
        #fpr, tpr, threshold = roc_curve(truth, predict)
        return fpr, tpr

    # takes files, labels and disc value and outputs tpr and fprs for plotting. puts it all together
#    def roccy(self, var, sigfile, bkgfile, siglabel, bkglabel, cutstr=''):
        # var is disc score
        #sig/bkgfile is signal/background file
        #siglabel is label that makes signal true
        #bkglabel is label that makes bkg true
        #cutstr is any additional selections
        
#        sigarr = self.getarr(sigfile, cutstr)
#        bkgarr = self.getarr(bkgfile, cutstr)
        
#        truth,pred = self.preproc(var, siglabel, bkglabel, sigarr, bkgarr)
#        fpr,tpr = self.getroc(truth, pred)
        
 #       return fpr, tpr
    
    #takes array and label selection and returns masked array of 1s and 0s according to whether label is true or not
    def labelmask(self, labels, array, branches=[]):
        #labels is labels you want to apply ["label1", "label2"]
        #array is array you are masking (converted from rootfile)
        #branches are variable/score you want to return
        
        if len(branches)<1:  
            branches = array.keys() #probably doesnt work
             
        #BEST WAY TO APPLY MULTIPLE LABELS?
        #nesting? look up later for lab in labels
        #mask=zeros(array) #NEED TO GET LENGTH TO INITIALIZE
         
        #change later -  for lab in labels?
        #or use uproot again and reconvert
        #or you have to apply mask with selection to the events, pre-array step. make "getevents" function or something
        #question: how to apply mask with condition involving multiple columns on an array?
        mask = array[labels]==1
        print("MASKING!!!!!!!!!!!!!!!!!!")
        print(mask)
        array = array[mask]
        print(array)
            
        maskarr = array[branches].to_numpy()
        print(maskarr)
    
        #maskarr = array.arrays(branches, labelsel) #code to mask that array #NEED TO DO
        return maskarr
    
    
    # takes files, labels and disc value and outputs tpr and fprs for plotting. puts it all together
    def roccy(self, barr, sarr, labels, blabels=['ttbar', 'wjets'], slabels=['Hmu', 'Hel'], plotvars=[], info=None):
        #barr is np array for signal
        #sarr is np array for background
        #slabel is label that makes signal true. should be array
        #blabel is label that makes bkg true
        #info is cache, optional
        #returns dictionary of tpr, fpr, info per slabel v blabel
              
        #add option to input var can be specific score you want to plot, needs to be same length as signal
        #current option is that var is set by slabels
        #add option to convert label to array if strings
        #make it so can input label strings directly if desired
        
        #construct label selection properly
        #default if plotvars is not specified is to use the signal scores        
        bkgarrs = ones_like(blabels)#initialize arrays
        sigarrs = ones_like(slabels)
        scores = np.ones_like(slabels)
        out = {}
               
        for i,s in enumerate(slabels):
            slab = labels[s+'_label']
            print('signal label to mask array '+slab)
           
            if len(plotvars)<1: # no set variable to plot, use defaults for variables/scores to plot
                print("no set variable to plot, using defaults according to signal labels")
                svar = labels[s+'_score']
                print('score to plot '+svar)
                scores[i] = svar
                 
                sscore = self.labelmask(slab, sarr, [svar]) #array of scores that pass the label            
                sigarrs[i] = sscore
                
                for j,b in enumerate(blabels):
                    blab = labels[b+'_label']
                    print('background label to mask array '+blab)
                    bscore = labelmask(blab, barr, [svar]) #array of scores that pass the label       
                    bkgarrs[i] = bscore
                    
                    fpr, tpr = self.rocrates(sscore, bscore)
                    key = s+'_v_'+b
                    out[key]={'fpr':fpr,'tpr':tpr}
                    
        return out, info
                    
                    
                    
                
                


        
        


