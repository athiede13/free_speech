"""
Plot subplots.

Created on Tue Sep  4 16:21:37 2018
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import matplotlib.pyplot as plt

#%matplotlib qt
#%matplotlib inline

#to fill

filepath = '/media/cbru/SMEDY/results/mantel_correlations/2019_05_simple_model/'
filenames1 = (filepath + 'phon_clu_5.000000e-01-4Hz_613_1_lat-lh.png',
              filepath + 'phon_clu_5.000000e-01-4Hz_613_1_lat-rh.png',
              filepath + 'max_cluster_corr_5.000000e-01-4Hz_phon_1.png',
              filepath + 'phon_clu_4-8Hz_613_1_lat-lh.png',
              filepath + 'phon_clu_4-8Hz_613_1_lat-rh.png',
              filepath + 'max_cluster_corr_4-8Hz_phon_1.png',
              filepath + 'phon_clu_8-12Hz_613_1_med-lh.png',
              filepath + 'phon_clu_8-12Hz_613_1_med-rh.png',
              filepath + 'max_cluster_corr_8-12Hz_phon_1.png',
              filepath + 'phon_clu_12-25Hz_613_1_lat-lh.png',
              filepath + 'phon_clu_12-25Hz_613_1_lat-rh.png',
              filepath + 'max_cluster_corr_12-25Hz_phon_1.png',
              filepath + 'phon_clu_55-90Hz_613_1_lat-lh.png',
              filepath + 'phon_clu_55-90Hz_613_1_lat-rh.png',
              filepath + 'max_cluster_corr_55-90Hz_phon_1.png'
              )

filenames2 = (filepath + 'read_clu_5.000000e-01-4Hz_613_1_lat-lh.png',
              filepath + 'read_clu_5.000000e-01-4Hz_613_1_lat-rh.png',
              filepath + 'max_cluster_corr_5.000000e-01-4Hz_read_1.png',
              filepath + 'read_clu_8-12Hz_613_1_med-lh.png',
              filepath + 'read_clu_8-12Hz_613_1_med-rh.png',
              filepath + 'max_cluster_corr_8-12Hz_read_1.png',
              filepath + 'read_clu_25-45Hz_613_1_lat-lh.png',
              filepath + 'read_clu_25-45Hz_613_1_lat-rh.png',
              filepath + 'max_cluster_corr_25-45Hz_read_1.png',
              filepath + 'mem_clu_5.000000e-01-4Hz_613_1_lat-lh.png',
              filepath + 'mem_clu_5.000000e-01-4Hz_613_1_lat-rh.png',
              filepath + 'max_cluster_corr_5.000000e-01-4Hz_mem_1.png'
              )

filenames3 = (filepath + 'iq_clu_5.000000e-01-4Hz_613_1_lat-lh.png',
              filepath + 'iq_clu_5.000000e-01-4Hz_613_1_lat-rh.png',
              filepath + 'max_cluster_corr_5.000000e-01-4Hz_iq_1.png',
              )

labels1 = ['delta ', '', '',
           'theta ', '', '',
           'alpha ', '', '',
           'beta ', '', '',
           'high gamma ', '', ''
           ]
labels2 = ['delta ', '', '',
           'alpha ', '', '',
           'low gamma ', '', '',
           'delta','','']
labels3 = ['delta ', '', '']
# delta \u03B4
# theta \u03B8
# alpha \u03B1
# beta \u03B2
# gamma \u03B3

#plot subplots

plt.rcParams['font.family'] = "serif"
fig1 = plt.figure(figsize=(15, 25))
fig1.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)
i = 1

for file in filenames1:
    img = plt.imread(file, format='png')
    ax = fig1.add_subplot(len(filenames1)/3, 3, i)
    ax.imshow(img, aspect='equal')
    ax.axis('off')
    ax.text(1.01, 1.03, labels1[i-1], horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes, fontsize=17)
    if i == 2:
        ax.text(0.5, 1.2, 'phonological processing', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=25)
    i = i+1


fig1.suptitle("Regressions of speech ISCs with", fontsize=25, y=0.935)
plt.show()
fig1.savefig(filepath + 'summary_speech_correlations1.png', bbox_inches='tight', dpi=600)
fig1.savefig(filepath + 'summary_speech_correlations1.pdf', bbox_inches='tight', dpi=600)
fig1.clear()

fig2 = plt.figure(figsize=(15, 20))
fig2.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)
i = 1

for file in filenames2:
    img = plt.imread(file, format='png')
    ax = fig2.add_subplot(len(filenames2)/3, 3, i)
    ax.imshow(img, aspect='equal')
    ax.axis('off')
    ax.text(1.01, 1.03, labels2[i-1], horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes, fontsize=17)
    if i == 2:
        ax.text(0.5, 1.2, 'technical reading', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=25)
    if i == 11:
        ax.text(0.5, 1.08, 'working memory', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=25)
    i = i+1

fig2.suptitle("Regressions of speech ISCs with", fontsize=25, y=0.95)
plt.show()
fig2.savefig(filepath + 'summary_speech_correlations2.png', bbox_inches='tight', dpi=600)
fig2.savefig(filepath + 'summary_speech_correlations2.pdf', bbox_inches='tight', dpi=600)
fig2.clear()

fig3 = plt.figure(figsize=(15, 5))
fig3.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)
i = 1

for file in filenames3:
    img = plt.imread(file, format='png')
    ax = fig3.add_subplot(len(filenames3)/3, 3, i)
    ax.imshow(img, aspect='equal')
    ax.axis('off')
    ax.text(1.01, 1.03, labels3[i-1], horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes, fontsize=17)
    if i == 2:
        ax.text(0.5, 1.18, 'IQ', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=25)
    i = i+1

fig3.suptitle("Regressions of speech ISCs with", fontsize=25, y=1.15)
plt.show()
fig3.savefig(filepath + 'summary_speech_correlations3.png', bbox_inches='tight', dpi=600)
fig3.savefig(filepath + 'summary_speech_correlations3.pdf', bbox_inches='tight', dpi=600)
fig3.clear()
