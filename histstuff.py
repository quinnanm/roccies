import numpy as np
import matplotlib
import argparse
import matplotlib.pyplot as plt

import pandas as pd
import uproot
import matplotlib.colors as mcolors
from hist import Hist
import hist as hs
import mplhep as hep

plt.rcParams.update({'font.size': 20})
from utils import *

class histstuff:
    def __init__(self):
        print('init')
        #general settings
        # self.indir = indir
        self.nbins = 100
        self.xmin = 0.0
        self.xmax = 1.0
        self.treename = 'Events'
        self.logscale = True
        self.outdir = './plots/hists/'
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        self.savetype = 'png' #(png or pdf)
        
    def initcache(self):
        #initializes info cache for histogram info 
        info = {}
        info['title'] = 'hist'
        info['year'] = '2017'
        info['note'] = ''
        return info
        
    def prettyhists(self, hists, info, hname='hist', show=False):
        #hists is a dictionary of name:hist
        #info contains dict of extra information
        #could be one or multiple (non stacked) hists
        #just some settings for pretty histograms
        
        #qualitative colormaps from https://matplotlib.org/stable/tutorials/colors/colormaps.html
        cmap = plt.get_cmap('Set3') #9 pastels
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        for i, (lab, hist) in enumerate(hists.items()):
            hep.histplot(
                hist, 
                ax=ax, 
                label=lab,
                linewidth=3,
                color=cmap(i))
            
        #hep.cms.lumitext(f"{info['year']} (13 TeV)", ax=ax)
        hep.cms.text("Work in Progress", ax=ax)
        #ax.legend(title=info['title'])  
        ax.legend()
        
        #labels
        plt.xlabel(info['title'])
        plt.ylabel('Entries')
        
        if self.logscale:
            ax.set_yscale('log')
            plt.savefig(self.outdir+'/1dhist_'+hname+'_'+info['note']+'_log.'+self.savetype)
        else:
            plt.savefig(self.outdir+'/1dhist_'+hname+'_'+info['note']+'.'+self.savetype)
        if show:
            plt.show()         
        plt.close()
        
           
    def gethist(self, arr, info, weight=None, ax=[], plot=True):
        #info is cache with minimally {'var':varname, 'proc':proc}
        #makes single hist, saves as pdf or png in dedicated outdir
        #arr has to be a np array of a single variable (for example pt from one rootfile) with selections already applied
        #weight should be a np array of weights
        if len(ax)!=3:
            print('setting to default ax = [nbins, xmin, xmax]')
            ax = [self.nbins, self.xmin, self.xmax]
        
        var = info['var']; proc = info['proc'] #variable and process you are plotting
        print('making hist out of '+var+' with process '+proc)
        h = Hist(hs.axis.Regular(ax[0], ax[1], ax[2], name='hist'))
       
        #defaults
        if weight is None:
            weight = np.ones_like(arr)
           
        #optional info for plotting
        htitle = proc+'-'+var
        info['title'] = htitle
        
        #fill the hist
        hist = {}
        hist[htitle]=h.fill(arr, weight=weight)
                
        #plot the hist
        if plot:
            self.prettyhists(hist, info, hname=htitle, show=True)
        else:
            self.prettyhists(hist, info, hname=htitle, show=False)
            
        return hist, info


        


