import os
import numpy as np
import uproot

def getarr(infile='', cutstr='', branches=[], info={}, treename='Events'):
    #returns array of given var with selection applied
    #returns cache 'info' with infile, cutstr, and branches used
    #branches = [list of only branches you want to keep, optional]
    #info initialized if doesnt exist, or you can input the cache if it already exists

    print('file '+infile)
    print('cutstr '+cutstr)
    evts = uproot.open(infile)[treename]
    print(evts)
    if len(branches)<1:  
        branches = evts.keys()
    print(branches)
    events = evts.arrays(branches, cutstr)
    nocut  = evts.arrays(branches)

    info['branches']= branches
    info['infile']= infile
    info['cutstr']= cutstr
    
    #print(events)      
    return events, info


#def getyield(hist, verbose=False):
   # errorVal = r.Double(0)
   # minbin=0
   # maxbin=hist.GetNbinsX()+1
   # hyield = hist.IntegralAndError(minbin, maxbin, errorVal)
  #  if verbose:
    #    print 'yield:', round(hyield, 3), '+/-', round(errorVal, 3), '\n'
  #  return hyield,  errorVal


