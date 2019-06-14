function mod_times=isc_start_finish(file,start_time,parameters)
%Finds the first and the last second when the modulating signal is on and saves them.

nro=1;
trig_ch=parameters.trig_ch;
sf=parameters.sf;
endless=0;
fileids=parameters.fileids;
stimulus_time=parameters.stimulus_time(fileids);
style=parameters.length_style;

if style==1
    time=ceil(double(file.first_samp)/sf);
    mod_start=time;
    mod_end=time+stimulus_time;
    mod_times=[mod_start mod_end];
end

if style==5
    mod_start=start_time;
    mod_end=mod_start+stimulus_time;
    mod_times=[mod_start mod_end];
end

if (ne(style,1) && ne(style,5))
    if nro==1
        time=ceil(double(file.first_samp)/sf);
        end_time=floor(double(file.last_samp)/sf);
        part=fiff_read_raw_segment_times(file, time, time+0.5);
        noise_ampl=abs(max(part(trig_ch,:))-min(part(trig_ch,:))+0.000001);
        i=1;
        check=0;
        mod_start=time;
        clear part
        part=fiff_read_raw_segment_times(file, mod_start(i,:), mod_start(i,:)+2);
        bla=part(trig_ch,:);
        difference=abs(max(bla)-min(bla));
        
        while ((difference<(500*noise_ampl))&&((mod_start(i,:)+2)<end_time))
            mod_start=mod_start+2;
            part=fiff_read_raw_segment_times(file, mod_start(i,:), mod_start(i,:)+2);
            bla=part(trig_ch,:);
            difference=abs(max(bla)-min(bla));
        end
        if (check==0)
            for j=1:size(part,2)
                if (abs(part(trig_ch,j))-256)>(100*noise_ampl)
                    mod_start=mod_start+((j-1)/sf);
                    break
                end
            end
            check=1;
        end
    end
end
if style==2
    mod_end=mod_start+stimulus_time;
    mod_times=[mod_start mod_end];
end
if style==3 || style==4
    if style==4
        mod_start=start_time+1;
        part=fiff_read_raw_segment_times(file, mod_start, mod_start+1);
        bla=part(trig_ch,:);
        difference=abs(max(bla)-min(bla));
        check=0;
        while ((abs(difference)<500*noise_ampl)&&(mod_start<end_time))
            mod_start=mod_start+1;
            part=fiff_read_raw_segment_times(file, mod_start, mod_start+1);
            bla=part(trig_ch,:);
            difference=abs(max(bla)-min(bla));
            if difference==256
                difference=0;
            end
        end
        if (check==0)
            for j=1:size(part,2)
                if (abs(part(trig_ch,j))-256)>(100*noise_ampl)
                    mod_start=(mod_start)+((j-1)/sf);
                    endless=1;
                    break
                end
            end
            check=1;
        end
        if endless==0
            mod_start=start_time;
            print('Attention! Start trigger could not be identified. Check your variable "start_time" (consider making it smaller)!')
        end
        clear endless
        % now the exact start should be found
    end
    endless=0;
    mod_end=round(mod_start+stimulus_time);
    part=fiff_read_raw_segment_times(file, mod_end, mod_end+1);
    bla=part(trig_ch,:);
    difference=abs(max(bla)-min(bla));
    check=0;
    while ((abs(difference)<500*noise_ampl)&&(mod_end<end_time))
        mod_end=mod_end+1;
        part=fiff_read_raw_segment_times(file, mod_end, mod_end+1);
        bla=part(trig_ch,:);
        difference=abs(max(bla)-min(bla));
        if difference==256
            difference=0;
        end
    end
    if (check==0)
        for j=1:size(part,2)
            if (abs(part(trig_ch,j))-256)>(100*noise_ampl)
                mod_end=(mod_end)+((j-1)/sf);
                endless=1;
                break
            end
        end
        check=1;
        
    end
    if endless==0
        mod_end=double(file.last_samp/sf);
    end
    
    mod_times=[mod_start mod_end];
    
end

end
