"""
Find maximum correlation between ISC and reading score in cluster and plot
scatter plot with regression line.

Inspired by MNE Tutorial.

@author: Anja Thiede <anja.thiede@helsinki.fi>
"""

import datetime
import numpy as np
import scipy.io as sio
from scipy import stats
import matplotlib.pyplot as plt

#%matplotlib qt
#%matplotlib inline

now = datetime.datetime.now()
SUBJECTS_DIR = '/media/cbru/SMEDY/DATA/MRI_data/MRI_orig/'
results_path = '/media/cbru/SMEDY/results/mantel_correlations/2019_05_simple_model/'
corr_matrix_path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/'
behav_file = '/media/cbru/SMEDY/DATA/nepsy/behav_vecs.mat'

condition = '_1' # 1 speech
cluster = 0 # 0 largest cluster, 1 second-largest cluster, etc.

# everything after this in order (only significant correlations):
# phonological processing: delta, theta, alpha, beta, low gamma, high gamma
# technical reading: delta, theta, alpha, beta, low gamma
# working memory: delta
# IQ: delta, high gamma

fres = ['5.000000e-01-4Hz_', '4-8Hz_', '8-12Hz_', '12-25Hz_', '25-45Hz_', '55-90Hz_',
        '5.000000e-01-4Hz_', '4-8Hz_', '8-12Hz_', '12-25Hz_', '25-45Hz_',
        '5.000000e-01-4Hz_',
        '5.000000e-01-4Hz_', '55-90Hz_']
nepsys = ['phon', 'phon', 'phon', 'phon', 'phon', 'phon',
          'read', 'read', 'read', 'read', 'read',
          'mem',
          'iq', 'iq']
isc_files = [corr_matrix_path + 'corr_matrix_5.000000e-01-4Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_4-8Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_8-12Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_12-25Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_25-45Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_55-90Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_5.000000e-01-4Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_4-8Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_8-12Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_12-25Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_25-45Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_5.000000e-01-4Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_5.000000e-01-4Hz_613_1.mat',
             corr_matrix_path + 'corr_matrix_55-90Hz_613_1.mat'
             ]
clu_files = [results_path + 'phon_clu_5.000000e-01-4Hz_613_1.npy',
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

# IDs of dys and con pairs in the isc vector
idCon = sio.loadmat('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/idCon.mat')
idDys = sio.loadmat('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/idDys.mat')
idCon = idCon['idCon']
idDys = idDys['idDys']
n_CON_pairs, n_DYS_pairs = len(idCon), len(idDys)
cutoff = 25

for i in range(0, len(isc_files)):
    # load isc correlation matrix
    orig_isc = sio.loadmat(isc_files[i])
    orig_isc = orig_isc['all_data'] # this is the vector 20484x946

    # load behav vector
    orig_behav = sio.loadmat(behav_file)
    mean_behav = orig_behav['mean_' + nepsys[i] + '_vec'] # this is a vector 946x1

    # load clu
    print('loading ' + clu_files[i])
    clu = np.load(clu_files[i])
    r_obs, clusters = clu
    
    # thresholding by cluster length
    good_cluster_inds = []
    clusters2 = []
    for ii in range(0, len(clusters)):
        if len(clusters[ii][1]) > (cutoff-1):
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
        
        out2 = out.copy()
        out2.sort(reverse=True)
        if len(out)<=cluster:
            print('Only ', len(out), ' cluster(s) significant')
        else:
            id_max = out.index(out2[cluster]) # largest, second-largest, etc.
            inds_t, inds_v = [(clusters[cluster_ind]) for ii, cluster_ind in
                              enumerate(good_cluster_inds)][id_max]
            cluster_r = r_obs[inds_t, inds_v].mean()
            print(len(inds_v), 'id ', id_max)
            print('r=', cluster_r)   
    
            # isc values at the significant vertices of selected cluster
            sign_isc = orig_isc[inds_v, :]
            mean_isc = sign_isc.mean(axis=0)
        
            # mean isc and behav separately for groups for plotting
            mean_isc_dys = mean_isc[idDys-1] # ISCs dyslexics
            mean_isc_con = mean_isc[idCon-1] # ISCs controls
            mean_behav_dys = mean_behav[idDys-1]
            mean_behav_con = mean_behav[idCon-1]
        
            # plot correlation
            fig = plt.figure()
            fig.set_size_inches(5, 5)
            colors = ['lightgrey', 'olive', 'blue']
            legend = ['mixed', 'dys', 'con']
            s = 10 # size of markers for scatterplot
            linewidth = 1
            # fontsizes
            SMALL_SIZE = 20
            MEDIUM_SIZE = 20
            BIGGER_SIZE = 20
        
            plt.rcParams['font.family'] = "serif"
            plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
            plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
            plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
            plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
            plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
            plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
            plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
            # fontsizes end
            plt.scatter(mean_behav, mean_isc, s=s, linewidth=linewidth, color=colors[0])
            plt.scatter(mean_behav_dys, mean_isc_dys, s=s, linewidth=linewidth,
                        color=colors[1])
            plt.scatter(mean_behav_con, mean_isc_con, s=s, linewidth=linewidth,
                        color=colors[2])
        
            # calculate linear regression line with generated linear fit
            slope, intercept, r_value, p_value, std_err = \
                stats.linregress(mean_behav.reshape(946), mean_isc)
            line = slope*mean_behav+intercept
            if p_value < 0.001:
                star = '***'
            elif p_value < 0.01:
                star = '**'
            elif p_value < 0.05:
                star = '*'
            else:
                star = 'n.s.'
            plt.plot(mean_behav, line, color='orange', linewidth=2)
            if nepsys[i] == 'phon':
                plt.xlabel(nepsys[i] + ' (z)')
                plt.xlim(-2, 1.2)
            elif nepsys[i] == 'read':
                plt.xlabel(nepsys[i] + ' (z)')
                plt.xlim(-2, 1.2)
            elif nepsys[i] == 'iq':
                plt.xlabel(nepsys[i] + ' (std score)')
            elif nepsys[i] == 'mem':
                plt.xlabel(nepsys[i] + ' (std score)')
            plt.ylim(-0.1, 0.35)
            plt.ylabel('ISC (r)')
            plt.box(False)
            plt.grid(False)
            plt.title('n=' + str(len(inds_v)) + ', r=' + str(cluster_r.round(2)),
                      y=1.1)
            plt.tight_layout(rect=[0, 0, 1, 1])
            plt.show()
#            if cluster == 0:
#                fig.savefig(results_path + '/max_cluster_corr_' + fres[i] + 
#                            nepsys[i] + condition + '.png', dpi=600)
#            else:
#                fig.savefig(results_path + '/max_' + str(cluster) + 
#                            'cluster_corr_' + fres[i] + nepsys[i] + 
#                            condition + '.png', dpi=600)
