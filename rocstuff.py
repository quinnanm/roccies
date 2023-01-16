import numpy as np
import matplotlib
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

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
                
        predict = np.concatenate((sigscores, bkgscores), axis=None)

        siglabels = np.ones(sigscores.shape)
        bkglabels = np.zeros(bkgscores.shape)       
        truth = np.concatenate((siglabels, bkglabels), axis=None)
        
        print('predict'+str(predict))
        print('truth'+str(truth))
 
        fpr, tpr, threshold = roc_curve(truth, predict)
    
        return fpr, tpr
 

    #just divides numerator and denominator to construct score from masked array
    def constructscore(self, array, numlist, denlist):
        #ex: pku['Hmu_score'] = "(score_label_H_WqqWmv_0c + score_label_H_WqqWmv_1c)/"+SUMscore_pku

        print('constructing score')       
        #constructs needed score given list and array
        def sumscore(scorelist, array):
            #print(str(scorelist))
            outscore = np.zeros(len(array[scorelist[0]]))
        
            for sc in scorelist:
                outscore = np.add(outscore, array[sc])
            outscore = (outscore)

            return outscore

        num = sumscore(numlist, array)        
        if len(numlist)<2:
            num = num.astype(float)
            print('SCORE DEFINED AS: '+str(numlist))
            return (num) #score is just the numerator score if there is only one score in list
        
        den = sumscore(denlist, array)
        score = np.divide((num), (den)) #else you have to divide by total scores       
        score = score.astype(float)
        print('SCORE DEFINED AS: SUM('+str(numlist)+') / SUM('+str(denlist)+')')
        
        return score
        
    #takes array and label selection and returns masked array of 1s and 0s according to whether label is true or not
    def labelmask(self, label, array, branches=[]):
        #labels is labels you want to apply ["label1", "label2"]
        #array is array you are masking (converted from rootfile)
        #branches are variable/score you want to return
        
        if len(branches)<1:  
            branches = array.keys()
            
        #label is list of labels to apply. need to construct appropriately
        mask = array[label[0]]==1 #first element
        
        for i,lab in enumerate(label[1:]):
            mask = (mask) | (array[lab]==1)          
            print('mask '+str(mask))           
            
        array = array[mask]
        print("MASKING WITH LABEL: "+str(label)+str(mask))           
        maskarr = array[branches]#.to_numpy()
       
        #Make it array of just scores so numpy likes it
        print(maskarr.dtype.names)
        print("NEW ARRAY: "+str(maskarr))
        
        return maskarr
    
    
    # takes files, labels and disc value and outputs tpr and fprs for plotting. puts it all together
    def roccy(self, sarr, barr, labels, slabels=['Hmu', 'Hel'], blabels=['T', 'W'], plotvars=[], info=None):
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
        #bkgarrs = [None] * len(blabels) #initialize lists
        #sigarrs = [None] * len(slabels)
        #scores = [None] * len(slabels)
 
        out = {}        
        #allscores = labels['SUM_score'] #deniminator needs to be sig+background for that roc curve in particular
        scorebranches = labels['SUM_score']
        
        for i,s in enumerate(slabels):
            slab = labels[s+'_label']
            print('signal label to mask array '+str(slab))
           
            if len(plotvars)<1: # no set variable to plot, use defaults for variables/scores to plot
                print("no set variable to plot, using defaults according to signal labels")
                svar = labels[s+'_score']
                
                print('score to plot '+str(svar))
                #scores[i] = svar
                                 
                for j,b in enumerate(blabels):
                    blab = labels[b+'_label']
                    print('background label to mask array '+str(blab))
                    
                    #denominator score is signal+background scores
                    bvar = labels[b+'_score']
                    denvars = svar+bvar
                    print('DENVAR'+str(denvars)+'\n')
                    
                    sscorearr = self.labelmask(slab, sarr, scorebranches) #array of scores that pass the label      
                    sscore = self.constructscore(sscorearr, svar, denvars) #then construct the score as sum if needed
                    #sigarrs[i] = sscore
                    
                    bscorearr = self.labelmask(blab, barr, scorebranches) #array of scores that pass the label
                    bscore = self.constructscore(bscorearr, svar, denvars) #then construct the score as sum if needed
                    #bkgarrs[i] = bscore
                    
                    fpr, tpr = self.rocrates(sscore, bscore)
                    key = s+'_v_'+b
                    out[key]={'fpr':fpr,'tpr':tpr}
                    
        return out, info
                    
                    
                    
                
                


        
        


