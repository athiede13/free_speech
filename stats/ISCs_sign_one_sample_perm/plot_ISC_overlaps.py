"""
Plot overlaps of permutation t-test on source data.

"""
# Author: Anja Thiede <anja.thiede@helsinki.fi>

import numpy as np
import scipy.io as sio
from summarize_clusters_stc_AT import summarize_clusters_stc_AT

#%matplotlib qt

# paths etc.
subjects_dir = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/'
results_path = '/media/cbru/SMEDY/results/ISCs_comp_against_0/'
fres = {'5.000000e-01-4Hz', '4-8Hz', '8-12Hz', '12-25Hz', '25-45Hz', '55-90Hz'}
condition = '_1' # 1 speech
win = '_613'
p_cluster_threshold = 0.05
colormap = 'Dark2_r'
#colormap = 'gnuplot2_r'

for fre in fres:
    stc_both_groups = []
    print(fre)
    for group_data in {"con_", "dys_"}:
        print('Load clusters')
        print(group_data)
        # load clu
        T_obs, clusters, cluster_p_values, H0 = clu = \
            np.load(results_path + 't_clu_' + group_data + fre + win +
                    condition + '.npy')
        #    Now select the clusters that are sig. at p < 0.05 (note that this value
        #    is multiple-comparisons corrected).
        good_cluster_inds = np.where(cluster_p_values < p_cluster_threshold)[0]
    
        #    Now let's build a convenient representation of each cluster, where each
        #    cluster becomes a "time point" in the SourceEstimate
        if not good_cluster_inds.any():
            print('No significant clusters for ' + fre + ' and ' + group_data + ' available.')
        else:
            tstep = 1
            fsave_vertices = [np.arange(10242), np.arange(10242)]
            stc_all_cluster_vis = summarize_clusters_stc_AT(clu, vertices=fsave_vertices,
                                                            subject='fsaverage')
            clim = sio.loadmat(results_path + 'legend/clim_' + fre, mdict={'clim': clim})
            t_threshold = clim['clim']['lims'][0][0][0][0]
            stc_all_cluster_vis.data[np.where(stc_all_cluster_vis.data<t_threshold)]=0
            stc_all_cluster_vis.data[np.where(stc_all_cluster_vis.data>t_threshold)]=1
            stc_both_groups.append(stc_all_cluster_vis.data[:,0])
    stc_both_groups[1] = stc_both_groups[1]*2
    stc_both_groups.append(stc_both_groups[0] + stc_both_groups[1])
    stc_all_cluster_vis.data[:,0] = stc_both_groups[2]
    stc_all_cluster_vis.data[0,0] = -1
    # clims
    clim = dict(kind='value',
                        pos_lims=[0, 2, 3])

    # Visualize the clusters
    # ----------------------
    print('Visualizing clusters.')
    for hemi in {'lh', 'rh'}:
        for views in {'lat', 'med'}:
            brain = stc_all_cluster_vis.plot(
                hemi=hemi, subjects_dir=subjects_dir,
                size=(800, 800), smoothing_steps=2, clim=clim,
                title=group_data + fre + condition + hemi,
                alpha=0.9, transparent=False, time_viewer=False,
                time_label=None, background='white', colorbar=False,
                views=views, colormap=colormap)
            brain.data['surfaces'][0].actor.property.backface_culling =\
                True # fix for look-through visualization of the brain
#            brain.data['colorbar'].number_of_labels = 3
            brain.save_single_image(results_path + 'overlap_' + fre + '_' + views +
                                    '-' + hemi + '.jpg')
            brain.close()

#%% legend

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
colormap = mpl.cm.Dark2.colors             
# Create bars
barWidth = 0.9
bars1 = [3, 3, 1]
bars2 = [4, 2, 3]
bars3 = [4, 6, 7, 10, 4, 4]
bars4 = bars1 + bars2 + bars3
 
# The X position of bars
r1 = [1,5,9]
r2 = [2,6,10]
r3 = [3,4,7,8,11,12]
r4 = r1 + r2 + r3
 
# Create barplot
plt.bar(r1, bars1, width = barWidth,
        color = (0.4, 0.6509803921568628, 0.11764705882352941), label='controls')
plt.bar(r2, bars2, width = barWidth, 
        color = (0.9019607843137255, 0.6705882352941176, 0.00784313725490196), label='dyslexics')
plt.bar(r3, bars3, width = barWidth, 
        color = (0.10588235294117647, 0.6196078431372549, 0.4666666666666667), label='overlap')
# Note: the barplot could be created easily. See the barplot section for other examples.
 
# Create legend
plt.legend(fontsize='xx-large', ncol=3)
plt.savefig(results_path + 'overlap_legend.pdf')

