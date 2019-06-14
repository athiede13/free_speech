"""
2 samples permutation test on source data with spatio-temporal clustering.

Tests if the source space data are significantly different between
2 groups of subjects. The multiple comparisons problem is addressed
with a cluster-level permutation test across space and time.

Adapted from MNE software package.
"""

# Authors: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#          Eric Larson <larson.eric.d@gmail.com>
#          modified by Anja Thiede <anja.thiede@helsinki.fi>
# License: BSD (3-clause)

import datetime
import numpy as np
from scipy import stats
import scipy.io as sio
import mne
from mne import spatial_src_connectivity
from mne.stats.cluster_level import spatio_temporal_cluster_test
from ttest_ind_no_p import ttest_ind_no_p

#%matplotlib qt

print(__doc__)

# Set parameters
# --------------

now = datetime.datetime.now()
SUBJECTS_DIR = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/'
results_path = '/media/cbru/SMEDY/results/dys_con_contrast/2019_05_t_test+cluster_correction/'
data_path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/'
src_fname = SUBJECTS_DIR + '/fsaverage/bem/fsaverage-ico-5-src.fif'
src = mne.read_source_spaces(src_fname)

fres = {'5.000000e-01-4Hz', '4-8Hz', '8-12Hz', '12-25Hz', '25-45Hz', '55-90Hz'}
conditions = {'_1'} # 1 speech
win = '_613'
tails = [1, -1]

log_path = (data_path+'logs/plot_stats_cluster_spatio_temporal_2samp_'+
            now.strftime("%Y-%m-%d") + win + '.log')
log = open(log_path, 'w')

idCon = sio.loadmat(data_path + 'corr_matrices/idCon.mat')
idDys = sio.loadmat(data_path + 'corr_matrices/idDys.mat')
idCon = idCon['idCon']
idDys = idDys['idDys']
n_CON_pairs, n_DYS_pairs = len(idCon), len(idDys)

print('Computing connectivity.')
connectivity = spatial_src_connectivity(src)

for fre in fres:
    for condition in conditions:
        for tail in tails:
            # read in correlation matrices
            X = sio.loadmat(data_path + 'corr_matrices/corr_matrix_' + fre +
                            win + condition + '.mat')
            X = X['all_data']
            X1 = X[:, idDys-1] # ISCs dyslexics
            X2 = X[:, idCon-1] # ISCs controls
            # Compute statistic
            #    Note that X needs to be a list of multi-dimensional array of shape
            #    samples (subjects_k) x time x space, so we permute dimensions
            X1 = np.transpose(X1, [1, 2, 0])
            X2 = np.transpose(X2, [1, 2, 0])
            X = [X1, X2]
            n_subject_pairs = X1.shape[0] + X2.shape[0]
            p_initial_threshold = 0.05
            if tail == -1:
                t_threshold = stats.distributions.t.ppf(p_initial_threshold /
                                                        2., n_subject_pairs - 1)
            else:
                t_threshold = -stats.distributions.t.ppf(p_initial_threshold /
                                                         2., n_subject_pairs - 1)

            print('Clustering.')
            print(t_threshold)
            stat_fun = ttest_ind_no_p # modified scipy function to not return pval
            T_obs, clusters, cluster_p_values, H0 = clu =\
                spatio_temporal_cluster_test(X, connectivity=connectivity,
                                             n_jobs=4, threshold=t_threshold,
                                             n_permutations=5000, t_power=0,
                                             out_type='indices',
                                             stat_fun=stat_fun, tail=tail,
                                             seed=None, max_step=1,
                                             check_disjoint=False,
                                             buffer_size=None)

            # save clu
            np.save(results_path + 't_clu_tail' + str(tail) + '_' + fre + win + condition, clu)

            # see whether there are significant clusters
            p_thresh = 0.05
            good_cluster_inds = np.where(cluster_p_values < p_thresh)[0]

log.close()
