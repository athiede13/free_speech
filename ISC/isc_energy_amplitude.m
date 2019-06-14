function isc_energy_amplitude(file, modtimes, parameters, j)
% Goes through file step by step and applies filtering, Hilbert transformation, projection to source space, taking absolute value, and downsampling.

energy_names=parameters.energy_names;
folders=parameters.folders;
bandpass=parameters.bandpassfrequencies;
order=parameters.order;
save_names=parameters.save_names;
ord_number=j;
lahtoaika=modtimes(1);
loppuaika=modtimes(2);
sf=parameters.sf;
lowpass=parameters.lowpassfrequency;
ds_freq=parameters.downsamplefrequency;
ds=sf/ds_freq;
eog_rej=parameters.eog_rejection;
mag_rej=parameters.mag_rejection;
grad_rej=parameters.grad_rejection;
eog_thres=parameters.eog_threshold;
mag_thres=parameters.mag_threshold;
grad_thres=parameters.grad_threshold;
eog_ch=parameters.eog_ch;
dSPM=parameters.dSPM;

[b1_kaista,a1_kaista]=butter(order,[(((bandpass(1)))/(sf/2)) ((bandpass(2))/(sf/2))]); %creating the filters
[b1_ali,a1_ali]=butter(order,((lowpass)/(sf/2)),'low');

back=cd(char(folders(ord_number)));
if (ord_number~=1)
    clear inv
    clear regs
    clear betas
    clear mods
end
load(save_names(ord_number,:))
cd(back);
m=0;
cd(char(folders{j}));
inv_struct=load(save_names(j,:)); %inverse operator
inv=inv_struct.inv;
alku=lahtoaika;
channels=inv.chsel;
if eog_rej==1
    channels=[inv.chsel eog_ch];
end
helping_variable=or(grad_rej==1, mag_rej==1);


while (alku+1)<(loppuaika)
    if m==0
        clear zf zi zf_filt zi_filt
        part=fiff_read_raw_segment_times(file, alku, alku+1,channels); %changed
        if or(eog_rej==1, helping_variable==1)
            suurin_eog=0;
            difference_mag=0;
            difference_grad=0;
            for i=inv.chsel
                name=char(file.info.ch_names(1,i));
                if size(name,2)>7
                    apu=find(isspace(name));
                    name=sprintf('%s%s', name(1:(apu-1)),name((apu+1):end));
                end
                if (name(1,7)==num2str(1))
                    if mag_rej==1
                        if (abs(max(part(i,:)-min(part(i,:))))>difference_mag)
                            difference_mag=abs(max(part(i,:)-min(part(i,:))));
                        end
                    end
                else
                    if grad_rej==1
                        if (abs(max(part(i,:)-min(part(i,:))))>difference_grad)
                            difference_grad=abs(max(part(i,:)-min(part(i,:))));
                        end
                    end
                end
            end
            if eog_rej==1
                for i=1:size(parameters.eog_ch)
                    difference_eog=abs(max(part(eog_ch(i),:)-min(part(eog_ch(i),:))));
                    if difference_eog>suurin_eog
                        suurin_eog=difference_eog;
                    end
                end
            end
            if ((difference_mag>mag_thres)||(difference_grad>grad_thres)||(difference_eog>eog_thres))
                part=NaN(size(inv.chsel,2),(ch_number));
            end
        end
        [x1, zf]=filter(b1_kaista,a1_kaista, part,[],2); % bandpass filtering
        apu=hilbert(x1); %hilbert transformation
        clear part
        ensol=inv.operator*apu; %source-space projection
        clear apu x1
        ensol=abs(ensol);    %absolute value (envelope)
        i=1:3:size(ensol,1);
        x=1:size(ensol,2);
        ensol2=sqrt(ensol(i,x).^2+ensol(i+1,x).^2+ensol(i+2,x).^2);
        [ensol2_filt, zf_filt]=filter(b1_ali,a1_ali,ensol2,[],2); %low-pass filtering
        
        clear ensol
        ensol=ensol2_filt(:,1:(ds):end); %downsampling
        alku=alku+1;
        m=1;
        helahoito=ensol;
    else
        part=fiff_read_raw_segment_times(file, alku, alku+1,channels);
        if or(eog_rej==1, helping_variable==1)
            suurin_eog=0;
            difference_mag=0;
            difference_grad=0;
            for i=inv.chsel
                name=char(file.info.ch_names(1,i));
                if size(name,2)>7
                    apu=find(isspace(name));
                    name=sprintf('%s%s', name(1:(apu-1)),name((apu+1):end));
                end
                if (name(1,7)==num2str(1))
                    if mag_rej==1
                        if (abs(max(part(i,:)-min(part(i,:))))>difference_mag)
                            difference_mag=abs(max(part(i,:)-min(part(i,:))));
                        end
                    end
                else
                    if grad_rej==1
                        if (abs(max(part(i,:)-min(part(i,:))))>difference_grad)
                            difference_grad=abs(max(part(i,:)-min(part(i,:))));
                        end
                    end
                end
            end
            if eog_rej==1
                for i=1:size(parameters.eog_ch)
                    difference_eog=abs(max(part(eog_ch(i),:)-min(part(eog_ch(i),:))));
                    if difference_eog>suurin_eog
                        suurin_eog=difference_eog;
                    end
                end
            end
            if ((difference_mag>mag_thres)||(difference_grad>grad_thres)||(difference_eog>eog_thres))
                part=NaN(size(inv.chsel,2),(ch_number));
            end
        end
        zi=zf;
        zi_filt=zf_filt;
        [x1, zf]=filter(b1_kaista, a1_kaista, part, zi,2); %bandpass filtering
        apu=hilbert(x1); %hilbert transformation
        clear part
        ensol=inv.operator*apu; %source-space projection
        clear apu
        ensol=abs(ensol); %absolute value (envelope)
        i=1:3:size(ensol,1);
        x=1:size(ensol,2);
        ensol2=sqrt(ensol(i,x).^2+ensol(i+1,x).^2+ensol(i+2,x).^2);
        
        [ensol2_filt,zf_filt]=filter(b1_ali,a1_ali,ensol2,zi_filt,2); %low-pass filtering
        clear ensol
        ensol=ensol2_filt(:,1:(ds):end); %downsampling
        alku=alku+1;
        helahoito=[helahoito ensol];
    end
end
if dSPM==1
    fprintf(1,'(dSPM)...\n');
    helahoito = inv.noisenorm*helahoito;
end
mne_write_inverse_sol_stc(energy_names(j,:),inv,helahoito,1,1)
