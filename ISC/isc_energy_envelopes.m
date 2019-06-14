function isc_energy_envelopes(files, frequencies,parameters)
% Creates filenames and calls following function(s) depending on user input.

parameters.fileids=files;
parameters.bandpassfrequencies=[frequencies(1) frequencies(2)];
spacing=parameters.spacing;
onlyenvelopes=parameters.envelopes_only;
onlycorrelations=parameters.correlations_only;
onlyaverages=parameters.averages_only;
parameters.number=size(parameters.subjects,1);   %the number of subjects
parameters.back=cd;     %home folder
parameters.en_bandwidth=sprintf('%d-%dHz',parameters.bandpassfrequencies(1), parameters.bandpassfrequencies(2));

%CREATING FILE NAMES:
n=0;
for i=1:parameters.number
    subject=parameters.subjects(i,:);
    temp = dir([parameters.folders{i,:}, '/', parameters.pattern{files, 1}]); % added this because the filenames can be different depending on the subject
    parameters.endings(files, 1) = {temp.name}; % only create this variable here
    parameters.filenames(i,:)=parameters.endings(files,1);   %the name of raw data files
    parameters.inv_names(i,:)=sprintf('%s-%s-meg-inv.fif',char(parameters.invname{files, 1}), spacing);     %the name of the inverse operator file
    parameters.inv_s_names(i,:)=sprintf('%s_%s_%s', subject, char(parameters.invname{files, 1}), parameters.inv_op);     %the name which is used to store the inv operator in matlab-format %CHANGED
    parameters.energy_names(i,:)=sprintf('%s_%s_%s_%d', subject, 'energy', parameters.en_bandwidth, files); %the name used to store energy envelopes
    parameters.energy_mne_names(i,:)=sprintf('%s_%s_%s_%d_MNE', subject, 'energy', parameters.en_bandwidth, files); %the name of morphed energy envelope files; needed to carry out correlation calculation
    
    for j=(1+i):(parameters.number)
        n=n+1;
        mate=parameters.subjects(j,(1:end));
        parameters.cor_en_names(n,:)=sprintf('%s_%s_cor_en_%s_%d_%d', subject, mate, parameters.en_bandwidth, parameters.window, files); %name for files encompassing the correlation coefficients
    end
end
parameters.average_names_ene=sprintf('average_ene_%s_%d_%d', parameters.en_bandwidth, parameters.window, files); %names for group average files

%the program itself:
if onlyenvelopes==1
    [yesno, parameters]=isc_main_energy(parameters);
    return
end
if onlycorrelations==1
    l=isc_correlation_energy(parameters); %calculating the correlations
    isc_average_energy_alt(parameters); %calculating the group averages
    return
end
if onlyaverages==1
    isc_average_energy_alt(parameters)
    return
end
[yesno, parameters]=isc_main_energy(parameters); %calls the functions for finding the start and the end of stimuli and for calculating the length of time when stimulus is on (if needed); calls for the function estimating the energy envelopes and writing stc files
text=sprintf('Are you done with command line MNE-processing (morphing)? (y/n): '); %you can only proceed if you are
yes_no=input(text,'s');
if (yes_no=='n')
    text=sprintf('Please finish command line MNE-processing before continuing and then continue (c): ');
    cont=input(text, 's');
    if (cont=='c')
        l=isc_correlation_energy(parameters); %calculating the correlations
        isc_average_energy_alt(parameters); %calculating the group averages
    end
else
    l=isc_correlation_energy(parameters); %calculating the correlations
    isc_average_energy_alt(parameters); %calculating the group averages
end
end
