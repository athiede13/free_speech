# Statistics

Files in this folder:

1. make_corr_matrix.m - Combine all ISC results into one big matrix.
1. make_models.m - Create group models.
1. isc_models.mat - Output from make_models.m
1. combine_corr_matrices_speech1_2.m - Make weighted average of speech correlation matrices for part 1 and 2.
1. make_colorbar.m - Create colorbar for visualization of results.
1. extract_MNI_coord.py - Extract maximum-value MNI coordinates from statistical maps (see subfolders).

## ISCs_sign_one_sample_perm - One-sample *t*-test for ISC significance in each group

Files in this subfolder:

1. plot_stats_cluster_spatio_temporal_1samp.py - Permutation-based *t*-test for ISCs with cluster correction.
1. summarize_clusters_stc_AT.py - Helper function modified from MNE to prepare clusters for visualization.
1. plot_ISC_subplots_T_vals.py - Visualization on brain surface.

## contrast_cluster_perm - Group difference maps

Files in this subfolder:

1. ttest_cluster_permutation.py - Permutation-based *t*-test for ISC group comparison with cluster correction.
1. ttest_ind_no_p.py - Independent-samples *t*-test function from [SciPy](https://docs.scipy.org/doc/scipy/reference/index.html#module-scipy) modified to not return *p*-value.
1. visualize_clusters_t.py - Visualize clusters on brain surface.
1. plot_ISC_subplots3.py - Visualization on brain surface.

## mantel - Mantel test

Files in this subfolder:

1. make_models.m - Create group models for groups and reading-related measures.
1. isc_models.mat - Models created by make_models.m
1. plot_joint_scores.py - Combine joint-scores plots of reading-related measures into one Figure.
1. run_regressions_mantel.m - Perform Mantel test.
1. bramila_mantel.m - Actual Mantel test function. Required by run_regressions_mantel.m, from BraMiLa: https://version.aalto.fi/gitlab/BML/bramila/tree/master
1. output/ - files created by run_regressions_mantel.m
1. cluster_correction.py - Correct Mantel statistics with cluster-based algorithm implemented in MNE.
1. permutation_cluster_test_AT.py - Modified MNE function to perform cluster permutation and return size of largest cluster.
1. visualize_clusters.py - Visualize clusters on brain surface.
1. summarize_clusters_stc_AT.py - Helper function modified from MNE to prepare clusters for visualization.
1. clusters_max_correlation.py - Find maximum correlation between ISC and reading score in cluster and plot
scatter plot with regression line.
1. plot_ISC_subplots_mantel.py - Visualization on brain surface.
