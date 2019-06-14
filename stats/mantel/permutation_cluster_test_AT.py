"""
MNE function to perform cluster permutation test. Changed to return maximal size of cluster.

Created on Fri Mar  1 10:27:19 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import numpy as np
from mne.parallel import check_n_jobs
from mne.stats import cluster_level
from mne.utils import logger

def _permutation_cluster_test_AT(X, threshold, tail, n_permutations,
                                 connectivity, n_jobs, seed, max_step,
                                 exclude, step_down_p, t_power, out_type,
                                 check_disjoint, buffer_size):
    n_jobs = check_n_jobs(n_jobs)
    """Aux Function.
    Note. X is required to be a list. Depending on the length of X
    either a 1 sample t-test or an F test / more sample permutation scheme
    is elicited.
    """
    if out_type not in ['mask', 'indices']:
        raise ValueError('out_type must be either \'mask\' or \'indices\'')
    if not isinstance(threshold, dict) and (tail < 0 and threshold > 0 or
                                            tail > 0 and threshold < 0 or
                                            tail == 0 and threshold < 0):
        raise ValueError('incompatible tail and threshold signs, got %s and %s'
                         % (tail, threshold))

    # check dimensions for each group in X (a list at this stage).
    X = [x[:, np.newaxis] if x.ndim == 1 else x for x in X]
    n_times = X[0].shape[0]

    sample_shape = X[0].shape[1:]
    for x in X:
        if x.shape[1:] != sample_shape:
            raise ValueError('All samples mush have the same size')

#    # flatten the last dimensions in case the data is high dimensional
#    X = [np.reshape(x, (x.shape[0], -1)) for x in X]
    n_tests = X[0].shape[1]

    if connectivity is not None and connectivity is not False:
        connectivity = cluster_level._setup_connectivity(connectivity, n_tests, n_times)

    if (exclude is not None) and not exclude.size == n_tests:
        raise ValueError('exclude must be the same shape as X[0]')

    # determine if connectivity itself can be separated into disjoint sets
    if check_disjoint is True and (connectivity is not None and
                                   connectivity is not False):
        partitions = cluster_level._get_partitions_from_connectivity(connectivity, n_times)
    else:
        partitions = None
    max_clu_lens = np.zeros(n_permutations)
    for i in range(0, n_permutations):
        #logger.info('Running initial clustering')
        include = None
        out = cluster_level._find_clusters(X[i][0], threshold, tail, connectivity,
                                           max_step=max_step, include=include,
                                           partitions=partitions, t_power=t_power,
                                           show_info=True)
        clusters, cluster_stats = out

        logger.info('Found %d clusters' % len(clusters))

        # convert clusters to old format
        if connectivity is not None and connectivity is not False:
            # our algorithms output lists of indices by default
            if out_type == 'mask':
                clusters = cluster_level._cluster_indices_to_mask(clusters, n_tests)
        else:
            # ndimage outputs slices or boolean masks by default
            if out_type == 'indices':
                clusters = cluster_level._cluster_mask_to_indices(clusters)

        # The clusters should have the same shape as the samples
        clusters = cluster_level._reshape_clusters(clusters, sample_shape)
        max_clu_len = 0
        for j in range(0, len(clusters)):
            max_new = len(clusters[j][0])
            if max_new > max_clu_len:
                max_clu_len = max_new
        logger.info('Max cluster length %d' % max_clu_len)
        max_clu_lens[i] = max_clu_len
    return max_clu_lens, clusters
