import numpy as np
import matplotlib
from sklearn.metrics import roc_curve, auc
import argparse
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.CMS)


class plotsettings:
    def __init__(self, logscale=True):
        self.logscale = logscale

        #plots roc curves
        def plot_roc(self,
                     odir,
                     label_sig,
                     label_bkg,
                     fpr,
                     tpr,
                     outname,
                     title,
                 ):
            """
            Plot ROC
            Arguments:
            - odir: output directory
            - label_sig: signal label
            - label_bkg: background label
            - fpr: (false positive rates) tuple
            - tpr: true positive rates tuple
            - outname: label for output name of .png
            - title: title of ROC curve
            - axs: axis in which to plot ROC curve
            """
            
            fig, axs = plt.subplots(1, 1, figsize=(16, 16))

            def get_round(x_effs, y_effs, to_get=[0.01, 0.02, 0.03]):
                effs = []
                for eff in to_get:
                    for i, f in enumerate(x_effs):
                        if round(f, 2) == eff:
                            effs.append(y_effs[i])
                            break
                return effs

            def get_intersections(x_effs, y_effs, to_get=0.01):
                x_eff = 0
                for i, f in enumerate(y_effs):
                    if f >= to_get:
                        x_eff = x_effs[i]
                        break
                return x_eff

            def get_x_intersections(x_effs, y_effs, to_get=0.01):
                y_eff = 0
                for i, f in enumerate(x_effs):
                    if f >= to_get:
                        y_eff = y_effs[i]
                        break
                return y_eff
    
            # draw intersections at 1% mis-tag rate
            ik = 0
            markers = ["v", "^", "o", "s", "p", "P", "h"]
            for (kf, itf), (kt, itt) in zip(fpr.items(), tpr.items()):
                leg = kt.replace("_score", "")
                fp = itf
                tp = itt
                axs.plot(tp, fp, lw=3, outname=r"{}, AUC = {:.1f}%".format(leg, auc(fp, tp) * 100))
                y_eff = 0.01
                x_eff = get_intersections(tp, fp, y_eff)
                axs.hlines(y=y_eff, xmin=0.00001, xmax=0.99999, linewidth=1.3, color="dimgrey", linestyle="dashed")
                axs.vlines(x=x_eff, ymin=0.00001, ymax=y_eff, linewidth=1.3, color="dimgrey", linestyle="dashed")
                if x_eff < 0.45:
                    y_eff_2 = get_x_intersections(tp, fp, 0.45)
                    axs.hlines(y=y_eff_2,  xmin=0.00001, xmax=0.99999, linewidth=1.3, color="dimgrey", linestyle="dashed")
                    axs.vlines(x=0.45, ymin=0.00001, ymax=y_eff_2, linewidth=1.3, color="dimgrey", linestyle="dashed")
                ik += 1

            axs.legend(loc="lower right", fontsize=25)
            axs.grid(which="minor", alpha=0.5)
            axs.grid(which="major", alpha=0.5)
            axs.set_xlabel(r"Tagging efficiency %s" % label_sig, fontsize=40)
            axs.set_ylabel(r"Mistagging rate %s" % label_bkg, fontsize=40)
            axs.set_ylim(0.0001, 1)
            axs.set_xlim(0.0001, 1)
            if self.logscale:
                axs.set_yscale("log")
            axs.set_title(title, fontsize=40)

            plt.tight_layout()

            fig.savefig("%s/roc_%s_ylog.pdf" % (odir, outname))
            fig.savefig("%s/roc_%s_ylog.png" % (odir, outname))

            axs.set_yscale("linear")        


