% Permute subject labels of ISC data.

% This script needs the isc_models created with make_models.m

% author: Anja Thiede <anja.thiede@helsinki.fi>

clear all
close all

addpath /home/cbru/MNE-2.7.0-3106-Linux-x86_64/share/matlab/ %local path to MNE
addpath /media/cbru/SMEDY/scripts_speech_rest/stats/ % bramila permutation t test located here
load /media/cbru/SMEDY/scripts_speech_rest/stats/mantel/isc_models.mat % we now have variables: group_models (1=dys, 2=within both groups, 3=con) mean_phon mean_mem mean_read mean_iq

% TO FILL

NPERMS=5000;
cons={'_1'}; % '_1' listening to speech, '_2' resting
freq={'5.000000e-01-4Hz', '4-8Hz','8-12Hz','12-25Hz','25-45Hz', '55-90Hz'}; %frequency bands
results_path = '/media/cbru/SMEDY/DATA/group_fake_iscs/';
corr_matrix_path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/';

% load data
% for the whole time frame
if strcmp(cons{1},'_1')
    window='_613';
    condition = '_1';
    disp('You selected listening to speech as the brain data')
elseif strcmp(cons{1},'_2')
    window = '_579';
    condition = '_2';
    disp('You selected resting as the brain data')
else
    error('Check condition!')
end

isc_results={
    [corr_matrix_path 'corr_matrix_5.000000e-01-4Hz' window condition '.mat'];
    [corr_matrix_path 'corr_matrix_4-8Hz' window condition '.mat'];
    [corr_matrix_path 'corr_matrix_8-12Hz' window condition '.mat'];
    [corr_matrix_path 'corr_matrix_12-25Hz' window condition '.mat'];
    [corr_matrix_path 'corr_matrix_25-45Hz' window condition '.mat'];
    [corr_matrix_path 'corr_matrix_55-90Hz' window condition '.mat'];
    };

%% pre-compute NPERMS permutations of indices
NS=length(group_models(:,1,1));
iscMASK=triu(ones(NS),1);
iscids=find(iscMASK); % our ISC matrices are stored as top triangles with NS subjects

% IDs for dys and con
temp=iscMASK.*group_models(:,:,1); % model for dys only
vec=temp(iscids);
idDys=find(vec==1);

temp=iscMASK.*group_models(:,:,3); % model for con only
vec=temp(iscids);
idCon=find(vec==1);

% 23 dyslexics and 21 controls
dys_ids=1:23;
con_ids=24:44;

throwthedice=1;
counter=1;
while(throwthedice)
    temp=randperm(NS); 
    if(sum(ismember(temp(dys_ids),dys_ids))>17) % check here that at least 25% of controls went to dyslexics and if not, then throw the dice again, do this by counting the number of '1s' 
        disp('throw the dice again')
    else
        fake_indices(:,counter)=temp; % store results in fake_indices
        counter=counter+1;
    end
    if(counter>NPERMS)
        throwthedice=0;
    end
end

%% create fake isc data

% prepare iscMASK
iscMASK(iscMASK~=0) = 1:(NS-1)*(NS)/2;
iscMASK = iscMASK + triu(iscMASK,1).';

for f=1:length(freq) % MEG frequency band
    % load real isc data
    s=1; % test only for one condition at a time
    load([isc_results{f,s}]); % loads variable 'all_data' [20484x946 double]
    % replace all NaNs with zeros
    all_data(find(isnan(all_data)))=0;
    disp(f)
    iscs_vec=all_data'; % after loading
    NNODES = size(iscs_vec, 2);
    
    fake_t_vals = zeros(NNODES,NPERMS);
    for n=1:NNODES
        % rebuild the isc_matrix [44x44]
        iscs_vec_node=iscs_vec(:,n)';
        isc_matrix=zeros(NS);

        for row=1:NS
            for column=1:NS
                id=iscMASK(column,row);
                if id > 0
                    isc_matrix(row,column)=iscs_vec_node(id);
                end
            end
        end  
        isc_matrix=isc_matrix+eye(NS);
    
        for i=1:NPERMS
            fake_isc_data = isc_matrix(fake_indices(:,i),fake_indices(:,i));
            top_triangle=triu(fake_isc_data)-eye(NS);
            iscs_dys = top_triangle(dys_ids,dys_ids);
            iscs_dys_vec = iscs_dys(triu(true(size(iscs_dys)),1));
            iscs_con = top_triangle(con_ids,con_ids);
            iscs_con_vec = iscs_con(triu(true(size(iscs_con)),1));
            [h,p,ci,stats] = ttest2(iscs_dys_vec,iscs_con_vec);
            fake_t_vals(n, i) = stats.tstat;
        end
    end
    save([results_path, 'fake_t_vals_' freq{f} window cons{s} '.mat'],'fake_t_vals')
    disp('fake_t_vals saved')
%     - for each node
%            - for each permutation i
%                 get shuffled indexes from the matrix fake_indexes 
%                 shuffle the data 
%                 fake_isc_data = isc_data(fake_indexes(:,i),fake_indexes(:,i))
%                 now compute the 2 sample ttest and store this fake t value somewhere
% 
%         you end up with a matrix num_of_nodes X num_of_permutations and then you can feed this 
%             into the cluster correction function from MNE.
    
    

    
% %     % computing actual mantel test
% %     r_mantel = corr(iscs_vec,model_vec,'type','spearman');
% %     save([results_path, mode, '_r_mantel_', freq{f} window cons{s}, '.mat'],'r_mantel')

%     
%     % option 4: cluster correction
%     %   for each permutation:
%     %   1. Compute the test statistic for each voxel individually.
%     %   2. Threshold the test statistic values.
%     %   3. Cluster voxels that exceed this threshold (with the same sign) based on adjacency.
%     %   4. Retain the size of the largest cluster (measured, e.g., by a simple voxel count, or by the sum of voxel t-values within the cluster) to build the null distribution.
%     
%     % get the uncorrected r-threshold
%     rthreshold_uncorrected{f,s}=min(abs(r_mantel(find(pval_local<0.05))))
%     if ~isempty(rthreshold_uncorrected{f,s})
%         save([results_path, mode, '_rthreshold_uncorrected_' freq{f} window cons{s} '.mat'],'rthreshold_uncorrected')
%         % 1. Compute the test statistic for each voxel individually.
%         % for each node, compute its own p-value from the NPERMS fake models
%         surrogate_values_thres=zeros(NPERMS,1);
%         
%         surrogate_values=corr(iscs_vec,fake_model_vec,'type','spearman');
%         save([results_path, mode, '_surrogate_values_' freq{f} window cons{s} '.mat'],'surrogate_values')
%     end
%     
%     % go through matrix and find clusters for each permutation done
%     % in MNE python
    
end

%% compute real independent samples T-tests and save uncorrected thresholds

for f=1:length(freq) % MEG frequency band
    % load real isc data
    s=1; % test only for one condition at a time
    load([isc_results{f,s}]); % loads variable 'all_data' [20484x946 double]
    % replace all NaNs with zeros
    all_data(find(isnan(all_data)))=0;
    disp(f)
    iscs_vec=all_data'; % after loading
    NNODES = size(iscs_vec, 2);
    real_t_vals = zeros(NNODES,1);
    real_p_vals = zeros(NNODES,1);
    
    for n=1:NNODES
        % compute actual T-test
        [h,p,ci,stats] = ttest2(iscs_vec(idDys,n),iscs_vec(idCon,n));
        real_t_vals(n) = stats.tstat;
        real_p_vals(n) = p;
    end

    % save real T-vals
    save([results_path, 'real_t_vals_', freq{f} window cons{s}, '.mat'],'real_t_vals')
    
    % get the uncorrected T-threshold
    tthreshold_uncorrected=min(abs(real_t_vals(find(real_p_vals<0.05/6)))) % Bonferroni correction, 6 frequency bands
    if ~isempty(tthreshold_uncorrected)
        save([results_path, 'tthreshold_uncorrected_' freq{f} window cons{s} '.mat'],'tthreshold_uncorrected')
    end
end

disp('computed real independent T-test and uncorrected threshold')
