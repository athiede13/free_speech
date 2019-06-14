% Calculate weighted average of part 1 and 2 correlations matrices of speech condition.

% author: Anja Thiede <anja.thiede@helsinki.fi>

close all
addpath /home/cbru/MNE-2.7.0-3106-Linux-x86_64/share/matlab/ %local path to MNE

load /media/cbru/SMEDY/scripts_speech_rest/stats/isc_models.mat % we now have variables: group_models (1=dys, 2=within both groups, 3=con)
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
corr_matrix_path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/';
freq={'5.000000e-01-4Hz', '4-8Hz','8-12Hz','12-25Hz','25-45Hz', '55-90Hz'};
window={'_286', '_327'};
condition = {'_10', '_11'};
isc_results={
    [corr_matrix_path 'corr_matrix_5.000000e-01-4Hz' window{1} condition{1} '.mat'], [corr_matrix_path 'corr_matrix_5.000000e-01-4Hz' window{2} condition{2} '.mat'];
    [corr_matrix_path 'corr_matrix_4-8Hz' window{1} condition{1} '.mat'], [corr_matrix_path 'corr_matrix_4-8Hz' window{2} condition{2} '.mat'];
    [corr_matrix_path 'corr_matrix_8-12Hz' window{1} condition{1} '.mat'], [corr_matrix_path 'corr_matrix_8-12Hz' window{2} condition{2} '.mat'];
    [corr_matrix_path 'corr_matrix_12-25Hz' window{1} condition{1} '.mat'], [corr_matrix_path 'corr_matrix_12-25Hz' window{2} condition{2} '.mat'];
    [corr_matrix_path 'corr_matrix_25-45Hz' window{1} condition{1} '.mat'], [corr_matrix_path 'corr_matrix_25-45Hz' window{2} condition{2} '.mat'];
    [corr_matrix_path 'corr_matrix_55-90Hz' window{1} condition{1} '.mat'], [corr_matrix_path 'corr_matrix_55-90Hz' window{2} condition{2} '.mat'];
    };

for f=1:length(freq)
    both_windows = [];
    for s=1:length(condition)
        % load ISC matrices
        load([isc_results{f,s}]);
        both_windows(s,:,:) = all_data;
    end
    w = [286/613 327/613];
    weighted_mean = mean(w'.*both_windows);
    all_data = squeeze(weighted_mean);  % name "all_data" just for consistency purposes
    
    % save
    save_window='_613';
    save_condition='_1';
    disp(strcat('Saving corr_matrix_',freq{f},save_window,save_condition,'.mat'));
    save([corr_matrix_path 'corr_matrix_' freq{f} save_window save_condition '.mat'],'all_data');
end

% Visualize correlation matrix in a random source point
r=7665;

% window 1
figure;
ids=find(tril(ones(length(subj_list)),-1));
temp=zeros(length(subj_list));
temp(ids)=both_windows(1,r,:);
temp=temp+temp'+eye(length(subj_list));
imagesc(temp,[-.3 .3])
colorbar

% window 2
figure;
ids=find(tril(ones(length(subj_list)),-1));
temp=zeros(length(subj_list));
temp(ids)=both_windows(2,r,:);
temp=temp+temp'+eye(length(subj_list));
imagesc(temp,[-.3 .3])
colorbar

% weighted mean
figure;
ids=find(tril(ones(length(subj_list)),-1));
temp=zeros(length(subj_list));
temp(ids)=all_data(r,:);
temp=temp+temp'+eye(length(subj_list));
imagesc(temp,[-.3 .3])
colorbar
