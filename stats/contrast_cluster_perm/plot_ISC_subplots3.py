"""
Plot subplots.

Created on Tue Sep  4 16:21:37 2018
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import matplotlib.pyplot as plt

#%matplotlib qt
#%matplotlib inline

#to fill

filepath = '/media/cbru/SMEDY/results/dys_con_contrast/2020_02_redo_subject_perm/'
con = 'speech'
files = (filepath + 'clu_5.000000e-01-4Hz_613_1_lat-lh.png',
         filepath + 'clu_5.000000e-01-4Hz_613_1_lat-rh.png',
         filepath + 'clu_5.000000e-01-4Hz_613_1_med-lh.png',
         filepath + 'clu_5.000000e-01-4Hz_613_1_med-rh.png',
         filepath + 'clu_4-8Hz_613_1_lat-lh.png', # no significant clusters for theta with Bonf-corr
         filepath + 'clu_4-8Hz_613_1_lat-rh.png',
         filepath + 'clu_4-8Hz_613_1_med-lh.png',
         filepath + 'clu_4-8Hz_613_1_med-rh.png',
#         filepath + 'clu_8-12Hz_613_1_lat-lh.png', # no significant clusters for alpha with maximal cluster correction
#         filepath + 'clu_8-12Hz_613_1_lat-rh.png',
#         filepath + 'clu_8-12Hz_613_1_med-lh.png',
#         filepath + 'clu_8-12Hz_613_1_med-rh.png',
         filepath + 'clu_12-25Hz_613_1_lat-lh.png',
         filepath + 'clu_12-25Hz_613_1_lat-rh.png',
         filepath + 'clu_12-25Hz_613_1_med-lh.png',
         filepath + 'clu_12-25Hz_613_1_med-rh.png',
         filepath + 'clu_25-45Hz_613_1_lat-lh.png',
         filepath + 'clu_25-45Hz_613_1_lat-rh.png',
         filepath + 'clu_25-45Hz_613_1_med-lh.png',
         filepath + 'clu_25-45Hz_613_1_med-rh.png',
         filepath + 'clu_55-90Hz_613_1_lat-lh.png',
         filepath + 'clu_55-90Hz_613_1_lat-rh.png',
         filepath + 'clu_55-90Hz_613_1_med-lh.png',
         filepath + 'clu_55-90Hz_613_1_med-rh.png'
         )

#plot subplots
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['Verdana',
                                   'Geneva',
                                   'Lucid',
                                   'Arial',
                                   'Helvetica',
                                   'Avant Garde',
                                   'sans-serif']
fig = plt.figure(figsize=(12, 13))
fig.tight_layout()
fig.subplots_adjust(wspace=0, hspace=0)
i = 1

positions = {3, 7, 11, 15, 19, 23}
legend = ('', '', '', 'delta',
          '', '', '', 'theta',
#          '', '', '', 'alpha',
          '', '', '', 'beta',
          '', '', '', 'low gamma',
          '', '', '', 'high gamma'
          )

# delta \u03B4
# theta \u03B8
# alpha \u03B1
# beta \u03B2
# gamma \u03B3
for file in files:
    img = plt.imread(file, format='png')
    ax = fig.add_subplot(6, 4, i)
    ax.imshow(img, aspect='equal')
    ax.axis('off')
    if i in positions:
        ax.text(-0.2, 1, legend[i], horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=17)
    if i == 2:
        ax.text(-0.1, 1.4, 'lateral', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=22)
    if i == 4:
        ax.text(-0.1, 1.4, 'medial', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=22)
    if i in {1, 3}:
        ax.text(0.5, 1.2, 'lh', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=15)
    if i in {2, 4}:
        ax.text(0.5, 1.2, 'rh', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=15)
    plt.set_cmap('hot')
    i = i+1

fig.suptitle("ISC group contrasts", fontsize=25, x=0.5, y=1)
plt.show()
fig.savefig(filepath + 'summary_t_contrast_' + con + '_ISCs3.pdf', dpi=600, bbox_inches='tight')
fig.savefig(filepath + 'summary_t_contrast_' + con + '_ISCs3.png', dpi=600, bbox_inches='tight')
