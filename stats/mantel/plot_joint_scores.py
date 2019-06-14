"""
Plot subplots.

Created on 20.5.2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import matplotlib.pyplot as plt

#%matplotlib qt
#%matplotlib inline

#to fill
filepath = '/media/cbru/SMEDY/results/nepsy_models/'
files = ('/media/cbru/SMEDY/results/nepsy_models/FIQ.png',
         '/media/cbru/SMEDY/results/nepsy_models/tech_read.png',
         '/media/cbru/SMEDY/results/nepsy_models/phon_proc.png',
         '/media/cbru/SMEDY/results/nepsy_models/work_mem.png'
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
fig = plt.figure(figsize=(10, 8))
fig.tight_layout()
fig.subplots_adjust(wspace=0, hspace=0)
i = 1

for file in files:
    img = plt.imread(file, format='png')
    ax = fig.add_subplot(2, 2, i)
    ax.imshow(img, aspect='equal')
    ax.axis('off')
    i = i+1

plt.show()
fig.savefig(filepath + 'joint_scores.pdf', dpi=600, bbox_inches='tight')
fig.savefig(filepath + 'joint_scores.png', dpi=600, bbox_inches='tight')
