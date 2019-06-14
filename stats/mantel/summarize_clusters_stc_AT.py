"""
MNE function to get all clusters in one SourceEstimate. Slightly changed.

Created on Wed Feb 27 15:06:01 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import numpy as np
from mne.source_estimate import SourceEstimate

def summarize_clusters_stc_AT(clu, p_thresh=0.05, tstep=1e-3, tmin=0,
                              subject='fsaverage', vertices=None):
    """Assemble summary SourceEstimate from spatiotemporal cluster results.
    This helps visualizing results from spatio-temporal-clustering
    permutation tests.
    Parameters
    ----------
    clu : tuple
        the output from clustering permutation tests.
    p_thresh : float
        The significance threshold for inclusion of clusters.
    tstep : float
        The temporal difference between two time samples.
    tmin : float | int
        The time of the first sample.
    subject : str
        The name of the subject.
    vertices : list of arrays | None
        The vertex numbers associated with the source space locations. Defaults
        to None. If None, equals ```[np.arange(10242), np.arange(10242)]```.
    Returns
    -------
    out : instance of SourceEstimate
        A summary of the clusters. The first time point in this SourceEstimate
        object is the summation of all the clusters. Subsequent time points
        contain each individual cluster. The magnitude of the activity
        corresponds to the length the cluster spans in time (in samples).
    """
    if vertices is None:
        vertices = [np.arange(10242), np.arange(10242)]

    r_obs, clusters, clu_pvals, _ = clu
    n_times, n_vertices = r_obs.shape
    good_cluster_inds = np.where(clu_pvals < p_thresh)[0]

    #  Build a convenient representation of each cluster, where each
    #  cluster becomes a "time point" in the SourceEstimate
    if len(good_cluster_inds) == 0:
        raise RuntimeError('No significant clusters available. Please adjust '
                           'your threshold or check your statistical '
                           'analysis.')
    data = np.zeros((n_vertices, n_times))
    data_summary = np.zeros((n_vertices, len(good_cluster_inds) + 1))
    for ii, cluster_ind in enumerate(good_cluster_inds):
        data.fill(0)
        v_inds = clusters[cluster_ind][1]
        r_inds = clusters[cluster_ind][0]
        data[v_inds, r_inds] = r_obs[r_inds, v_inds]
        # Store a nice visualization of the cluster by summing across time
#        data = np.sign(data) * np.logical_not(data == 0) * tstep
        data_summary[:, ii + 1] = np.sum(data, axis=1)
        # Make the first "time point" a sum across all clusters for easy
        # visualization
    data_summary[:, 0] = np.sum(data_summary, axis=1)

    return SourceEstimate(data_summary, vertices, tmin=tmin, tstep=tstep,
                          subject=subject)
    