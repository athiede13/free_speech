% Create models for control, dyslexic, and mixed subject pairs.

% authors: Enrico Glerean, Anja Thiede <anja.thiede@helsinki.fi>

close all

% subject info
% create a matlab sheet with subject numbers
subj_ids = xlsread('/media/cbru/SMEDY/scripts_speech_rest/stats/subjects_to_stats.xlsx');
% now we have variable subj_ids

NS=max(subj_ids(:,1)); % number of subjects
blacklist=unique(subj_ids(find(subj_ids(:,2)==0),1)); % find the subjects to leave out because they don't belong to the MEG dataset

% mask for correlation matrices
mot_mask=ones(NS);
mot_mask(blacklist,:)=[];
mot_mask(:,blacklist)=[];


%% group comparisons
Ndys=length(find(subj_ids(:,3))); %
Ncon=NS - Ndys;
mm = [ones(Ndys)  zeros(Ndys,Ncon);
    zeros(Ncon,Ndys) zeros(Ncon);
    ];
mm(1:(size(mm,1)+1):end)=1;

group_models(:,:,1)=mot_mask.*mm; % dys only

mm = [ones(Ndys)  zeros(Ndys,Ncon);
    zeros(Ncon,Ndys) ones(Ncon);
    ];
mm(1:(size(mm,1)+1):end)=1;

group_models(:,:,2)=mot_mask.*mm; % dys and con separated

mm = [zeros(Ndys)  zeros(Ndys,Ncon);
    zeros(Ncon,Ndys) ones(Ncon);
    ];
mm(1:(size(mm,1)+1):end)=1;
group_models(:,:,3)=mot_mask.*mm; % con only

% save models
save isc_models.mat group_models

% visualize group models
figure()
imagesc(group_models(:,:,1))
title('Dys=1 Con=0 (Dyslexics only)')
colorbar
figure()
imagesc(group_models(:,:,2))
title('Dys=1 Con=1 (Dyslexics and controls separately)')
colorbar
figure()
imagesc(group_models(:,:,3))
title('Dys=0 Con=1 (Controls only)')
colorbar