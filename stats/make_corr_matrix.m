% Import pairwise correlation .stc files to Matlab and create one huge data matrix.

% author: Anja Thiede <anja.thiede@helsinki.fi>

addpath /home/cbru/MNE-2.7.0-3106-Linux-x86_64/share/matlab/ %local path to MNE

% read in in the same order as in the model created by make_models_free_speech.m
% (here first dyslexics and then non-dyslexics)
subj_list={
    'sme_003';
    'sme_004';
    'sme_008';
    'sme_010';
    'sme_011';
    'sme_013';
    'sme_014';
    'sme_015';
    'sme_016';
    'sme_017';
    'sme_020';
    'sme_022';
    'sme_024';
    'sme_025';
    'sme_028';
    'sme_031';
    'sme_032';
    'sme_038';
    'sme_040';
    'sme_044';
    'sme_045';
    'sme_046';
    'sme_047';
    'sme_001';
    'sme_002';
    'sme_005';
    'sme_006';
    'sme_007';
    'sme_009';
    'sme_012';
    'sme_019';
    'sme_026';
    'sme_027';
    'sme_029';
    'sme_034';
    'sme_035';
    'sme_036';
    'sme_037';
    'sme_039';
    'sme_042';
    'sme_043';
    'sme_048';
    'sme_049';
    'sme_050'
    };

[row, columns]=ind2sub([length(subj_list) length(subj_list)],find(triu(ones(length(subj_list)),1)));

%TO BE SET
frequencies={'5.000000e-01-4Hz','4-8Hz','8-12Hz','12-25Hz','25-45Hz','55-90Hz'};
condition={'_10'}; % '_10' speech 1, '_11' speech 2
window='_286'; % '_286' speech 1, '_327' speech 2

for f=1:length(frequencies)
    for s=1:length(condition)
        Npwcorr=length(row);%length of rows of the lower triangle
        
        all_data=zeros(20484,Npwcorr);
        lhrh=zeros(20484,1);
        
        for r=1:length(row)
            if strcmp(subj_list(row(r)),'E12100')==1||strcmp(subj_list(columns(r)),'E12028')==1 %blacklist
                all_data(:,r)=zeros;
            else
                s_r=char(subj_list(row(r)));
                s_c=char(subj_list(columns(r)));
                s_r2=str2double(s_r(2:end));
                s_c2=str2double(s_c(2:end));
                if s_c2<s_r2%filenames are stored in alphabetical ascending order, meaning lower subject_id first, higher subject_id last
                    s1=s_c;
                    s2=s_r;
                else
                    s1=s_r;
                    s2=s_c;
                end
                read_lh=strcat('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/average/',s1,'_',s2,'_cor_en_',frequencies{f},window,condition{s},'-lh.stc');
                if exist(read_lh, 'file') == 2
                    stc_l=mne_read_stc_file(read_lh);
                else
                    read_lh=strcat('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/average/',s2,'_',s1,'_cor_en_',frequencies{f},window,condition{s},'-lh.stc');
                    stc_l=mne_read_stc_file(read_lh);
                end
                read_rh=strcat('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/average/',s1,'_',s2,'_cor_en_',frequencies{f},window,condition{s},'-rh.stc');
                if exist(read_rh, 'file') == 2
                    stc_r=mne_read_stc_file(read_rh);
                else
                    read_rh=strcat('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/average/',s2,'_',s1,'_cor_en_',frequencies{f},window,condition{s},'-rh.stc');
                    stc_r=mne_read_stc_file(read_rh);
                end
                
                lhrh=stc_l.data(:,1); %first slice only, as this is the average over time
                lhrh(10243:20484,1)=stc_r.data(:,1);
                all_data(:,r)=lhrh; %first left hemisphere data, then right hemisphere data
            end
        end
        
        disp(strcat('Saving corr_matrix_',frequencies{f},window,condition{s},'.mat'));
        save(strcat('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/corr_matrix_',frequencies{f},window,condition{s},'.mat'),'all_data');
        
    end
end

save('/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/subjects.mat', 'subj_list');

%% Visualize correlation matrix in a random source point
r=7665;

ids=find(tril(ones(length(subj_list)),-1));
temp=zeros(length(subj_list));
temp(ids)=all_data(r,:);
temp=temp+temp'+eye(length(subj_list));
imagesc(temp,[-.3 .3])
colorbar

