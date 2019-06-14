function isc_user_interface()
% This is the only function the user needs to fill in all details for inter-subject correlation (ISC) computation and run. Calls all subsequently needed steps.

%THINGS TO FILL OUT:
addpath /home/cbru/MNE-2.7.0-3106-Linux-x86_64/share/matlab/ %local path to MNE

% all subjects original
% parameters.subjects=['sme_001';  'sme_002'; 'sme_003'; 'sme_004'; 'sme_005';
%     'sme_006'; 'sme_007'; 'sme_008'; 'sme_009'; 'sme_010';
%     'sme_011'; 'sme_012'; 'sme_013'; 'sme_014'; 'sme_015';
%     'sme_016'; 'sme_017'; 'sme_019'; 'sme_020';
%     'sme_022'; 'sme_024'; 'sme_025';
%     'sme_026'; 'sme_027'; 'sme_028'; 'sme_029';
%     'sme_031'; 'sme_032'; 'sme_034'; 'sme_035';
%     'sme_036'; 'sme_037'; 'sme_038'; 'sme_039'; 'sme_040';
%     'sme_042'; 'sme_043'; 'sme_044'; 'sme_045';
%     'sme_046'; 'sme_047'; 'sme_048'; 'sme_049'; 'sme_050'];
% % exclusion reasons:
% % SME018, SME021, SME030, SME041 no MRI, SME033 no MRI, no MEG
% % no trigger codes for SME023

% % dyslexics updated
% parameters.subjects=['sme_003'; 'sme_004'; 'sme_008';
% 'sme_010'; 'sme_011'; 'sme_013'; 'sme_014'; 'sme_015'; 'sme_016'; 'sme_017';
% 'sme_020'; 'sme_022'; 'sme_024'; 'sme_025'; 'sme_028'; 'sme_031'; 'sme_032';
% 'sme_038'; 'sme_040'; 'sme_044'; 'sme_045'; 'sme_046'; 'sme_047'];
% controls updated
% parameters.subjects=['sme_001';  'sme_002'; 'sme_005'; 'sme_006'; 'sme_007';
% 'sme_009'; 'sme_012'; 'sme_019'; 'sme_026'; 'sme_027'; 'sme_029';
% 'sme_034'; 'sme_035'; 'sme_036'; 'sme_037'; 'sme_039'; 'sme_042'; 'sme_043';
% 'sme_048'; 'sme_049'; 'sme_050'];

subj_folder='/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/';
% create a loop to name the subject folders
parameters.folders={};
for i=1:size(parameters.subjects,1)
    parameters.folders{i,1}=[subj_folder, parameters.subjects(i,(1:end))];	%where your measurement files can be found
end
parameters.spacing='oct6';  %spacing used in mne_setup_source_space
parameters.sf=1000; %sampling frequency
parameters.trig_ch=378; %the number of trigger channel (STI101)
parameters.lowpassfrequency=0.3; % cut-off frequency for low-pass filters; should always be smaller than half of sampling frequency after downsampling (Nyqvist)
parameters.downsamplefrequency=10; %sampling frequency after downsampling
parameters.order=3; %order of bandpass and low-pass filters; being conservative is recommended to avoid ringing
parameters.window=327; % in seconds; how long is the time span for which ISCs should be calculated
parameters.thresholding=0;%statistical thresholding, 1=on, 0=off; rejects correlation coefficients with p<thresholdlevel (below); keeping this on might mean that there is not enough values for visualization
% note: if the parametrical tresholding is on, then the permutation t-test
% cannot be run afterwards, meaning better to keep it off
parameters.thresholdlevel=0.05/2;
parameters.inv_op='inv.mat'; %ending fo inverse operator in Matlab; used in creating the name for the file in which inv operator is stored
parameters.fileids = 11; % an integer for each file type or trial; allows to run same analysis for files with exactly the same parameters
parameters.pattern = {'a';'b';'c';'d';'e';'f';'g';'h';'l';'m';'speech*_ssp.fif'};% insert a pattern and make sure only one file per subject is found following this pattern; in order of parameters.fileids
parameters.invname = {'a';'b';'c';'d';'e';'f';'g';'h';'l';'m';'speech'}; % in order of parameters.fileids
frequencies=[0.5 4; 4 8; 8 12; 12 25; 25 45; 55 90]; %the frequency bands to be analyzed; one band per row, for example [8 12; 14 22] etc.
%How to determine the length of the times when stimulus is on:
possible_styles={'beginning_time', 'start_time', 'start_end', 'define_start'};
%'beginning_time'=starts at the beginning of the file, ends after the time determined by the parameter below
%'start_time'=starts at the start trigger, ends after the time determined by the parameter below
%'start_end'=starts at the start trigger, ends at the end trigger
%'define_start'=starts looking for a trigger at the time defined (start_time), ends at the end trigger
choice_of_style='define_start';
start_time=all_modtimes(2,:); %time in seconds that the trigger of interest starts earliest
parameters.stimulus_time=[0,0,0,0,0,0,0,0,0,0,300]; %time during which the stimulus is on in each file type (in seconds, and in order of parameters.fileids); needs to be exact when no end trigger is present. If end trigger is present, then it can be an estimate (rather estimate too low than too high).
style=find(ismember(possible_styles,choice_of_style));
parameters.length_style=style;
parameters.length_stimulus_start=start_time;

%Rejection options:
parameters.eog_rejection=0; %0=off, 1=on
parameters.mag_rejection=0; %0=off, 1=on; mag refers to magnetometers
parameters.grad_rejection=0; %0=off, 1=on; grad refers to (magnetic) gradiometers
parameters.eog_ch=[307, 308];   %numbers of eog-channels in measurement file
%Rejection thresholds should be determined from the data
parameters.grad_threshold=1e-01;    %rejects seconds during which the maximum variation in any gradiometer channel is bigger than this
parameters.mag_threshold=10e-03;    %rejects seconds during which the maximum variation in any magnetometer channel is bigger than this
parameters.eog_threshold=10e-02;   %rejects seconds during which the maximum variation in any eog-channel is bigger than this

%Option for dynamic statistical parameteric mapping (normalizing estimates
%in terms of noise sensitivity at each spatial location)
parameters.dSPM=1; %0=off, 1=on

%When analyzing new files, these should be on:
parameters.should_the_inverse_operators_be_updated=0; %0=off, 1=on
parameters.should_the_length_of_the_files_be_reestimated=0; %0=off, 1=on

%Shortcuts to calculate only energy envelopes, only correlations or only group averages. Useful
%when the envelopes have already been estimated and morphed, or when processing large number of files,
%as one can just leave the program running unattended (otherwise you would have to confirm that you have
%completed the MNE morphing). NOTE: these are mutually exclusive:
parameters.envelopes_only=0; %0=off, 1=on
parameters.correlations_only=0; %0=off, 1=on; NOTE: morphing has to be done and up to date to use this option
parameters.averages_only=1; %0=off, 1=on

%An estimation of the number of correlation coefficients (the length of your file in seconds divided by the length of the correlation window in seconds rounded up to an integer) if calculating
%only a new group average; otherwise can be left untouched. For example, with 884 second movie, 20 second window results in 45 corralation "frames"
parameters.frames=1;

%If you plan to change the morphgrade from the default 5 when morphing, let
%the script know it here (allowed morhpgrades are 3,4,5, and 6):
parameters.morphgrade=5;

%NOTE: you should just add '_MNE' to the end of energy envelope file
%name when morphing (or change the naming here); for example:
%mne_make_movie --stcin 3140_energy_60-90Hz_2 --stc 3140_energy_60-90Hz_2_MNE --smooth 5 --morph fsaverage
%morphs stc file 3140_energy_60-90Hz_2 into average anatomy and then
%saves the result as 3140_energy_60-90Hz_2_MNE (also stc-file)

%END OF THINGS TO FILL OUT

flag=0;

%reminder to morph the energy envelopes into average anatomy before trying
%to calculate the correlations:
if parameters.correlations_only==1
    if parameters.envelopes_only==1
        fprintf(1, 'Please use only one shortcut at a time.\n')
        return
    elseif parameters.averages_only==1
        fprintf(1, 'Please use only one shortcut at a time.\n')
        return
    else
        text=sprintf('Are you done with command line MNE-processing (morphing)? (y/n): '); %you can only proceed if you are
        yes_no=input(text,'s');
        if (yes_no=='n')
            flag=1;
            fprintf(1,'Please finish morphing before trying to calculate correlations.\n')
        end
    end
end
if parameters.envelopes_only==1
    if parameters.correlations_only==1
        fprintf(1, 'Please use only one shortcut at a time.\n')
        return
    elseif parameters.averages_only==1
        fprintf(1, 'Please use only one shortcut at a time.\n')
        return
    end
end
if parameters.averages_only==1
    if parameters.correlations_only==1
        fprintf(1, 'Please use only one shortcut at a time.\n')
        return
    elseif parameters.envelopes_only==1
        fprintf(1, 'Please use only one shortcut at a time.\n')
        return
    end
end
if flag==0
    for i=1:size(parameters.fileids,2)
        for j=1:size(frequencies, 1)
            isc_energy_envelopes(parameters.fileids(i),frequencies(j,:),parameters);
        end
    end
end

