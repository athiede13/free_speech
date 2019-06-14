"""
Apply cluster correction for mantel test based on spatial proximity and cluster size.

Inspired by MNE tutorial.

Created on Fri Feb 22 13:21:40 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import numpy as np
from scipy import stats
from scipy.io import loadmat
import matplotlib.pyplot as plt
import mne
from mne import spatial_src_connectivity

from permutation_cluster_test_AT import _permutation_cluster_test_AT

print(__doc__)

#%% file paths

save_dir = '/media/cbru/SMEDY/scripts_speech_rest/stats/mantel/'
SUBJECTS_DIR = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/'
results_dir = '/media/cbru/SMEDY/results/mantel_correlations/2019_05_simple_model/'
read_dir = '/media/cbru/SMEDY/DATA/correlations_mantel/2019_05_simple_model/'

#%% compute connectivity

src_fname = SUBJECTS_DIR + '/fsaverage/bem/fsaverage-ico-5-src.fif'
src = mne.read_source_spaces(src_fname)
print('Computing connectivity.')
connectivity_sparse = spatial_src_connectivity(src)
connectivity = connectivity_sparse.toarray()

np.save(save_dir + 'connectivity', connectivity_sparse)

#%% cluster correction

#   for each permutation:
#   1. Compute the test statistic for each voxel individually.
#   2. Threshold the test statistic values.
#   3. Cluster voxels that exceed this threshold (with the same sign) based on adjacency.
#   4. Retain the size of the largest cluster (measured, e.g., by a simple voxel count,
#      or by the sum of voxel t-values within the cluster) to build the null distribution.

# define conditions
mode = 'iq' # 'iq' or 'read' or 'mem' or 'phon'
cons = '_1' # '_1' listening to speech
freqs = {'5.000000e-01-4Hz', '4-8Hz', '8-12Hz', '12-25Hz', '25-45Hz', '55-90Hz'}

if cons == '_1':
    window = '_613'
elif cons == '_2':
    window = '_579'
else:
    print('Check condition!')

for freq in freqs:
    print(mode + ' ' + cons + ' ' + freq)
    # read in surrogate and actual mantel test results
    surrogate_values = loadmat(read_dir + mode + '_surrogate_values_' +
                               freq + window + cons + '.mat')['surrogate_values']
    r_mantel = loadmat(read_dir + mode + '_r_mantel_' + freq + window + cons +
                       '.mat')['r_mantel']

    # get threshold
    threshold = loadmat(read_dir + mode + '_rthreshold_uncorrected_' + freq +
                        window + cons + '.mat')['rthreshold_uncorrected']
    thres_id = threshold.shape[0] - 1 # which frequency band id -1 to get correct index

    # reshape surrogate_values to (n_observations, n_times, n_vertices)
    surrogate_values = surrogate_values[:, :, np.newaxis]
    surrogate_values = surrogate_values.reshape((5000, 1, 20484))

    # reshape r_mantel
    r_mantel = r_mantel[:, :, np.newaxis]
    r_mantel = r_mantel.reshape((1, 1, 20484))

    # search for clusters
    max_clu_lens, clusters = _permutation_cluster_test_AT(surrogate_values,
                                                          threshold=threshold[thres_id][0][0][0],
                                                          n_permutations=5000,
                                                          tail=0,
                                                          connectivity=connectivity_sparse,
                                                          n_jobs=4, seed=10,
                                                          max_step=1, t_power=1,
                                                          out_type='indices',
                                                          exclude=None,
                                                          step_down_p=0,
                                                          check_disjoint=False,
                                                          buffer_size=1000)

    np.save(results_dir + mode + '_max_clu_lens_' + freq + window + cons, max_clu_lens)

    max_clu_lens = np.load(results_dir + mode + '_max_clu_lens_' + freq + window + cons + '.npy')

    # null distribution
    plt.figure(0)
    plt.hist(max_clu_lens)
    kde = stats.gaussian_kde(max_clu_lens)
    x = np.linspace(max_clu_lens.min(), max_clu_lens.max(), 100)
    p = kde(x)
    # cutoff for a cluster size that is significant
    plt.figure(1)
    plt.plot(x, p)
    plt.hlines(0.05, 0, 14) # visualization of cutoff
    cutoff = 7 # manually from plot above and kde(x)

    max_clu_lens2, clusters = _permutation_cluster_test_AT(r_mantel,
                                                           threshold=threshold[thres_id][0][0][0],
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

    # get p-values for all clusters
    p = kde(clu_lens)

    # out in format required by MNE cluster function (for visualization)
    r_mantel_out = r_mantel.reshape(1, 20484)
    clusters_new = clusters
    for c, l, i in zip(clusters, clu_lens, range(0, len(clusters))):
        clusters_new[i] = np.zeros(np.int(l), dtype='int'), c[0]

    clu = r_mantel_out, clusters_new, p
    np.save(results_dir + mode + '_clu_' + freq + window + cons, clu)

    # see how many clusters exceed the threshold (i.e. survive the correction)
    ids = np.where(clu_lens > cutoff)[0]
    clu_sig = clusters[0:len(ids)]
    for i in range(0, len(ids)):
        clu_sig[i] = clusters[ids[i]]

    sig_clu_lens = np.zeros(len(clu_sig))
    for j in range(0, len(clu_sig)):
        sig_clu_lens[j] = len(clu_sig[j][0])
