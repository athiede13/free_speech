"""
Apply cluster correction for independent-samples T-test based on spatial proximity and cluster size.

Inspired by MNE tutorial.

Created on Fri Feb 22 13:21:40 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import numpy as np
from scipy import stats
#from scipy import sparse
from scipy.io import loadmat
import matplotlib.pyplot as plt
#import mne
#from mne import spatial_src_connectivity
import os

from permutation_cluster_test_AT import _permutation_cluster_test_AT

print(__doc__)

#%% file paths

conn = '/media/cbru/SMEDY/scripts_speech_rest/stats/mantel/connectivity.npy'
#SUBJECTS_DIR = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/'
results_dir = '/media/cbru/SMEDY/results/dys_con_contrast/2020_02_redo_subject_perm/'
read_dir = '/media/cbru/SMEDY/DATA/group_fake_iscs/'

#%% read connectivity

#src_fname = SUBJECTS_DIR + '/fsaverage/bem/fsaverage-ico-5-src.fif'
#src = mne.read_source_spaces(src_fname)
print('Read connectivity.')
connectivity = np.load(conn)

connectivity_sparse = connectivity[()]

#connectivity = connectivity_sparse.toarray()

#np.save(save_dir + 'connectivity', connectivity_sparse)

#%% cluster correction

#   for each permutation:
#   1. Compute the test statistic for each voxel individually.
#   2. Threshold the test statistic values.
#   3. Cluster voxels that exceed this threshold (with the same sign) based on adjacency.
#   4. Retain the size of the largest cluster (measured, e.g., by a simple voxel count,
#      or by the sum of voxel t-values within the cluster) to build the null distribution.

# define conditions
cons = '_1' # '_1' listening to speech
freqs = {'5.000000e-01-4Hz', '4-8Hz', '8-12Hz', '12-25Hz', '25-45Hz', '55-90Hz'}

if cons == '_1':
    window = '_613'
elif cons == '_2':
    window = '_579'
else:
    print('Check condition!')

for freq in freqs:
    if os.path.isfile(read_dir + 'fake_t_vals_' + freq + window + cons + '.mat'):
            print(cons + ' ' + freq)
            # read in fake and actual T-test results
            fake_values = loadmat(read_dir + 'fake_t_vals_' + freq + 
                                       window + cons + '.mat')['fake_t_vals']
            real_values = loadmat(read_dir + 'real_t_vals_' + freq + window + cons +
                                  '.mat')['real_t_vals']
        
            # get threshold
            threshold = loadmat(read_dir + 'tthreshold_uncorrected_' + freq +
                                window + cons + '.mat')['tthreshold_uncorrected']
            print(threshold)
            #thres_id = threshold.shape[0] - 1 # which frequency band id -1 to get correct index
        
            # reshape fake_values to (n_observations, n_times, n_vertices)
            fake_values = fake_values[:, :, np.newaxis]
            fake_values = fake_values.reshape((5000, 1, 20484))
        
            # reshape real_values
            real_values = real_values[:, :, np.newaxis]
            real_values = real_values.reshape((1, 1, 20484))
        
            # search for clusters (only once)
#            max_clu_lens, clusters = _permutation_cluster_test_AT(fake_values,
#                                                                  threshold=threshold[0][0],
#                                                                  n_permutations=5000,
#                                                                  tail=0,
#                                                                  connectivity=connectivity_sparse,
#                                                                  n_jobs=4, seed=10,
#                                                                  max_step=1, t_power=1,
#                                                                  out_type='indices',
#                                                                  exclude=None,
#                                                                  step_down_p=0,
#                                                                  check_disjoint=False,
#                                                                  buffer_size=1000)
#        
#            np.save(results_dir + 'max_clu_lens_' + freq + window + cons, max_clu_lens)
        
            max_clu_lens = np.load(results_dir + 'max_clu_lens_' + freq + window + cons + '.npy')
       
            # null distribution
            plt.figure(0)
            plt.hist(max_clu_lens)
            kde = stats.gaussian_kde(max_clu_lens)
            x = np.linspace(max_clu_lens.min(), max_clu_lens.max(), 100)
            p = kde(x)
            # cutoff for a cluster size that is significant
            plt.figure(1)
            plt.plot(x, p)
            plt.hlines(0.095, 0, 14) # visualization of cutoff
            # take maximum across all freq bands
            cutoff = np.max(max_clu_lens)
            print(['cutoff length is ', cutoff])
            
            max_clu_lens2, clusters = _permutation_cluster_test_AT(real_values,
                                                                   threshold=threshold[0][0],
                                                                   n_permutations=1,
                                                                   tail=0,
                                                                   connectivity=connectivity_sparse,
                                                                   n_jobs=4, seed=10,
                                                                   max_step=1,
                                                                   t_power=1,
                                                                   out_type='indices',
                                                                   exclude=None,
                                                                   step_down_p=0,
                                                                   check_disjoint=False,
                                                                   buffer_size=1000)
        
            # length of all initial clusters
            clu_lens = np.zeros(len(clusters))
            for j in range(0, len(clusters)):
                clu_lens[j] = len(clusters[j][0])
        
            # hists
            plt.figure(1)
            plt.hist(max_clu_lens)
            plt.hist(clu_lens)
        
            # out in format required by MNE cluster function (for visualization)
            t_out = real_values.reshape(1, 20484)
            clusters_new = clusters
            for c, l, i in zip(clusters, clu_lens, range(0, len(clusters))):
                clusters_new[i] = np.zeros(np.int(l), dtype='int'), c[0]
        
            clu = t_out, clusters_new
            np.save(results_dir + 'clu_' + freq + window + cons, clu)
        
            # see how many clusters exceed the threshold (i.e. survive the correction)
            ids = np.where(clu_lens > cutoff)[0]
            clu_sig = clusters[0:len(ids)]
            for i in range(0, len(ids)):
                clu_sig[i] = clusters[ids[i]]
        
            sig_clu_lens = np.zeros(len(clu_sig))
            for j in range(0, len(clu_sig)):
                sig_clu_lens[j] = len(clu_sig[j][0])
    else: print('No uncorrected p-vals < 0.05 for ' + freq)
