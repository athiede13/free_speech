"""
Plot second-largest clusters as subplots.

Created on Mon Sep 30 14:30:12 2019

@author: 
@author: 
"""

import matplotlib.pyplot as plt

#%matplotlib qt
#%matplotlib inline

#to fill

filepath = '/media/cbru/SMEDY/results/mantel_correlations/2019_05_simple_model/'
filenames1 = (
              filepath + 'z_max_1cluster_corr_5.000000e-01-4Hz_phon_1.png',
              filepath + 'z_max_1cluster_corr_4-8Hz_phon_1.png',
              filepath + 'z_max_1cluster_corr_8-12Hz_phon_1.png',
              filepath + 'z_max_1cluster_corr_12-25Hz_phon_1.png',
              filepath + 'z_max_1cluster_corr_55-90Hz_phon_1.png',
              filepath + 'z_max_1cluster_corr_5.000000e-01-4Hz_read_1.png',
              filepath + 'z_max_1cluster_corr_8-12Hz_read_1.png',
              filepath + 'z_max_1cluster_corr_25-45Hz_read_1.png',
              filepath + 'z_max_1cluster_corr_5.000000e-01-4Hz_mem_1.png',
              filepath + 'z_max_1cluster_corr_5.000000e-01-4Hz_iq_1.png'
              )

labels1 = ['phon delta', 'phon theta', 'phon alpha', 'phon beta', 
           'phon high gamma', 
           'read delta', 'read alpha', 'read low gamma', 
           'work mem delta',
           'IQ delta']
# delta \u03B4
# theta \u03B8
# alpha \u03B1
# beta \u03B2
# gamma \u03B3

#plot subplots

plt.rcParams['font.family'] = "serif"
fig1 = plt.figure(figsize=(20, 15))
fig1.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0.2)
i = 1

for file in filenames1:
    img = plt.imread(file, format='png')
    ax = fig1.add_subplot(3, 4, i)
    ax.imshow(img, aspect='equal')
    ax.axis('off')
    ax.text(0.6, 1, labels1[i-1], horizontalalignment='center',
            verticalalignment='center', transform=ax.transAxes, fontsize=17)
    i = i+1


fig1.suptitle("Second-largest clusters", fontsize=25, y=0.94)
plt.show()
fig1.savefig(filepath + 'z_second_largest_clusters.png', bbox_inches='tight', dpi=600)
fig1.savefig(filepath + 'z_second_largest_clusters.pdf', bbox_inches='tight', dpi=600)
fig1.clear()