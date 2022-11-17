import numpy as np
import matplotlib
import argparse
import matplotlib.pyplot as plt
import ROOT as r
from ROOT import gStyle
gStyle.SetOptStat(0)
r.gROOT.SetBatch(True)

from rocstuff import *
from plotsettings import *

rs = rocstuff()
ps = plotsettings()

#define files:
#first one ucsd, second one pku
files = {'bulkg':{'ucsd':'./rootfiles/ucsd/bulkg-3.root',
                  'pku':'./rootfiles/pku/bulkg_pku.root'},
         'hww':{'ucsd':'./rootfiles/ucsd/hww-2.root',
                'pku':'./rootfiles/pku/hww_pku.root'},
         'jhu':{'ucsd':'./rootfiles/ucsd/jhu-4.root',
                'pku':'./rootfiles/pku/jhu_pku.root'},
         'qcd':{'ucsd':'./rootfiles/ucsd/qcd-3.root',
                'pku':'./rootfiles/pku/qcd_pku.root'},
         'ttbar':{'ucsd':'./rootfiles/ucsd/ttbar-6.root',
                  'pku':'./rootfiles/pku/ttbar_pku.root'},
         'wjets':{'ucsd':'./rootfiles/ucsd/wjets-4.root',
                  'pku':'./rootfiles/pku/wjets_pku.root'}}


#selection same as training/inference presel
basesel = 'fj_pt>200 && fj_pt<2500 && fj_msoftdrop>=20 && fj_msoftdrop<260 && abs(fj_eta)<2.4'
    # (fj_pt<2500) &
    # (np.absolute(fj_eta)<2.4) &
    # (fj_msoftdrop>=20) &
    # (fj_msoftdrop<260) &
    # (   ( (fj_Top_2q==1) |
    #       (fj_Top_elenu==1) |
    #       (fj_Top_munu==1) |
    #       (fj_Top_taunu==1) ) |
    #     ( (fj_V_2q==1) |
    #       (fj_V_elenu==1) |
    #       (fj_V_munu==1) |
    #       (fj_V_taunu==1) ) |
    #     ( ( (fj_isQCDb==1) |
    #       (fj_isQCDbb==1) |
    #       (fj_isQCDc==1) |
    #       (fj_isQCDcc==1) |
    #       (fj_isQCDothers == 1) ) &
    #     (fj_genRes_mass<=0) ) |
    #   ( ((fj_H_VV_elenuqq==1) | (fj_H_VV_munuqq==1) | (fj_H_VV_leptauelvqq==1) | (fj_H_VV_leptaumuvqq==1) | (fj_H_VV_hadtauvqq==1)) &
    #     (fj_nprongs>1) &
    #     (fj_lepinprongs==1) &
    #     (fj_genRes_mass>0) ) ))

#caches
pku = {}
ucsd = {}
  
##########################################################
##########################################################
#pku

Hlabel_pku= ["label_H_WqqWqq_0c","label_H_WqqWqq_1c","label_H_WqqWqq_2c","label_H_WqqWq_0c","label_H_WqqWq_1c","label_H_WqqWq_2c","label_H_WqqWev_0c","label_H_WqqWev_1c","label_H_WqqWmv_0c","label_H_WqqWmv_1c","label_H_WqqWtauev_0c","label_H_WqqWtauev_1c","label_H_WqqWtaumv_0c","label_H_WqqWtaumv_1c","label_H_WqqWtauhv_0c","label_H_WqqWtauhv_1c"]

SUMscore_pku = "( score_label_H_WqqWqq_0c + score_label_H_WqqWqq_1c + score_label_H_WqqWqq_2c + score_label_H_WqqWq_0c + score_label_H_WqqWq_1c + score_label_H_WqqWq_2c + score_label_H_WqqWev_0c + score_label_H_WqqWev_1c + score_label_H_WqqWmv_0c + score_label_H_WqqWmv_1c + score_label_H_WqqWtauev_0c + score_label_H_WqqWtauev_1c + score_label_H_WqqWtaumv_0c + score_label_H_WqqWtaumv_1c + score_label_H_WqqWtauhv_0c + score_label_H_WqqWtauhv_1c + score_label_QCD_bb + score_label_QCD_cc + score_label_QCD_b + score_label_QCD_c + score_label_QCD_others + score_label_Top_bWqq_0c + score_label_Top_bWqq_1c + score_label_Top_bWq_0c + score_label_Top_bWq_1c + score_label_Top_bWev + score_label_Top_bWmv + score_label_Top_bWtauhv + score_label_Top_bWtauev + score_label_Top_bWtaumv + score_label_Wqq_jets_1c + score_label_Wqq_jets_0c )"

HSUM_pku = "(score_label_H_WqqWqq_0c + score_label_H_WqqWqq_1c + score_label_H_WqqWqq_2c + score_label_H_WqqWq_0c + score_label_H_WqqWq_1c + score_label_H_WqqWq_2c + score_label_H_WqqWev_0c + score_label_H_WqqWev_1c + score_label_H_WqqWmv_0c + score_label_H_WqqWmv_1c + score_label_H_WqqWtauev_0c + score_label_H_WqqWtauev_1c + score_label_H_WqqWtaumv_0c + score_label_H_WqqWtaumv_1c + score_label_H_WqqWtauhv_0c + score_label_H_WqqWtauhv_1c)"

Hscore_pku = HSUM_pku+'/'+SUMscore_pku

pku['Hmu_score'] = "(score_label_H_WqqWmv_0c + score_label_H_WqqWmv_1c)/"+SUMscore_pku
pku['Hel_score'] = "(score_label_H_WqqWev_0c + score_label_H_WqqWev_1c)/"+SUMscore_pku
pku['Hlep_score'] = "(score_label_H_WqqWev_0c + score_label_H_WqqWev_1c + score_label_H_WqqWmv_0c + score_label_H_WqqWmv_1c)/"+SUMscore_pku
pku['Htau_score'] = "(score_label_H_WqqWtauev_0c + score_label_H_WqqWtauev_1c + score_label_H_WqqWtaumv_0c + score_label_H_WqqWtaumv_1c + score_label_H_WqqWtauhv_0c + score_label_H_WqqWtauhv_1c)/"+SUMscore_pku
pku['Hmu_label'] = ["label_H_WqqWmv_0c","label_H_WqqWmv_1c"]
pku['Hel_label'] = ["label_H_WqqWev_0c","label_H_WqqWev_1c"]
pku['Hlep_label'] = ["label_H_WqqWev_0c","label_H_WqqWev_1c","label_H_WqqWmv_0c","label_H_WqqWmv_1c"]
pku['Htau_label'] = ["label_H_WqqWtauev_0c","label_H_WqqWtauev_1c","label_H_WqqWtaumv_0c","label_H_WqqWtaumv_1c","label_H_WqqWtauhv_0c","label_H_WqqWtauhv_1c"]

#specific taus
# Htaumu_score_pku = "(score_label_H_WqqWtaumv_0c + score_label_H_WqqWtaumv_1c)"
# Htauel_score_pku = "(score_label_H_WqqWtauev_0c + score_label_H_WqqWtauev_1c)"
# Htauhad_score_pku = "(score_label_H_WqqWtauhv_0c + score_label_H_WqqWtauhv_1c)"

#PKU BACKGROUNDS#########################
pku['QCD_score'] = "(score_label_QCD_bb + score_label_QCD_cc + score_label_QCD_b + score_label_QCD_c + score_label_QCD_others)/"+SUMscore_pku 
pku['W_score'] = "(score_label_Wqq_jets_1c + score_label_Wqq_jets_0c)/"+SUMscore_pku 
pku['T_score'] = "(score_label_Top_bWqq_0c + score_label_Top_bWqq_1c + score_label_Top_bWq_0c + score_label_Top_bWq_1c + score_label_Top_bWev + score_label_Top_bWmv + score_label_Top_bWtauhv + score_label_Top_bWtauev + score_label_Top_bWtaumv)/"+SUMscore_pku 
pku['lepT_score'] = "(score_label_Top_bWev + score_label_Top_bWmv)/"+SUMscore_pku 
pku['lepW_score'] = "(score_label_Wqq_jets_1c + score_label_Wqq_jets_0c)/"+SUMscore_pku  ##?? #just W with sel

pku['QCD_label'] = ["label_QCD_bb","label_QCD_cc","label_QCD_b","label_QCD_c","label_QCD_others"]
pku['W_label'] = ["label_Wqq_jets_1c","label_Wqq_jets_0c"] 
pku['T_label'] = ["label_Top_bWqq_0c","label_Top_bWqq_1c","label_Top_bWq_0c","label_Top_bWq_1c","label_Top_bWev","label_Top_bWmv","label_Top_bWtauhv","label_Top_bWtauev","label_Top_bWtaumv"] 
pku['lepT_label'] = ["label_Top_bWev","label_Top_bWmv"] 
pku['lepW_label'] = ["fj_wjets_label"]  #??

##########################################################
##########################################################
# ucsd
# fj_ttbar_label, fj_wjets_label, fj_isHVV_elenuqq, fj_isHVV_munuqq, fj_H_VV_leptauelvqq, fj_H_VV_leptaumuvqq, fj_H_VV_hadtauvqq

SUMscore_ucsd = "(score_fj_ttbar_label + score_fj_wjets_label + score_fj_isHVV_elenuqq + score_fj_isHVV_munuqq + score_fj_H_VV_leptauelvqq + score_fj_H_VV_leptaumuvqq + score_fj_H_VV_hadtauvqq)"
Hscore_ucsd  = "(score_fj_isHVV_elenuqq + score_fj_isHVV_munuqq + score_fj_H_VV_leptauelvqq + score_fj_H_VV_leptaumuvqq + score_fj_H_VV_hadtauvqq)/"+SUMscore_ucsd
Hlabel_ucsd = ["fj_isHVV_elenuqq","fj_isHVV_munuqq","fj_H_VV_leptauelvqq","fj_H_VV_leptaumuvqq","fj_H_VV_hadtauvqq"]

ucsd['Hmu_score'] = "score_fj_isHVV_munuqq"
ucsd['Hel_score'] = "(score_fj_isHVV_elenuqq)"
ucsd['Hlep_score'] = "(score_fj_isHVV_munuqq + score_fj_isHVV_elenuqq)/"+SUMscore_ucsd
ucsd['Htau_score'] = "(score_fj_H_VV_leptauelvqq + score_fj_H_VV_leptaumuvqq + score_fj_H_VV_hadtauvqq)/"+SUMscore_ucsd

ucsd['Hmu_label'] = ["fj_isHVV_munuqq"]
ucsd['Hel_label'] = ["fj_isHVV_elenuqq"]
ucsd['Hlep_label'] = ["fj_isHVV_munuqq","fj_isHVV_elenuqq"]
ucsd['Htau_label'] = ["fj_H_VV_leptauelvqq","fj_H_VV_leptaumuvqq","fj_H_VV_hadtauvqq"]

#bkgs ucsd
ucsd['QCD_score'] = "(1.0 - (score_fj_isHVV_elenuqq + score_fj_isHVV_munuqq + score_fj_H_VV_leptauelvqq + score_fj_H_VV_leptaumuvqq + score_fj_H_VV_hadtauvqq))/"+SUMscore_ucsd #?? #NOT signal basically
ucsd['W_score'] = "(score_fj_wjets_label)"
ucsd['T_score'] = "score_fj_ttbar_label"
ucsd['lepT_score'] = "(score_fj_wjets_label)"  #?? #just W with sel
ucsd['lepW_score'] = "(score_fj_ttbar_label)" #?? #just T with sel

ucsd['QCD_label'] = ["fj_QCD_label"]
ucsd['W_label'] = ["fj_wjets_label"]
ucsd['T_label'] = ["fj_ttbar_label"]
ucsd['lepT_label'] = ["fj_ttbar_label"]
ucsd['lepW_label'] = ["fj_wjets_label"]


############# special selections
procs = ['Hmu', 'Hel', 'Htau', 'Hlep', 'QCD', 'W', 'T', 'lepT', 'lepW']
for proc in procs:
    setsel = basesel
    if 'H' in proc:
        setsel = basesel+' && fj_nprongs>1 && fj_lepinprongs==1 && fj_genRes_mass>0'
    pku[proc+'_sel']=basesel #default sel
    ucsd[proc+'_sel']=basesel

#specal selections #should be in labels!
# pku['lepW_sel']=basesel+' & fj_wjets_lepmerged==1'
# pku['lepW_sel']=basesel+' & fj_wjets_lepmerged==1'
# ucsd['lepW_sel']=basesel+' & fj_wjets_lepmerged==1'
# ucsd['lepW_sel']=basesel+' & fj_wjets_lepmerged==1'
# pku['QCD']=basesel+' & fj_genRes_mass<=0'
# ucsd['QCD']=basesel+' & fj_genRes_mass<=0'

#iso sels
pku['isosel']=' && lep_iso<0.3'
pku['minisel']=' && lep_miniiso<0.2'
pku['bothsel']=' && lep_iso<0.3 && lep_miniiso<0.2'
ucsd['isosel']=' && lep_iso<0.3'
ucsd['minisel']=' && lep_miniiso<0.2'
ucsd['bothsel']=' && lep_iso<0.3 && lep_miniiso<0.2'

############### plot scores ( logscale hists)


############### plot rocs ( logscale rocs)

#el, mu, tau vs. ttbar
fpru, tpru = rs.roccy(ucsd['Hmu_score'], files['hww']['ucsd'], files['ttbar']['ucsd'], ucsd['Hmu_label'], ucsd['T_label'], cutstr=basesel)
fprp, tprp = rs.roccy(pku['Hmu_score'], files['hww']['pku'], files['ttbar']['pku'], pku['Hmu_label'], pku['T_label'], cutstr=basesel)
print fpru, tpru, fprp, tprp
#ps.plot_roc(odir, label_sig, label_bkg, fpr, tpr, outname, title):

#el, mu, tau vs. ttbar lepinjet
#el, mu, tau vs. wjets
#el, mu, tau vs. wjets lepinjet
#el, mu, tau vs. qcd
#el, mu, tau vs, ttbar + iso
#el, mu, tau vs, ttbar + mini
#el, mu, tau vs, ttbar + iso + mini
#el, mu, tau vs, wjets + iso
#el, mu, tau vs, wjets + mini
#el, mu, tau vs, wjets + iso + mini
