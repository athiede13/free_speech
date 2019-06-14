"""
Visualize cluster results.

Created on Wed Feb 27 15:09:19 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""
from os.path import basename
import sys
sys.path.append('../')
import numpy as np
from mantel.summarize_clusters_stc_AT import summarize_clusters_stc_AT

#%matplotlib qt

subjects_dir = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/'

# to fill, needed if this script is not used directly after cluster_correction.py
results_dir = '/media/cbru/SMEDY/results/dys_con_contrast/2019_05_t_test+cluster_correction/'
p_thresh = 0.05

# load sign clu
# ISC contrast speech
delta = (results_dir + 't_clu_tail1_5.000000e-01-4Hz_613_1.npy',
         results_dir + 't_clu_tail-1_5.000000e-01-4Hz_613_1.npy')
theta = (results_dir + 't_clu_tail1_4-8Hz_613_1.npy',
         results_dir + 't_clu_tail-1_4-8Hz_613_1.npy')
alpha = (results_dir + 't_clu_tail1_8-12Hz_613_1.npy',
         results_dir + 't_clu_tail-1_8-12Hz_613_1.npy')
beta = (results_dir + 't_clu_tail1_12-25Hz_613_1.npy',
        results_dir + 't_clu_tail-1_12-25Hz_613_1.npy')
gamma1 = (results_dir + 't_clu_tail1_25-45Hz_613_1.npy',
          results_dir + 't_clu_tail-1_25-45Hz_613_1.npy')
gamma2 = (results_dir + 't_clu_tail1_55-90Hz_613_1.npy',
          results_dir + 't_clu_tail-1_55-90Hz_613_1.npy')
all_bands = {delta, theta, alpha, beta, gamma1, gamma2}

t_threshold = -1.9651120203087005 # computed in ttest_cluster_permutation.py

for band in all_bands:
    stc_all_cluster_vis_pos = None
    stc_all_cluster_vis_neg = None
    stc_all_cluster_vis_both = None
    clu = np.load(band[0])
    T_obs, clusters, cluster_p_values, H0 = clu
    good_cluster_inds = np.where(cluster_p_values < p_thresh)[0]
    if not good_cluster_inds.any():
        print('No significant clusters available for file ' + band[0] + '\n')
    else:
        stc_all_cluster_vis_pos = summarize_clusters_stc_AT(clu, p_thresh=0.05,
                                                            tstep=1e-3, tmin=0,
                                                            subject='fsaverage',
                                                            vertices=None)
    clu = np.load(band[1])
    T_obs, clusters, cluster_p_values, H0 = clu
    good_cluster_inds = np.where(cluster_p_values < p_thresh)[0]
    if not good_cluster_inds.any():
        print('No significant clusters available for file ' + band[1] + '\n')
        print('The smallest corrected p-value is '+str(min(cluster_p_values)))
    else:
        stc_all_cluster_vis_neg = summarize_clusters_stc_AT(clu, p_thresh=0.05,
                                                            tstep=1e-3, tmin=0,
                                                            subject='fsaverage',
                                                            vertices=None)
    # combine positive and negative clusters to one source estimate file
    if stc_all_cluster_vis_pos is not None and stc_all_cluster_vis_neg is not None:
        print('both contrasts')
        stc_all_cluster_vis_both = stc_all_cluster_vis_pos.copy()
        stc_all_cluster_vis_both.data[:, 0] = (stc_all_cluster_vis_pos.data[:, 0] +
                                               stc_all_cluster_vis_neg.data[:, 0])
    elif stc_all_cluster_vis_pos is None and stc_all_cluster_vis_neg is not None:
        print('only negative contrast')
        stc_all_cluster_vis_both = stc_all_cluster_vis_neg.copy()
        stc_all_cluster_vis_both.data[:, 0] = stc_all_cluster_vis_neg.data[:, 0]
    elif stc_all_cluster_vis_neg is None and stc_all_cluster_vis_pos is not None:
        print('only positive contrast')
        stc_all_cluster_vis_both = stc_all_cluster_vis_pos.copy()
        stc_all_cluster_vis_both.data[:, 0] = stc_all_cluster_vis_pos.data[:, 0]
    else:
        print('Error! There is no data for negative and positive contrasts.')

    # thresholding
    stc_all_cluster_vis_both.data[(stc_all_cluster_vis_both.data[:, 0] <
                                   -t_threshold) & (stc_all_cluster_vis_both.data[:, 0] >
                                                    t_threshold), 0] = 0

    print('Visualizing clusters.')

    for hemi in {'lh', 'rh'}:
        clim = dict(kind='value', pos_lims=[-6, 0, 6]) # T values
        brain = stc_all_cluster_vis_both.plot(subjects_dir=subjects_dir,
                                              views='lat', clim=clim,
                                              colormap='mne', hemi=hemi,
                                              alpha=0.8, time_label=None,
                                              transparent=True,
                                              background='white',
                                              title=basename(band[0])[:-4]+
                                              '-'+hemi, colorbar=True)
        # fix for look-through visualization of the brain
        brain.data['surfaces'][0].actor.property.backface_culling = True
        brain.show_view('lateral')
        brain.data['colorbar'].number_of_labels = 3
        brain.save_single_image(results_dir + 'clu_' + basename(band[0])[12:-4] +
                                '_lat-' + hemi + '.png')
        brain.show_view('medial')
        brain.save_single_image(results_dir + 'clu_' + basename(band[0])[12:-4] +
                                '_med-' + hemi + '.png')
        brain.close()
    print(stc_all_cluster_vis_both.data.min(), stc_all_cluster_vis_both.data.max())
    del stc_all_cluster_vis_pos, stc_all_cluster_vis_neg, stc_all_cluster_vis_both
