clear all
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

mm=[      zeros(Ndys)  zeros(Ndys,Nnondys); % non dyslexics only
    zeros(Nnondys,Ndys) ones(Nnondys);
];
mm(1:(size(mm,1)+1):end)=1;
group_models(:,:,3)=mot_mask.*mm;

% %% regress out IQ
% % we do this only for the brain data
% 
% % phon - IQ
% 
% % yot_m(intersect(blacklist,1:Ndys),:)=[];
% % fam_m(intersect(blacklist,1:Ndys),:)=[];
% 
% [a b scores]=regress(phon,[iq ones(length(phon),1)]);
% scores=scores-min(scores)+min(phon);
% phon_ort_iq=scores;
% 
% mean_phon_ort_iq=zeros(length(phon));
% for s1=1:length(phon)
%     for s2=s1:length(phon)
%         mean_phon_ort_iq(s1,s2)=mean([scores(s1,1) scores(s2,1)]);
%         mean_phon_ort_iq(s2,s1)=mean_phon_ort_iq(s1,s2);
%     end
% end
% 
% 
% % read - IQ
% 
% [a b scores]=regress(read,[iq ones(length(read),1)]);
% scores=scores-min(scores)+min(read);
% read_ort_iq=scores;
% 
% mean_read_ort_iq=zeros(length(read));
% for s1=1:length(read)
%     for s2=s1:length(read)
%         mean_read_ort_iq(s1,s2)=mean([scores(s1,1) scores(s2,1)]);
%         mean_read_ort_iq(s2,s1)=mean_read_ort_iq(s1,s2);
%     end
% end
% 
% 
% % mem - IQ
% 
% [a b scores]=regress(mem,[iq ones(length(mem),1)]);
% scores=scores-min(scores)+min(mem);
% mem_ort_iq=scores;
% 
% mean_mem_ort_iq=zeros(length(mem));
% for s1=1:length(mem)
%     for s2=s1:length(mem)
%         mean_mem_ort_iq(s1,s2)=mean([scores(s1,1) scores(s2,1)]);
%         mean_mem_ort_iq(s2,s1)=mean_mem_ort_iq(s1,s2);
%     end
% end

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
title(['Mean full IQ'])
xlabel('Subjects (1-23=Dyslexics)');
ylabel('Subjects (1-23=Dyslexics)');
set(gcf,'Color','white')
saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/FIQ.png']);


% % mean phon minus IQ
% figure
% isc=mean_phon_ort_iq;
% imagesc(isc)
% colorbar
% hold on
% %plot([0 size(isc,1)]+.5,[cutM cutM]+.5,'k');
% %plot([cutM cutM]+.5,[0 size(isc,1)]+.5,'k');
% colormap(map)
% title(['Mean phonological processing minus IQ'])
% xlabel('Subjects (1-23=Dyslexics)');
% ylabel('Subjects (1-23=Dyslexics)');
% set(gcf,'Color','white')
% saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/phon_minus_IQ.png']);
% 
% figure
% temp=mean_phon(1:cutM,1:cutM);
% ids=find(triu(ones(cutM)));
% plot(temp(ids),mean_phon_ort_iq(ids),'.')
% xlabel('Mean phonological processing')
% ylabel('Mean phonological processing minus IQ')
% set(gcf,'Color','white')
% saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/phon_minus_IQ_scatterplot.png']);
% 
% % mean read minus IQ
% figure
% isc=mean_read_ort_iq;
% imagesc(isc)
% colorbar
% hold on
% %plot([0 size(isc,1)]+.5,[cutM cutM]+.5,'k');
% %plot([cutM cutM]+.5,[0 size(isc,1)]+.5,'k');
% colormap(map)
% title(['Mean technical reading minus IQ'])
% xlabel('Subjects (1-23=Dyslexics)');
% ylabel('Subjects (1-23=Dyslexics)');
% set(gcf,'Color','white')
% saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/read_minus_IQ.png']);
% 
% figure
% temp=mean_read(1:cutM,1:cutM);
% ids=find(triu(ones(cutM)));
% plot(temp(ids),mean_read_ort_iq(ids),'.')
% xlabel('Mean technical reading')
% ylabel('Mean technical reading minus IQ')
% set(gcf,'Color','white')
% saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/read_minus_IQ_scatterplot.png']);
% 
% % mean mem minus IQ
% figure
% isc=mean_mem_ort_iq;
% imagesc(isc)
% colorbar
% hold on
% %plot([0 size(isc,1)]+.5,[cutM cutM]+.5,'k');
% %plot([cutM cutM]+.5,[0 size(isc,1)]+.5,'k');
% colormap(map)
% title(['Mean working memory minus IQ'])
% xlabel('Subjects (1-23=Dyslexics)');
% ylabel('Subjects (1-23=Dyslexics)');
% set(gcf,'Color','white')
% saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/mem_minus_IQ.png']);
% 
% figure
% temp=mean_mem(1:cutM,1:cutM);
% ids=find(triu(ones(cutM)));
% plot(temp(ids),mean_mem_ort_iq(ids),'.')
% xlabel('Mean working memory')
% ylabel('Mean working memory minus IQ')
% set(gcf,'Color','white')
% saveas(gcf,['/media/cbru/SMEDY/results/nepsy_models/mem_minus_IQ_scatterplot.png']);


% save models
save isc_models mean_phon mean_read mean_mem mean_iq group_models    
%save mean_phon_ort_iq mean_read_ort_iq mean_mem_ort_iq






