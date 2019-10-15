% Read .wav sound file and filter

% author: Anja Thiede <anja.thiede@helsinki.fi>

speech_file = 'D:\\stimuli/presentation_final/speech/stimuli/speech_part1.wav';
times = [250 270];
alku = times(1);
loppuaika = times(2);
bandpass = [12 25]; % beta
lowpass = 0.3; % Hz
ds = 10; % Hz
order = 3; % filter order

[y,Fs] = audioread(speech_file);
% samples = [times(1)*Fs,times(2)*Fs];
% clear y Fs
% [y,Fs] = audioread(speech_file,samples);

size(y);
% sound(y,Fs);

% plot waveform
y = y(:,1);
dt = 1/Fs;
t = 0:dt:(length(y)*dt)-dt;
figure
plot(t,y); xlabel('Seconds'); ylabel('Amplitude'); box('off');
%xticklabels({num2str(times(1)), num2str(times(1)+5), num2str(times(1)+10), num2str(times(1)+15), num2str(times(2))});

figure
plot(psd(spectrum.periodogram,y,'Fs',Fs,'NFFT',length(y)));

%[z,fs,nb]=wavread(speech_file); 
bfil=fft(y); %fft of input signal
wn=[12 25]/(Fs/2);   %bandpass
[b,a]=butter(order,wn);
fvtool(b,a);
f=filter(b,a,y);
afil=fft(f);

% plot
subplot(2,1,1);plot(real(bfil));
title('frequency respones of input signal');
xlabel('frequency');ylabel('magnitude');
subplot(2,1,2);plot(real(afil));
title('frequency respones of filtered signal');
xlabel('frequency');ylabel('magnitude');

% [b1_kaista,a1_kaista]=butter(order,[(((bandpass(1)))/(Fs/2)) ((bandpass(2))/(Fs/2))]); %creating the filters
% [b1_ali,a1_ali]=butter(order,((lowpass)/(Fs/2)),'low');
% [x1, zf]=filter(b1_kaista,a1_kaista,y,[],2); % bandpass filtering
% apu=hilbert(x1); %hilbert transformation
% clear y x1
% ensol=abs(apu);    %absolute value (envelope)
% i=1:3:size(ensol,1);
% x=1:size(ensol,2);
% ensol2=sqrt(ensol(i,x).^2+ensol(i+1,x).^2+ensol(i+2,x).^2);
% [ensol2_filt, zf_filt]=filter(b1_ali,a1_ali,ensol2,[],2); %low-pass filtering
% 
% clear ensol
% ensol=ensol2_filt(:,1:(ds):end); %downsampling
% helahoito=ensol;
%         
% zi=zf;
% zi_filt=zf_filt;
% [x1, zf]=filter(b1_kaista, a1_kaista, y, zi, 2); %bandpass filtering
% apu=hilbert(x1); %hilbert transformation
% clear y apu
% ensol=abs(apu); %absolute value (envelope)
% i=1:3:size(ensol,1);
% x=1:size(ensol,2);
% ensol2=sqrt(ensol(i,x).^2+ensol(i+1,x).^2+ensol(i+2,x).^2);
% 
% [ensol2_filt,zf_filt]=filter(b1_ali,a1_ali,ensol2,zi_filt,2); %low-pass filtering
% clear ensol
% ensol=ensol2_filt(:,1:(ds):end); %downsampling
% helahoito=[helahoito ensol];

% full version
m = 0;
while (alku+1)<(loppuaika)
    if m==0
        clear zf zi zf_filt zi_filt
        samples = [alku*Fs,(alku+1)*Fs];
        clear y
        [part,Fs] = audioread(speech_file,samples);

        [x1, zf]=filter(b1_kaista,a1_kaista, part,[],2); % bandpass filtering
        apu=hilbert(x1); %hilbert transformation
        clear part
        ensol=abs(apu);    %absolute value (envelope)
%         clear apu x1
%         i=1:3:size(ensol,1);
%         x=1:size(ensol,2);
%         ensol2=sqrt(ensol(i,x).^2+ensol(i+1,x).^2+ensol(i+2,x).^2);
        [ensol2_filt, zf_filt]=filter(b1_ali,a1_ali,ensol,[],2); %low-pass filtering % before ensol2

        clear ensol
        ensol=ensol2_filt(:,1:(ds):end); %downsampling
        alku=alku+1;
        m=1;
        helahoito=ensol;
    else
        samples = [alku*Fs,(alku+1)*Fs];
        clear y Fs
        [part,Fs] = audioread(speech_file,samples);
        
        zi=zf;
        zi_filt=zf_filt;
        [x1, zf]=filter(b1_kaista, a1_kaista, part, zi, 2); %bandpass filtering
        apu=hilbert(x1); %hilbert transformation
        clear part
        ensol=abs(apu); %absolute value (envelope)
        clear apu
%         i=1:3:size(ensol,1);
%         x=1:size(ensol,2);
%         ensol2=sqrt(ensol(i,x).^2+ensol(i+1,x).^2+ensol(i+2,x).^2);

        [ensol2_filt,zf_filt]=filter(b1_ali,a1_ali,ensol,zi_filt,2); %low-pass filtering % before ensol2
        clear ensol
        ensol=ensol2_filt(:,1:(ds):end); %downsampling
        alku=alku+1;
        helahoito=[helahoito ensol];
    end
end

% plot waveform
data_filt = helahoito(:,1);
space = 44100;
for i=1:size(helahoito,2)
    data_filt((space*i):(space*i+space)) = helahoito(:,i);
end
    
figure
y = data_filt;
y = y(1*44100:(10*44100),1);
dt = 1/Fs;
t = 0:dt:(length(y)*dt)-dt;
plot(t,y); xlabel('Seconds'); ylabel('Amplitude');
figure
plot(psd(spectrum.periodogram,y,'Fs',Fs,'NFFT',length(y)));
