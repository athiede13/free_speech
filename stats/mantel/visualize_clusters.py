"""
Visualize cluster results.

Created on Wed Feb 27 15:09:19 2019
@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

from os.path import basename
import numpy as np
from summarize_clusters_stc_AT import summarize_clusters_stc_AT

#%matplotlib qt

subjects_dir = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/'

# to fill, needed if this script is not used directly after cluster_correction.py
results_dir = '/media/cbru/SMEDY/results/mantel_correlations/2019_05_simple_model/'
colorbar = False

# load sign clu
# correlations simple model
files = (results_dir + 'iq_clu_5.000000e-01-4Hz_613_1.npy',
         results_dir + 'iq_clu_55-90Hz_613_1.npy',
         results_dir + 'mem_clu_5.000000e-01-4Hz_613_1.npy',
         results_dir + 'phon_clu_5.000000e-01-4Hz_613_1.npy',
         results_dir + 'phon_clu_4-8Hz_613_1.npy',
         results_dir + 'phon_clu_8-12Hz_613_1.npy',
         results_dir + 'phon_clu_12-25Hz_613_1.npy',
         results_dir + 'phon_clu_25-45Hz_613_1.npy',
         results_dir + 'phon_clu_55-90Hz_613_1.npy',
         results_dir + 'read_clu_5.000000e-01-4Hz_613_1.npy',
         results_dir + 'read_clu_4-8Hz_613_1.npy',
         results_dir + 'read_clu_8-12Hz_613_1.npy',
         results_dir + 'read_clu_12-25Hz_613_1.npy',
         results_dir + 'read_clu_25-45Hz_613_1.npy'
         )

print('Visualizing clusters.')
cutoff = 25 # max cluster length of surrogate values across all frequencies and behavioural data

for file in files:
    print(file)
    clu = np.load(file)
    r_obs, clusters = clu
    # thresholding by cluster length
    good_cluster_inds = []
    clusters2 = []
    for ii in range(0, len(clusters)):
        if len(clusters[ii][1]) > (cutoff-1):
            good_cluster_inds.append(ii)
            clusters2.append(clusters[ii])
        clu2 = r_obs, clusters2, np.zeros(len(clusters2)), _
    if not clusters2:
        print('All clusters are smaller than the minimal length.')
    else:
        # Investigating the significant effects / Find max cluster
        out = []
        for j in range(0, len(good_cluster_inds)):
            inds_t, inds_v = [(clusters[cluster_ind]) for ii, cluster_ind in
                              enumerate(good_cluster_inds)][j]
            out.append(len(inds_v)) # max cluster is xxth
    
        id_max = out.index(max(out))
        inds_t, inds_v = [(clusters[cluster_ind]) for ii, cluster_ind in
                          enumerate(good_cluster_inds)][id_max]
        print(len(inds_v))
        #summarize clusters
        stc_all_cluster_vis = summarize_clusters_stc_AT(clu2, p_thresh=0.05,
                                                        tstep=1e-3, tmin=0,
                                                        subject='fsaverage',
                                                        vertices=None)
        
        # checkup for cluster lengths
        # find the cluster with most non-zero values
        count = []
        for c in range(0, stc_all_cluster_vis.data.shape[1]):
            nz = np.nonzero(stc_all_cluster_vis.data[:, c])
            count.append(len(nz[0]))
        max_le = count.index(max(count[1:]))
        
        for hemi in {'lh', 'rh'}:
            clim = dict(kind='value', pos_lims=[-0.3, 0, 0.3])
            brain = stc_all_cluster_vis.plot(subjects_dir=subjects_dir,
                                             views='lat', clim=clim,
                                             colorbar=colorbar, colormap='mne',
                                             hemi=hemi,
                                             alpha=0.8, time_label=None,
                                             transparent=True,
                                             background='white',
                                             title=basename(file)[:-4]+'-'+hemi)
            # fix for look-through visualization of the brain
            brain.data['surfaces'][0].actor.property.backface_culling = True
            brain.show_view('lateral')
#                brain.data['colorbar'].number_of_labels = 3
#                brain.save_single_image(results_dir + 'colorbar.png')
            brain.save_single_image(results_dir + basename(file)[:-4]+'_lat-'+ hemi + '.png')
            brain.show_view('medial')
            brain.save_single_image(results_dir + basename(file)[:-4]+'_med-'+ hemi + '.png')
            brain.close()
