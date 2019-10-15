"""
Plot subplots.

Created on 6.5.2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import matplotlib.pyplot as plt

#%matplotlib qt
#%matplotlib inline

#to fill

filepath = '/media/cbru/SMEDY/results/ISCs_comp_against_0/'
con = 'speech'

files = ('/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_5.000000e-01-4Hz_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_5.000000e-01-4Hz_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_5.000000e-01-4Hz_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_5.000000e-01-4Hz_med-rh.jpg',
             
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_4-8Hz_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_4-8Hz_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_4-8Hz_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_4-8Hz_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_8-12Hz_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_8-12Hz_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_8-12Hz_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_8-12Hz_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_12-25Hz_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_12-25Hz_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_12-25Hz_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_12-25Hz_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_25-45Hz_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_25-45Hz_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_25-45Hz_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_25-45Hz_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_55-90Hz_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_55-90Hz_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_55-90Hz_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/overlap_55-90Hz_med-rh.jpg'

             )

#plot subplots
plt.rcParams['font.family'] = "serif"
fig = plt.figure(figsize=(12, 13))

positions = {3, 7, 11, 15, 19, 23}
legend = ('', '', '', 'delta (0.5\u20134 Hz)',
          '', '', '', 'theta (4\u20138 Hz)',
          '', '', '', 'alpha (8\u201312 Hz)',
          '', '', '', 'beta (12\u201325 Hz)',
          '', '', '', 'low gamma (25\u201345 Hz)',
          '', '', '', 'high gamma (55\u201390 Hz)'
          )

# delta \u03B4
# theta \u03B8
# alpha \u03B1
# beta \u03B2
# gamma \u03B3
i=1
for file in files:
    img = plt.imread(file, format='jpg')
    ax = fig.add_subplot(6,4,i)
    ax.imshow(img, aspect = 'equal')
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
    if i in {1,3}:
        ax.text(0.5, 1.2, 'lh', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=15)
    if i in {2,4}:
        ax.text(0.5, 1.2, 'rh', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=15)
    plt.set_cmap('hot')
    i=i+1

fig.tight_layout()
fig.subplots_adjust(wspace=0, hspace=0)
fig.suptitle("Overlap of T-statistics of ISCs during speech", fontsize=25, x=0.5, y=1.12)
plt.show()
fig.savefig(filepath + 'overlap_T_' + con + '_ISC.pdf', dpi=600, bbox_inches='tight')
fig.savefig(filepath + 'overlap_T_' + con + '_ISC.png', dpi=600, bbox_inches='tight')
