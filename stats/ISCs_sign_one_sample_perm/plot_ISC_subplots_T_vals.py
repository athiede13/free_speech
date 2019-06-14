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
files = ('/media/cbru/SMEDY/results/ISCs_comp_against_0/con_5.000000e-01-4Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_5.000000e-01-4Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_5.000000e-01-4Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_5.000000e-01-4Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/white.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_5.000000e-01-4Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_5.000000e-01-4Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_5.000000e-01-4Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_5.000000e-01-4Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar1.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_4-8Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_4-8Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_4-8Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_4-8Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/white.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_4-8Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_4-8Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_4-8Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_4-8Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar2.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_8-12Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_8-12Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_8-12Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_8-12Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/white.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_8-12Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_8-12Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_8-12Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_8-12Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar3.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_12-25Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_12-25Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_12-25Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_12-25Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/white.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_12-25Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_12-25Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_12-25Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_12-25Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar4.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_25-45Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_25-45Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_25-45Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_25-45Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/white.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_25-45Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_25-45Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_25-45Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_25-45Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar5.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_55-90Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_55-90Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_55-90Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_55-90Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/white.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_55-90Hz_613_1_lat-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_55-90Hz_613_1_lat-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_55-90Hz_613_1_med-lh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_55-90Hz_613_1_med-rh.jpg',
         '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar6.jpg'
         )

files_con = ('/media/cbru/SMEDY/results/ISCs_comp_against_0/con_5.000000e-01-4Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_5.000000e-01-4Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_5.000000e-01-4Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_5.000000e-01-4Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_4-8Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_4-8Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_4-8Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_4-8Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_8-12Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_8-12Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_8-12Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_8-12Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_12-25Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_12-25Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_12-25Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_12-25Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_25-45Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_25-45Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_25-45Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_25-45Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_55-90Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_55-90Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_55-90Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/con_55-90Hz_613_1_med-rh.jpg',

             )

files_dys = ('/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_5.000000e-01-4Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_5.000000e-01-4Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_5.000000e-01-4Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_5.000000e-01-4Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_4-8Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_4-8Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_4-8Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_4-8Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_8-12Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_8-12Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_8-12Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_8-12Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_12-25Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_12-25Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_12-25Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_12-25Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_25-45Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_25-45Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_25-45Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_25-45Hz_613_1_med-rh.jpg',

             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_55-90Hz_613_1_lat-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_55-90Hz_613_1_lat-rh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_55-90Hz_613_1_med-lh.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/dys_55-90Hz_613_1_med-rh.jpg',
             )

files_leg = ('/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar1.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar2.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar3.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar4.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar5.jpg',
             '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar6.jpg'
             )

#plot subplots
plt.rcParams['font.family'] = "serif"
fig = plt.figure(figsize=(17, 13))
fig.tight_layout()
fig.subplots_adjust(wspace=0.02, hspace=0.12)
i = 0

positions = {3, 7, 11, 15, 19, 23}
legend = ('', '', '', '\u03B4 (0.5\u20134 Hz)',
          '', '', '', '\u03B8 (4\u20138 Hz)',
          '', '', '', '\u03B1 (8\u201312 Hz)',
          '', '', '', '\u03B2 (12\u201325 Hz)',
          '', '', '', 'low \u03B3 (25\u201345 Hz)',
          '', '', '', 'high \u03B3 (55\u201390 Hz)'
          )

# delta \u03B4
# theta \u03B8
# alpha \u03B1
# beta \u03B2
# gamma \u03B3
#for file in files:
#    img = plt.imread(file, format='jpg')
#    ax = fig.add_subplot(6,10,i)
#    ax.imshow(img, aspect = 'equal')
#    ax.axis('on')
#    if i in positions:
#        ax.text(0.6, 1.05, legend[i], horizontalalignment='center',
#                verticalalignment='center', transform=ax.transAxes, fontsize=17)
#    if i==3:
#        ax.text(0, 1.9, 'control group', horizontalalignment='center',
#                verticalalignment='center', transform=ax.transAxes, fontsize=22)
#    if i==8:
#        ax.text(0, 1.9, 'dyslexic group', horizontalalignment='center',
#                verticalalignment='center', transform=ax.transAxes, fontsize=22)
#    if i in {1,3,6,8}:
#        ax.text(0.5, 1.5, 'lh', horizontalalignment='center',
#                verticalalignment='center', transform=ax.transAxes, fontsize=15)
#    if i in {2,4,7,9}:
#        ax.text(0.5, 1.5, 'rh', horizontalalignment='center',
#                verticalalignment='center', transform=ax.transAxes, fontsize=15)
#    if i==5:
#        left, width = 0.07, 0.1
#        bottom, height = 0.1, .8
#        ax.axis([left, bottom, width, height], {'on','image'})
#    plt.set_cmap('hot')
#    i=i+1
i = 0
gs1 = plt.GridSpec(6, 4)
gs1.update(left=0, right=0.435)
for file in files_con:
    img = plt.imread(file, format='jpg')
    ax = fig.add_subplot(gs1[i])
    ax.imshow(img, aspect='equal')
    ax.axis('off')
    if i in positions:
        ax.text(1.3, 1.05, legend[i], horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=17)
    if i == 2:
        ax.text(0, 1.7, 'control group', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=22)
    if i in {0, 2}:
        ax.text(0.5, 1.3, 'lh', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=15)
    if i in {1, 3}:
        ax.text(0.5, 1.3, 'rh', horizontalalignment='center',
                verticalalignment='center', transform=ax.transAxes, fontsize=15)
    i = i+1

ii = 0
gs2 = plt.GridSpec(6, 4)
gs2.update(left=0.465, right=0.9)
for file in files_dys:
    img = plt.imread(file, format='jpg')
    ax2 = fig.add_subplot(gs2[ii])
    ax2.imshow(img, aspect='equal')
    ax2.axis('off')
    if ii == 2:
        ax2.text(0, 1.7, 'dyslexic group', horizontalalignment='center',
                 verticalalignment='center', transform=ax2.transAxes, fontsize=22)
    if ii in {0, 2}:
        ax2.text(0.5, 1.3, 'lh', horizontalalignment='center',
                 verticalalignment='center', transform=ax2.transAxes, fontsize=15)
    if ii in {1, 3}:
        ax2.text(0.5, 1.3, 'rh', horizontalalignment='center',
                 verticalalignment='center', transform=ax2.transAxes, fontsize=15)
    ii = ii+1

i = 0
gs3 = plt.GridSpec(6, 1)
gs3.update(left=0.9, right=1)
for file in files_leg:
    img = plt.imread(file, format='jpg')
    ax = fig.add_subplot(gs3[i])
    ax.imshow(img, aspect='equal')
    ax.axis('off')
    i = i+1

fig.suptitle("T-statistics of ISCs during speech", fontsize=25, x=0.5, y=1.02)
plt.show()
fig.savefig(filepath + 'test_summary_T_' + con + '_ISCs.pdf', dpi=600, bbox_inches='tight')
fig.savefig(filepath + 'test_summary_T_' + con + '_ISCs.png', dpi=600, bbox_inches='tight')
