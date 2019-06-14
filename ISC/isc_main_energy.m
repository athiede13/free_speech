function [yesno, parameters]=isc_main_energy(parameters)
% Calls the correct following functions depending on user input.

number=parameters.number;
folders=parameters.folders;
names=parameters.filenames;
fileids=parameters.fileids;

back=cd(char(folders{1}));
sf=parameters.sf;
cd(back)
parameters.back=back;
new_inverse=parameters.should_the_inverse_operators_be_updated;
new_times=parameters.should_the_length_of_the_files_be_reestimated;

%inverse operators to matlab format
if new_inverse==1
    save_names=isc_inverse(parameters,names);
    parameters.save_names=save_names;
    save('save_names.mat', 'save_names');
else
    load('save_names.mat');
    parameters.save_names=save_names;
end

%This finds when the stimulus is on in each file
name=sprintf('modtimes_%d.mat',fileids);
if new_times==1
    all_modtimes=zeros(2,number);
    for j=1:number
        file = fiff_setup_read_raw([char(folders{j}), '/', names{j,:}]);
        start_time = parameters.length_stimulus_start(j);
        %Finds out starts and finishes of each modulating signal
        mod_times=isc_start_finish(file,start_time,parameters);
        %collects times when modulating signals are on to a matrix (starts/finishes)x(subjects)
        all_modtimes(:,j)=mod_times;
    end
    
    save(name,'all_modtimes');
    
else
    load(name)
end

cd(char(folders{1}));
load(save_names(1,:))
cd(back)
clear inv
first_sec=zeros(number,1);

for j=1:number
    cd(char(folders(j)));
    file=fiff_setup_read_raw(names{j,:});
    first_sec(j,:)=ceil(double(file.first_samp)/sf);
    cd(back);
    isc_energy_amplitude(file, all_modtimes(:,j), parameters, j);
    
end
cd(back)

yesno=0;






