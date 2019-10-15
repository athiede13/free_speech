"""
Permutation t-test on source data with spatio-temporal clustering.

The multiple comparisons problem is addressed with a cluster-level
permutation test across space and time.

Adapted from MNE software package.
"""
# Authors: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#          Eric Larson <larson.eric.d@gmail.com>
#          modified by Anja Thiede <anja.thiede@helsinki.fi>
# License: BSD (3-clause)

import datetime
import numpy as np
from scipy import stats as stats
import scipy.io as sio
import mne
from mne import spatial_src_connectivity
from mne.stats import (spatio_temporal_cluster_1samp_test, ttest_1samp_no_p)
from summarize_clusters_stc_AT import summarize_clusters_stc_AT

print(__doc__)

#%matplotlib qt

# Set parameters
# --------------
now = datetime.datetime.now()
subjects_dir = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/'
data_path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/'
stc_path = ('/media/cbru/SMEDY/results/dys_con_contrast/2019_01_group_ISCs_FDR_correction/')
results_path = '/media/cbru/SMEDY/results/ISCs_comp_against_0/'
src_fname = subjects_dir + '/fsaverage/bem/fsaverage-ico-5-src.fif'
src = mne.read_source_spaces(src_fname)
# To use an algorithm optimized for spatio-temporal clustering, we
# just pass the spatial connectivity matrix (instead of spatio-temporal)
print('Computing connectivity.')
connectivity = spatial_src_connectivity(src)

fres = {'5.000000e-01-4Hz', '4-8Hz', '8-12Hz', '12-25Hz', '25-45Hz', '55-90Hz'}
condition = '_1' # 1 speech
win = '_613'
n_permutations = 5000
p_initial_threshold = 0.05
p_cluster_threshold = 0.05/6 # Bonf-corrected for 6 fre bands
rerun_perm = 0 # 0 do not rerun permutations, 1 rerun permutations (time-intensive)

log_path = (data_path+'logs/plot_stats_cluster_spatio_temporal_1samp_'+
            now.strftime("%Y-%m-%d") + win + '.log')
log = open(log_path, 'w')
stc = mne.read_source_estimate(data_path +
                               'average_all/average_ene_12-25Hz_286_10-lh.stc') # example stc
clim = dict(kind='value', lims=(0, 1, 1000))
idCon = sio.loadmat(data_path + 'corr_matrices/2018_09/idCon.mat')
idDys = sio.loadmat(data_path + 'corr_matrices/2018_09/idDys.mat')
idCon = idCon['idCon']
idDys = idDys['idDys']
n_CON_pairs, n_DYS_pairs = len(idCon), len(idDys)

# legends
clim_low = 10
clim_mid = 50
clim_high = 90

#%% Setup for reading the raw data

for fre in fres:
    print(fre)
    # read in correlation matrices
    X = sio.loadmat(data_path + 'corr_matrices/corr_matrix_' + fre + win + condition + '.mat')
    X = X['all_data']

    X_dys = X[:, idDys-1] # ISCs dyslexics
    X_con = X[:, idCon-1] # ISCs controls

    #    Note that X needs to be a list of multi-dimensional array of shape
    #    samples (subjects_k) x time x space, so we permute dimensions
    X_dys = np.transpose(X_dys, [1, 2, 0])
    X_con = np.transpose(X_con, [1, 2, 0])
    X_all = np.concatenate((X_con, X_dys), axis=0)

    # find clims
    # clustering
    n_subject_pairs = X_all.shape[0]
    t_threshold = -stats.distributions.t.ppf(p_initial_threshold / 2., n_subject_pairs - 1)
    print('Clustering.')

    stat_fun = ttest_1samp_no_p
    T_obs, clusters, cluster_p_values, H0 = clu = \
        spatio_temporal_cluster_1samp_test(X_all, connectivity=connectivity,
                                           n_jobs=4, n_permutations=100,
                                           threshold=t_threshold, t_power=1,
                                           buffer_size=None, out_type='indices',
                                           verbose=True, stat_fun=stat_fun)

    #    Now let's build a convenient representation of each cluster, where each
    #    cluster becomes a "time point" in the SourceEstimate
    tstep = stc.tstep
    fsave_vertices = [np.arange(10242), np.arange(10242)]
    stc_all_cluster_vis = summarize_clusters_stc_AT(clu, vertices=fsave_vertices,
                                                    subject='fsaverage')
    clim = dict(kind='value',
                lims=[np.percentile(stc_all_cluster_vis.data[:, 0], clim_low),
                      np.percentile(stc_all_cluster_vis.data[:, 0], clim_mid),
                      np.percentile(stc_all_cluster_vis.data[:, 0], clim_high)])
    print(clim)
    sio.savemat(results_path + 'legend/clim_' + fre, mdict={'clim': clim})

    thisdict =	{"con_": X_con,
                "dys_": X_dys}
    for group_data in thisdict:
        print(group_data)
        if rerun_perm == 1:
            # clustering
            n_subject_pairs = thisdict[group_data].shape[0]
            print(n_subject_pairs)
            t_threshold = -stats.distributions.t.ppf(p_initial_threshold / 2., n_subject_pairs - 1)
            print('Clustering.')
    
            stat_fun = ttest_1samp_no_p
            T_obs, clusters, cluster_p_values, H0 = clu = \
                spatio_temporal_cluster_1samp_test(thisdict[group_data], connectivity=connectivity,
                                                   n_jobs=4, n_permutations=n_permutations,
                                                   threshold=t_threshold, t_power=1,
                                                   buffer_size=None, out_type='indices',
                                                   verbose=True, stat_fun=stat_fun)
    
            # save clu
            np.save(results_path + 't_clu_' + group_data + fre + win + condition,
                    clu)
        else:
            print('Load clusters')
            print(group_data)
            T_obs, clusters, cluster_p_values, H0 = clu = \
                np.load(results_path + 't_clu_' + group_data + fre + win +
                        condition + '.npy')
        #    Now select the clusters that are sig. at p < 0.05 (note that this value
        #    is multiple-comparisons corrected).
        good_cluster_inds = np.where(cluster_p_values < p_cluster_threshold)[0] 
        out = []
        for j in range(0, len(good_cluster_inds)):
            inds_t, inds_v = [(clusters[cluster_ind]) for ii, cluster_ind in
                              enumerate(good_cluster_inds)][j]
            out.append(len(inds_v)) # max cluster is xxth
    
        id_max = out.index(max(out))
        inds_t, inds_v = [(clusters[cluster_ind]) for ii, cluster_ind in
                          enumerate(good_cluster_inds)][id_max]
        print(len(inds_v))
        print(cluster_p_values[cluster_p_values < p_cluster_threshold][id_max])
    
        # Visualize the clusters
        # ----------------------
        print('Visualizing clusters.')

        #    Now let's build a convenient representation of each cluster, where each
        #    cluster becomes a "time point" in the SourceEstimate
        if not good_cluster_inds.any():
            print('No significant clusters for ' + fre + ' and ' + group_data + ' available.')
        else:
            tstep = stc.tstep
            fsave_vertices = [np.arange(10242), np.arange(10242)]
            stc_all_cluster_vis = summarize_clusters_stc_AT(clu, vertices=fsave_vertices,
                                                            subject='fsaverage')
            if clim['lims'][2] > 0:
                colormap = 'hot'
            else:
                colormap = 'Blues'
# Plot the T-values in the SourceEstimate, which shows all the clusters,
# weighted by their T-values
            for hemi in {'lh', 'rh'}:
                for views in {'lat'}:#, 'med'}:
                    brain = stc_all_cluster_vis.plot(
                        hemi=hemi, subjects_dir=subjects_dir,
                        size=(800, 800), smoothing_steps=5, clim=clim,
                        title=group_data + fre + condition + hemi,
                        alpha=1, transparent=True, time_viewer=False,
                        time_label=None, background='white', colorbar=True,
                        views=views, colormap=colormap)
                    brain.data['surfaces'][0].actor.property.backface_culling =\
                        True # fix for look-through visualization of the brain
                    brain.save_single_image(results_path + group_data + fre +
                                            win + condition + '_' + views +
                                            '-' + hemi + '.jpg')
                    brain.close()
