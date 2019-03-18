% this script needs the isc_models created with make_models_free_speech.m

clear all
close all

addpath /home/cbru/MNE-2.7.0-3106-Linux-x86_64/share/matlab/ %local path to MNE
addpath /media/cbru/SMEDY/scripts_speech_rest/stats/ % bramila permutation t test located here
load /media/cbru/SMEDY/scripts_speech_rest/stats/mantel/isc_models.mat % we now have variables: group_models (1=dys, 2=within both groups, 3=con) mean_phon mean_mem mean_read mean_iq
load /media/cbru/SMEDY/scripts_speech_rest/stats/mantel/connectivity.mat % connectivity matrix from MNE Python

% TO FILL

NPERMS=5000;
mode='mem'; % 'iq' or 'read' or 'mem' or 'phon'
cons={'_1'}; % '_1' listening to speech, '_2' resting
freq={'5.000000e-01-4Hz', '4-8Hz','8-12Hz','12-25Hz','25-45Hz', '55-90Hz'}; %frequency bands 
regress_IQ_out = 1; % 0 = no, 1 = yes; regresses IQ out from brain data
if regress_IQ_out==1
    results_path = '/media/cbru/SMEDY/results/mantel_correlations/2019_03_IQ_regressed_out/';
else
    results_path = '/media/cbru/SMEDY/results/mantel_correlations/2019_03_simple_model/';
end

% isc results for each condition and frequency band, 1=speech, 2=rest
% 1st row: 4-8Hz, 2nd row: 8-12Hz etc.

disp('Calculating mantel test between brain data and behavioural model')
corr_matrix_path = '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/';

% if(0) % 1 to load 20s time wind, 0 to load whole
%     window='_20';
%     isc_results={
%         '/m/nbe/scratch/braindata/thiedea/free_listening/MEG_preproc/average_matlab/correlation_matrix_4-8Hz_20_1.mat','/m/nbe/scratch/braindata/thiedea/free_listening/MEG_preproc/average_matlab/correlation_matrix_4-8Hz_20_4.mat';
%         '/m/nbe/scratch/braindata/thiedea/free_listening/MEG_preproc/average_matlab/correlation_matrix_8-12Hz_20_1.mat','/m/nbe/scratch/braindata/thiedea/free_listening/MEG_preproc/average_matlab/correlation_matrix_8-12Hz_20_4.mat',
%         };
% else

% % for the whole time frame
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
    %'/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/corr_matrix_8-12Hz_287_1.mat', '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/corr_matrix_8-12Hz_287_2.mat';
    %'/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/corr_matrix_12-25Hz_287_1.mat', '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/corr_matrix_12-25Hz_287_2.mat';
    %'/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/corr_matrix_25-45Hz_287_1.mat', '/media/cbru/SMEDY/DATA/MEG_speech_rest_prepro/corr_matrices/corr_matrix_25-45Hz_287_2.mat';
    };

%% create models
global_mask=1;
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

% behavioural data
rng(0) % control the random generator (rand) so that the randomness is always the same (in case sth goes wrong)

% which model to use
toptri=find(triu(ones(NS),1));    
if strcmp(mode, 'iq')
    disp('You selected IQ as the model')
    mean_iq = mean_iq - diag(diag(mean_iq)) + diag(diag(eye(NS,NS))); % square matrix with ones in diagonal
    model = mean_iq;
elseif strcmp(mode, 'phon')
    disp('You selected phonological processing as the model')
    mean_phon = mean_phon - diag(diag(mean_phon)) + diag(diag(eye(NS,NS))); % square matrix with ones in diagonal
    model = mean_phon;
elseif strcmp(mode, 'mem')
    disp('You selected working memory as the model')
    mean_mem = mean_mem - diag(diag(mean_mem)) + diag(diag(eye(NS,NS))); % square matrix with ones in diagonal
    model = mean_mem;
elseif strcmp(mode, 'read')
    disp('You selected technical reading as the model')
    mean_read = mean_read - diag(diag(mean_read)) + diag(diag(eye(NS,NS))); % square matrix with ones in diagonal
    model = mean_read;
else
    error('Check mode!')
end
    
model_vec = model(toptri);

% load IQ
if regress_IQ_out==1
    mean_iq = mean_iq - diag(diag(mean_iq)) + diag(diag(eye(NS,NS))); % square matrix with ones in diagonal
    mean_iq_vec = mean_iq(toptri);
end

% pre-compute NPERMS fake models
fake_model_vec=zeros(946,NPERMS); % 946 comes from number of subject pairs
throwthedice=1;
counter=1;
while(throwthedice)
   temp=randperm(NS);
   fake_model=model(temp,temp);
   r_temp=corr(fake_model(toptri),model(toptri),'type','spearman');
   if(r_temp > 0.95)
       disp('throw the dice again')
   else
        fake_model_vec(:,counter)=fake_model(toptri);
        counter=counter+1;
   end
   if(counter>NPERMS) throwthedice=0; end
end
      
% setting up output variables and stats parameters
contrast_lh.tmin=1;
contrast_lh.tstep=0.1;
contrast_lh.vertices=zeros(10242,1);
for i=1:10242;
    contrast_lh.vertices(i)=i-1;
end
contrast_rh=contrast_lh;

dys_lh=contrast_lh;
dys_rh=contrast_lh;

con_lh=contrast_lh;
con_rh=contrast_rh;

mean_behav_lh = contrast_lh;
mean_behav_rh = contrast_rh;

%% mantel tests

out=zeros(size(temp));
pval=zeros(size(temp));

for f=1:length(freq); % MEG frequency band 
    %for s=1:length(cons) % test only for one condition at a time
    s=1;
    load([isc_results{f,s}]); % loads variable 'all_data' [20484x561 double]
    % replace all NaNs with zeros
    all_data(find(isnan(all_data)))=0;
    disp(f)
    %disp(s)
    iscs_vec=all_data';%after loading
    if regress_IQ_out==1
        % do regression here: ISCs - IQ
        for n=1:length(iscs_vec)
            [a(:,:,n), b(:,:,n), iscs_ort_iq(:,n)]=regress(iscs_vec(:,n),[mean_iq_vec ones(size(iscs_vec,1),1)]);
        end
        iscs_ort_iq=iscs_ort_iq-min(iscs_ort_iq)+min(iscs_vec); %scaling???
        iscs_vec = iscs_ort_iq;
    end
    NNODES = size(iscs_vec, 2);
    
    % computing actual mantel test
    r_mantel = corr(iscs_vec,model_vec,'type','spearman');
    save([results_path, mode, '_r_mantel_', freq{f} window cons{s}, '.mat'],'r_mantel') 

    % option 1: for each random node, estimate one fake model
    random_nodes = randperm(NNODES, NPERMS); % select random nodes
    surrogate_values=zeros(NPERMS,1);
    for i=1:NPERMS     
        surrogate_values(i)=corr(iscs_vec(:,random_nodes(i)),fake_model_vec(:,i),'type','spearman');      
    end

    [fi xi]=ksdensity(surrogate_values,'function','cdf','npoints',200);
    pval_left=interp1([-1 xi 1],[0 fi 1],r_mantel);    % trick to avoid NaNs
    pval_global=1-pval_left;
    qval_global=mafdr(pval_global,'BHFDR','true');
    figure
    semilogy(r_mantel,pval_global,'b.')
    hold on
    semilogy(r_mantel,qval_global,'bo')
    
    % option 2: for each node, compute its own p-value from the NPERMS fake models

    surrogate_values=corr(iscs_vec,fake_model_vec,'type','spearman');
    for i = 1:NNODES
        if(mod(i,1000)==1) disp(num2str(i)); end
        [fi xi]=ksdensity(surrogate_values(i,:),'function','cdf','npoints',200);
        pval_left=interp1([-1 xi 1],[0 fi 1],r_mantel(i));    % trick to avoid NaNs
        pval_local(i)=1-pval_left;
    end

    % option 2 with for if there's not enough memory
    %for i = 1:NNODES
    %    if(mod(i,1000)==1) disp(num2str(i)); end
    %    surrogate_values=corr(iscs_vec(:,i),fake_model_vec,'type','spearman');
    %    [fi xi]=ksdensity(surrogate_values,'function','cdf','npoints',200);
    %    pval_left=interp1([-1 xi 1],[0 fi 1],r_mantel(i));    % trick to avoid NaNs
    %    pval_local(i)=1-pval_left;
    %end

    qval_local=mafdr(pval_local,'BHFDR','true');
    hold on
    semilogy(r_mantel,pval_local,'r.')
    semilogy(r_mantel,qval_local,'ro')
    
    % option 3: computing the max statistic
    surrogate_values=corr(iscs_vec,fake_model_vec,'type','spearman');
    max_surrogate=max(surrogate_values');
    [fi xi]=ksdensity(max_surrogate,'function','cdf','npoints',200);
    pval_left=interp1([-1 xi 1],[0 fi 1],r_mantel);    % trick to avoid NaNs
    pval_max_stats=1-pval_left;

    hold on
    semilogy(r_mantel,pval_max_stats,'g.')

    % plot the 0.05 line

    plot([min(r_mantel) max(r_mantel)],[0.05 0.05],'k--')
    xlabel('Mantel correlations (Spearman)')
    ylabel('P-values and Q-values')

    % save figure
    set(gcf,'Color','white')
    saveas(gcf,[results_path, mode, '_pq_vals_' freq{f} window cons{s}, '.png']);

    % option 4: cluster correction
%   for each permutation:
%   1. Compute the test statistic for each voxel individually.
%   2. Threshold the test statistic values.
%   3. Cluster voxels that exceed this threshold (with the same sign) based on adjacency.
%   4. Retain the size of the largest cluster (measured, e.g., by a simple voxel count, or by the sum of voxel t-values within the cluster) to build the null distribution.
    
    % get the uncorrected r-threshold
    rthreshold_uncorrected{f,s}=min(abs(r_mantel(find(pval_local<(0.05/3)))))
    if ~isempty(rthreshold_uncorrected{f,s})
        save([results_path, mode, '_rthreshold_uncorrected_' freq{f} window cons{s} '.mat'],'rthreshold_uncorrected')            
        % 1. Compute the test statistic for each voxel individually.
        % for each node, compute its own p-value from the NPERMS fake models
        surrogate_values=zeros(NPERMS,1);
        surrogate_values_thres=zeros(NPERMS,1);

        surrogate_values=corr(iscs_vec,fake_model_vec,'type','spearman');
        save([results_path, mode, '_surrogate_values_' freq{f} window cons{s} '.mat'],'surrogate_values')            
    end
    
%     % 2. Threshold the test statistic values.
%     surrogate_values_thres = surrogate_values;
%     surrogate_values_thres(abs(surrogate_values) < rthreshold_uncorrected{f,s}) = 0;

    % go through matrix and find clusters for each permutation done
    % in MNE python
        
end
