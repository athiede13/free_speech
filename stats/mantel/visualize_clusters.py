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
p_thresh = 0.05
mode = 'phon' # 'iq' or 'read' or 'mem' or 'phon'
freq = {'5.000000e-01-4Hz', '4-8Hz', '8-12Hz', '12-25Hz', '25-45Hz', '55-90Hz'} #frequency bands
cons = '_1' # '_1' listening to speech
if cons == '_1':
    window = '_613'
elif cons == '_2':
    window = '_579'
else:
    print('Check condition!')

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
cutoffs = [12, 9, 10, 13, 11, 12, 10, 8, 9, 12, 9, 10, 10, 12]

for file, cutoff in zip(files, cutoffs):
    print(file, cutoff)
    clu = np.load(file)
    r_obs, clusters, cluster_p_values, H0 = clu
    # thresholding by p-val
    good_cluster_inds = np.where(cluster_p_values < p_thresh)[0]
    if not good_cluster_inds.any():
        print('No significant clusters available for file ' + file + '\n')
        print('The smallest corrected p-value is '+str(min(cluster_p_values)))
    else:
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
                                                            vertices=None)

            for hemi in {'lh', 'rh'}:
                clim = dict(kind='value', lims=[0, 0.15, 0.3])
                brain = stc_all_cluster_vis.plot(subjects_dir=subjects_dir,
                                                 views='lat', clim=clim,
                                                 colorbar=False, hemi=hemi,
                                                 alpha=1, time_label=None,
                                                 transparent=True,
                                                 background='white',
                                                 title=basename(file)[:-4]+'-'+hemi)
                # fix for look-through visualization of the brain
                brain.data['surfaces'][0].actor.property.backface_culling = True
                brain.show_view('lateral')
                brain.data['colorbar'].number_of_labels = 3
                brain.save_single_image(results_dir + basename(file)[:-4]+'_lat-'+ hemi + '.png')
                brain.show_view('medial')
                brain.save_single_image(results_dir + basename(file)[:-4]+'_med-'+ hemi + '.png')
                brain.close()
