function isc_user_interface()
% ISC function with parameters used for second speech part. For explanations, refer to isc_user_interface.m

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
parameters.subjects=['sme_001';  'sme_002'; 'sme_005'; 'sme_006'; 'sme_007';
    'sme_009'; 'sme_012'; 'sme_019'; 'sme_026'; 'sme_027'; 'sme_029';
    'sme_034'; 'sme_035'; 'sme_036'; 'sme_037'; 'sme_039'; 'sme_042'; 'sme_043';
    'sme_048'; 'sme_049'; 'sme_050'];

subj_folder='/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/';
parameters.folders={};
for i=1:size(parameters.subjects,1)
    parameters.folders{i,1}=[subj_folder, parameters.subjects(i,(1:end))];
end
parameters.spacing='oct6';
parameters.sf=1000;
parameters.trig_ch=378;
parameters.lowpassfrequency=0.3;
parameters.downsamplefrequency=10;
parameters.order=3;
parameters.window=327;
parameters.thresholding=0;
parameters.thresholdlevel=0.05/2;
parameters.inv_op='inv.mat';
parameters.pattern = {'a';'b';'c';'d';'e';'f';'g';'h';'l';'m';'speech*_ssp.fif'};
parameters.invname = {'a';'b';'c';'d';'e';'f';'g';'h';'l';'m';'speech'};
parameters.fileids=11;
frequencies=[0.5 4; 4 8; 8 12; 12 25; 25 45; 55 90];
possible_styles={'beginning_time', 'start_time', 'start_end', 'define_start'};
choice_of_style='define_start';
load('/media/cbru/SMEDY/scripts_speech_rest/ISC/modtimes_speech_A/modtimes_1_plus_extra_subjects.mat');
start_time=all_modtimes(2,:);
parameters.stimulus_time=[0,0,0,0,0,0,0,0,0,0,300];
style=find(ismember(possible_styles,choice_of_style));
parameters.length_style=style;
parameters.length_stimulus_start=start_time;

%Rejection options:
parameters.eog_rejection=0;
parameters.mag_rejection=0;
parameters.grad_rejection=0;
parameters.eog_ch=[307, 308];
parameters.grad_threshold=1e-01;
parameters.mag_threshold=10e-03;
parameters.eog_threshold=10e-02;

%Option for dynamic statistical parameteric mapping (normalizing estimates
%in terms of noise sensitivity at each spatial location)
parameters.dSPM=1;

%When analyzing new files, these should be on:
parameters.should_the_inverse_operators_be_updated=0;
parameters.should_the_length_of_the_files_be_reestimated=0;

%Shortcuts to calculate only energy envelopes, only correlations or only group averages. Useful
%when the envelopes have already been estimated and morphed, or when processing large number of files,
%as one can just leave the program running unattended (otherwise you would have to confirm that you have
%completed the MNE morphing). NOTE: these are mutually exclusive:
parameters.envelopes_only=0;
parameters.correlations_only=0;
parameters.averages_only=1;

%An estimation of the number of correlation coefficients (the length of your file in seconds divided by the length of the correlation window in seconds rounded up to an integer) if calculating
%only a new group average; otherwise can be left untouched. For example, with 884 second movie, 20 second window results in 45 corralation "frames"
parameters.frames=1;

%If you plan to change the morphgrade from the default 5 when morphing, let
%the script know it here (allowed morhpgrades are 3,4,5, and 6):
parameters.morphgrade=5;

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

