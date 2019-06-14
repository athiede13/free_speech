"""
Extract MNI coordinates for all brain maps.

Created on Fri May 24 11:26:07 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import mne
import numpy as np
from summarize_clusters_stc_AT import summarize_clusters_stc_AT

#%% for one-sample T-test whether ISCs are significant
results_path = '/media/cbru/SMEDY/results/ISCs_comp_against_0/'
fres = {'5.000000e-01-4Hz', '4-8Hz', '8-12Hz', '12-25Hz', '25-45Hz', '55-90Hz'}
condition = '_1' # 1 speech, 2 rest
win = '_613' #'_579' #
groups = {'con_', 'dys_'}

for fre in fres:
    for group in groups:
        T_obs, clusters, cluster_p_values, H0 = clu =\
            np.load(results_path + 't_clu_' + group + fre + win + condition + '.npy')
        fsave_vertices = [np.arange(10242), np.arange(10242)]
        stc_all_cluster_vis = summarize_clusters_stc_AT(clu,
                                                        vertices=fsave_vertices,
                                                        subject='fsaverage')
        # find the max T value and vertex
        max_T = stc_all_cluster_vis.data[:, 0].max()
        max_vtx = np.where(stc_all_cluster_vis.data[:, 0] ==
                           stc_all_cluster_vis.data[:, 0].max())
        p_cluster_threshold = 0.05
        good_cluster_inds = np.where(cluster_p_values <
                                     p_cluster_threshold)[0]
        for ii in good_cluster_inds:
            if np.isin(max_vtx, clusters[ii][1]):
                clu_size = len(clusters[ii][1])

        if max_vtx[0][0] > 10242:
            hemi = 1 # rh
            vtx = max_vtx[0][0] - 10242
        else:
            hemi = 0 # lh
            vtx = max_vtx[0][0]
        # transform to mni coordinates
        mni = mne.vertex_to_mni(vtx, hemi, 'fsaverage')[0]
        print(group, fre, clu_size, mni.astype(np.int64), round(max_T, 2))

#%% for ISC group differences
results_dir = '/media/cbru/SMEDY/results/dys_con_contrast/2019_05_t_test+cluster_correction/'
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
p_thresh = 0.05
p_cluster_threshold = 0.05

for band in all_bands:
    stc_all_cluster_vis_pos = None
    stc_all_cluster_vis_neg = None
    stc_all_cluster_vis_both = None
    clu = np.load(band[0])
    T_obs_pos, clusters_pos, cluster_p_values_pos, H0_pos = clu
    good_cluster_inds = np.where(cluster_p_values_pos < p_thresh)[0]
    if not good_cluster_inds.any():
        print('')
    else:
        stc_all_cluster_vis_pos = summarize_clusters_stc_AT(clu, p_thresh=0.05,
                                                            tstep=1e-3, tmin=0,
                                                            subject='fsaverage',
                                                            vertices=None)
    clu = np.load(band[1])
    T_obs_neg, clusters_neg, cluster_p_values_neg, H0_neg = clu
    good_cluster_inds = np.where(cluster_p_values_neg < p_thresh)[0]
    if not good_cluster_inds.any():
        print('')
    else:
        stc_all_cluster_vis_neg = summarize_clusters_stc_AT(clu, p_thresh=0.05,
                                                            tstep=1e-3, tmin=0,
                                                            subject='fsaverage',
                                                            vertices=None)
    # combine positive and negative clusters to one source estimate file
    if stc_all_cluster_vis_pos is not None and stc_all_cluster_vis_neg is not None:
        stc_all_cluster_vis_both = stc_all_cluster_vis_pos.copy()
        stc_all_cluster_vis_both.data[:, 0] =\
            stc_all_cluster_vis_pos.data[:, 0] + stc_all_cluster_vis_neg.data[:, 0]
    elif stc_all_cluster_vis_pos is None and stc_all_cluster_vis_neg is not None:
        stc_all_cluster_vis_both = stc_all_cluster_vis_neg.copy()
        stc_all_cluster_vis_both.data[:, 0] = stc_all_cluster_vis_neg.data[:, 0]
    elif stc_all_cluster_vis_neg is None and stc_all_cluster_vis_pos is not None:
        stc_all_cluster_vis_both = stc_all_cluster_vis_pos.copy()
        stc_all_cluster_vis_both.data[:, 0] = stc_all_cluster_vis_pos.data[:, 0]
    else:
        print('Error! There is no data for negative and positive contrasts.')
    # find the max T value and vertex, extreme might be negative or positive
    max_T = stc_all_cluster_vis_both.data[:, 0].max()
    min_T = stc_all_cluster_vis_both.data[:, 0].min()
    if abs(max_T) > abs(min_T): # take only positive clusters
        T = max_T
        max_vtx = np.where(stc_all_cluster_vis_both.data[:, 0] ==
                           stc_all_cluster_vis_both.data[:, 0].max())
        good_cluster_inds = np.where(cluster_p_values_pos < p_cluster_threshold)[0]
        for ii in good_cluster_inds:
            if np.isin(max_vtx, clusters_pos[ii][1]):
                clu_size = len(clusters_pos[ii][1])
    else: # take only negative clusters
        T = min_T
        max_vtx = np.where(stc_all_cluster_vis_both.data[:, 0] ==
                           stc_all_cluster_vis_both.data[:, 0].min())
        good_cluster_inds = np.where(cluster_p_values_neg < p_cluster_threshold)[0]
        for ii in good_cluster_inds:
            if np.isin(max_vtx, clusters_neg[ii][1]):
                clu_size = len(clusters_neg[ii][1])
    if max_vtx[0][0] > 10242:
        hemi = 1 # rh
        vtx = max_vtx[0][0] - 10242
    else:
        hemi = 0 # lh
        vtx = max_vtx[0][0]
    # transform to mni coordinates
    mni = mne.vertex_to_mni(vtx, hemi, 'fsaverage')[0]
    print(band, clu_size, mni.astype(np.int64), round(T, 2))

#%% for Mantel regressions
results_path = '/media/cbru/SMEDY/results/mantel_correlations/2019_05_simple_model/'
clu_files = [
    results_path + 'phon_clu_5.000000e-01-4Hz_613_1.npy',
    results_path + 'phon_clu_4-8Hz_613_1.npy',
    results_path + 'phon_clu_8-12Hz_613_1.npy',
    results_path + 'phon_clu_12-25Hz_613_1.npy',
    results_path + 'phon_clu_25-45Hz_613_1.npy',
    results_path + 'phon_clu_55-90Hz_613_1.npy',
    results_path + 'read_clu_5.000000e-01-4Hz_613_1.npy',
    results_path + 'read_clu_4-8Hz_613_1.npy',
    results_path + 'read_clu_8-12Hz_613_1.npy',
    results_path + 'read_clu_12-25Hz_613_1.npy',
    results_path + 'read_clu_25-45Hz_613_1.npy',
    results_path + 'mem_clu_5.000000e-01-4Hz_613_1.npy',
    results_path + 'iq_clu_5.000000e-01-4Hz_613_1.npy',
    results_path + 'iq_clu_55-90Hz_613_1.npy'
    ]

cutoffs = [13, 11, 12, 10, 8, 9, 12, 9, 10, 10, 12, 12, 9, 10]
p_cluster_threshold = 0.05

for file, cutoff in zip(clu_files, cutoffs):
    # load clu
    clu = np.load(file)
    r_obs, clusters, cluster_p_values, H0 = clu
    fsave_vertices = [np.arange(10242), np.arange(10242)]
    stc_all_cluster_vis = summarize_clusters_stc_AT(clu, vertices=fsave_vertices,
                                                    subject='fsaverage')
    good_cluster_inds = np.where(cluster_p_values < p_cluster_threshold)[0]
    # thresholding by cluster length
    good_cluster_inds2 = []
    clusters2 = []
    for ii in range(0, len(good_cluster_inds)):
        if len(clusters[good_cluster_inds[ii]][1]) > (cutoff-1):
            good_cluster_inds2.append(good_cluster_inds[ii])
            clusters2.append(clusters[good_cluster_inds[ii]])
            clu2 = r_obs, clusters2, cluster_p_values[good_cluster_inds2]
    if not clusters2:
        print('All clusters are smaller than the minimal length.')
    else:
        stc_all_cluster_vis = summarize_clusters_stc_AT(clu2, p_thresh=0.05,
                                                        tstep=1e-3, tmin=0,
                                                        subject='fsaverage',
                                                        vertices=fsave_vertices)
    max_R = stc_all_cluster_vis.data[:, 0].max()
    max_vtx = np.where(stc_all_cluster_vis.data[:, 0] ==
                       stc_all_cluster_vis.data[:, 0].max())
    for ii in good_cluster_inds2:
        if np.isin(max_vtx, clusters[ii][1]):
            clu_size = len(clusters[ii][1])

    if max_vtx[0][0] > 10242:
        hemi = 1 # rh
        vtx = max_vtx[0][0] - 10242
    else:
        hemi = 0 # lh
        vtx = max_vtx[0][0]
    # transform to mni coordinates
    mni = mne.vertex_to_mni(vtx, hemi, 'fsaverage')[0]
    print(file, clu_size, mni.astype(np.int64), round(max_R, 2))
