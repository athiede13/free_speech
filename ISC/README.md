# Inter-subject correlation (ISC)

Files in this folder:

1. isc_user_interface.m - Only function that needs to be touched by user. User defines variables and this script will call the required functions. Example with detailed explanations of variables.
1. isc_user_interface_10.m - User interface function filled for speech part 1.
1. isc_user_interface_11.m - User interface function filles for speech part 2.
1. isc_main_energy.m - Wrapper function to call correct functions depending on user input.
1. isc_inverse.m - Save inverse operators in .mat format.
1. save_names.mat - Output from isc_inverse.m
1. isc_start_finish.m - Calculate file lengths.
1. modtimes_10.mat - Output from isc_start_finish.m for speech part 1.
1. modtimes_11.mat - Output from isc_start_finish.m for speech part 2.
1. isc_energy_envelopes.m - Wrapper function to create filenames and call correct functions to create envelopes of the MEG signal.
1. isc_energy_amplitude.m - Make energy envelopes for each frequency band.
1. morph_to_fsaverage.py - Morph envelopes to average subject. Step independent of Matlab ISC functions.
1. isc_correlation_energy.m - Calculate pair-wise correlations (ISCs).
1. isc_average_energy_alt.m - Calculate group averages.
