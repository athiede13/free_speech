% Create models for control, dyslexic, and mixed subject pairs. Plots the
% behavioural joint scores and saves the plots.

% authors: Enrico Glerean, Anja Thiede <anja.thiede@helsinki.fi>

close all
addpath('/media/cbru/SMEDY/scripts_speech_rest/matlab_toolboxes/cbrewer/cbrewer/')

% subject info
subj_ids = xlsread('/media/cbru/SMEDY/scripts_speech_rest/stats/subjects_to_stats.xlsx');

NS=max(subj_ids(:,1)); % number of subjects
blacklist=unique(subj_ids(find(subj_ids(:,2)==0),1)); % find the subjects to leave out because of motion

% mask for correlation matrices
mot_mask=ones(NS);
mot_mask(blacklist,:)=NaN;
mot_mask(:,blacklist)=NaN;

% phonological processing
scores=load('/media/cbru/SMEDY/DATA/nepsy/phon_proc_dataonly.csv');
Nsub=size(scores,1);
mean_phon=zeros(Nsub);
for s1=1:Nsub
    for s2=s1:Nsub
        mean_phon(s1,s2)=mean([scores(s1,1) scores(s2,1)]);
        mean_phon(s2,s1)=mean_phon(s1,s2);
    end
end
mean_phon=mean_phon.*mot_mask;
phon=scores;

% technical reading
scores=load('/media/cbru/SMEDY/DATA/nepsy/tech_read_dataonly.csv');
mean_read=zeros(Nsub);
for s1=1:Nsub
    for s2=s1:Nsub
        mean_read(s1,s2)=mean([scores(s1,1) scores(s2,1)]);
        mean_read(s2,s1)=mean_read(s1,s2);
    end
end
mean_read=mean_read.*mot_mask;
read=scores;

% working memory
scores=load('/media/cbru/SMEDY/DATA/nepsy/work_mem_dataonly.csv');
mean_mem=zeros(Nsub);
for s1=1:Nsub
    for s2=s1:Nsub
        mean_mem(s1,s2)=mean([scores(s1,1) scores(s2,1)]);
        mean_mem(s2,s1)=mean_mem(s1,s2);
    end
end
mean_mem=mean_mem.*mot_mask;
mem=scores;

% FIQ
scores=load('/media/cbru/SMEDY/DATA/nepsy/FIQ_dataonly.csv');
mean_iq=zeros(Nsub);
for s1=1:Nsub
    for s2=s1:Nsub
        mean_iq(s1,s2)=mean([scores(s1,1) scores(s2,1)]);
        mean_iq(s2,s1)=mean_iq(s1,s2);
    end
end
mean_iq=mean_iq.*mot_mask;
iq=scores;

%% group comparisons
Ndys=length(find(subj_ids(:,3)));
Nnondys=Nsub - Ndys;
mm=[   ones(Ndys)  zeros(Ndys,Nnondys);
    zeros(Nnondys,Ndys) zeros(Nnondys);
    ];
mm(1:(size(mm,1)+1):end)=1;

group_models(:,:,1)=mot_mask.*mm; % dyslexics only

mm=[     ones(Ndys)  zeros(Ndys,Nnondys);
    zeros(Nnondys,Ndys) ones(Nnondys);
    ];
mm(1:(size(mm,1)+1):end)=1;

group_models(:,:,2)=mot_mask.*mm; % dyslexics and non dyslexics separated

mm=[      zeros(Ndys)  zeros(Ndys,Nnondys);
    zeros(Nnondys,Ndys) ones(Nnondys);
    ];
mm(1:(size(mm,1)+1):end)=1;
group_models(:,:,3)=mot_mask.*mm; % non dyslexics only

%% Plot for models
dys_nondys=subj_ids(:,3);
dys_nondys(blacklist)=[];
cutM=sum(dys_nondys);
map=cbrewer('seq','Reds',9);
map=[1 1 1;map];

% mean phonological processing
figure
isc=mean_phon;
isc(blacklist,:)=[];
isc(:,blacklist)=[];
imagesc(isc)
colorbar
hold on
plot([0 size(isc,1)]+.5,[cutM cutM]+.5,'k');
plot([cutM cutM]+.5,[0 size(isc,1)]+.5,'k');
colormap(map)
h = colorbar;
ylabel(h, 'z-score', 'fontsize', 11)
title(['Mean phonological processing'])
xlabel('Subjects (1-23=Dyslexics)');
ylabel('Subjects (1-23=Dyslexics)');
set(gcf,'Color','white')
saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/phon_proc.png']);

% mean technical reading
figure
isc=mean_read;
isc(blacklist,:)=[];
isc(:,blacklist)=[];
imagesc(isc)
colorbar
hold on
plot([0 size(isc,1)]+.5,[cutM cutM]+.5,'k');
plot([cutM cutM]+.5,[0 size(isc,1)]+.5,'k');
colormap(map)
h = colorbar;
ylabel(h, 'z-score', 'fontsize', 11)
title(['Mean technical reading'])
xlabel('Subjects (1-23=Dyslexics)');
ylabel('Subjects (1-23=Dyslexics)');
set(gcf,'Color','white')
saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/tech_read.png']);

% mean working memory
figure
isc=mean_mem;
isc(blacklist,:)=[];
isc(:,blacklist)=[];
imagesc(isc)
colorbar
hold on
plot([0 size(isc,1)]+.5,[cutM cutM]+.5,'k');
plot([cutM cutM]+.5,[0 size(isc,1)]+.5,'k');
colormap(map)
h = colorbar;
ylabel(h, 'standardized score (WMS-III)', 'fontsize', 11)
title(['Mean working memory'])
xlabel('Subjects (1-23=Dyslexics)');
ylabel('Subjects (1-23=Dyslexics)');
set(gcf,'Color','white')
saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/work_mem.png']);

% mean IQ
figure
isc=mean_iq;
isc(blacklist,:)=[];
isc(:,blacklist)=[];
imagesc(isc)
colorbar
hold on
plot([0 size(isc,1)]+.5,[cutM cutM]+.5,'k');
plot([cutM cutM]+.5,[0 size(isc,1)]+.5,'k');
colormap(map)
h = colorbar;
ylabel(h, 'standardized score (WAIS-III)', 'fontsize', 11)
title(['Mean full IQ'])
xlabel('Subjects (1-23=Dyslexics)');
ylabel('Subjects (1-23=Dyslexics)');
set(gcf,'Color','white')
saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/FIQ.png']);

% save models
save isc_models mean_phon mean_read mean_mem mean_iq group_models
