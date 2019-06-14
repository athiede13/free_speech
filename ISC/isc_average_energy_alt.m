function isc_average_energy_alt(parameters)
%Calculates average correlation for each hemisphere and saves them into stc-files.

%addpath /proj/mne/MNE-2.7.4-3434-Linux-x86_64/share/matlab/
back=parameters.back;
en_av_names=parameters.average_names_ene;
en_names=parameters.cor_en_names;
luku=size(en_names, 1); % amount of pairwise correlations
morphgrade=parameters.morphgrade;
if morphgrade==4
    koko=2562;
end
if morphgrade==5
    koko=10242;
end
if morphgrade==3
    koko=642;
end
if morphgrade==6
    koko=40962;
end

cd([parameters.folders{1}(1:end-7), '/average']);
% old cd /m/nbe/scratch/braindata/thiedea/free_listening/MEG_preproc/average

%z=0;
n=1;
name_en=[en_names(n,:) '-lh.stc'];
file=mne_read_stc_file(name_en);
nr=zeros(koko, size(file.data,2));
x=~isnan(file.data);
data=file.data;
data(isnan(data))=0;
sum_en_lh=data;
nr=nr+x;
n=n+1;
for j=2:luku
    name_en=[en_names(n,:) '-lh.stc'];
    file=mne_read_stc_file(name_en);
    x=~isnan(file.data);
    data=file.data;
    data(isnan(data))=0;
    sum_en_lh=sum_en_lh+data;
    nr=nr+x;
    n=n+1;
end
sum_en_lh=sum_en_lh./nr;
apu_lh=isnan(sum_en_lh);
sum_en_lh(apu_lh)=0;
%         apu2_lh=(abs(sum_en_lh))<0.05;
%         sum_en_lh(apu2_lh)=0;
en.tmin=1;
en.tstep=1;
en.vertices=file.vertices;
savename_en=[en_av_names '-lh.stc'];
en.data=sum_en_lh;
mne_write_stc_file(savename_en,en);
clear file name_en n nr data sum_en_lh
fprintf(1,'Wrote %s\n',savename_en);
n=1;

name_en=[en_names(n,:) '-rh.stc'];
file=mne_read_stc_file(name_en);
nr=zeros(koko, size(file.data,2));
x=~isnan(file.data);
data=file.data;
data(isnan(data))=0;
sum_en_rh=data;
nr=nr+x;
n=n+1;
for j=2:luku
    name_en=[en_names(n,:) '-rh.stc'];
    file=mne_read_stc_file(name_en);
    x=~isnan(file.data);
    data=file.data;
    data(isnan(data))=0;
    sum_en_rh=sum_en_rh+data;
    nr=nr+x;
    n=n+1;
end

sum_en_rh=sum_en_rh./nr;
apu_rh=isnan(sum_en_rh);
sum_en_rh(apu_rh)=0;
%         apu2_rh=(abs(sum_en_rh))<0.05;
%         sum_en_rh(apu2_rh)=0;
en.tmin=1;
en.tstep=1;
en.vertices=file.vertices;
savename_en=[en_av_names '-rh.stc'];
en.data=sum_en_rh;
mne_write_stc_file(savename_en,en);
clear file name_en n nr data sum_en_rh
fprintf(1,'Wrote %s\n',savename_en);


cd(back)
