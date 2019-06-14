function x=isc_correlation_energy(parameters)
%Calculates the correlation coefficients with the wanted window, plus saves the over time average as the first time point.
number=parameters.number;
folders=parameters.folders;
back=parameters.back;
thresholding=parameters.thresholding;
tmin=1;
tstep=0.1;
window=parameters.window;
energy_names=parameters.energy_mne_names;
cor_en=parameters.cor_en_names;

clear r_rh r_lh p_lh p_rh sol_lh sol_rh
n=0;
for j=1:number
    for k=(1+j):(number) % might this be the reason that the first subject was left out?
        %left hemishphere:
        clear inv
        clear energy_lh1 energy_rh1 energia1_alh energia1_arh energia1_blh energia1_brh
        cd(char(folders{j}));
        name_lh1=[energy_names(j,:) '-lh.stc'];
        energy_lh1=mne_read_stc_file(name_lh1);
        cd(char(folders{k}));
        toka_lh1=[energy_names(k,:) '-lh.stc'];
        vertaus_lh1=mne_read_stc_file(toka_lh1);
        cd ../average
        A_lh=energy_lh1.data;
        B_lh=vertaus_lh1.data;
        clear vertaus_lh1
        ener_cor1_lh=zeros(size(A_lh,1),floor(size(A_lh,2)/(window/tstep)));
        p_lh=zeros(size(A_lh,1),floor(size(A_lh,2)/(window/tstep)));
        l=floor(size(A_lh,2)/(size(A_lh,2)/(window/tstep)));
        for m=1:floor(size(A_lh,2)/(window/tstep))
            An=bsxfun(@minus,A_lh(:,((m-1)*(window/tstep)+1):(m*(window/tstep))),mean(A_lh(:,((m-1)*(window/tstep)+1):(m*(window/tstep))),2));
            Bn=bsxfun(@minus,B_lh(:,((m-1)*(window/tstep)+1):(m*(window/tstep))),mean(B_lh(:,((m-1)*(window/tstep)+1):(m*(window/tstep))),2));
            An=bsxfun(@times,An,1./sqrt(sum(An.^2,2)));
            Bn=bsxfun(@times,Bn,1./sqrt(sum(Bn.^2,2)));
            ener_cor1_lh(:,m)=sum(An.*Bn,2);
            e_lh=find(isnan(ener_cor1_lh(:,m)));
            ener_cor1_lh(e_lh,m)=0;
            p_lh(e_lh,m)=1;
            rho=ener_cor1_lh(:,m);
            t = rho.*sqrt((l-2)./(1-rho.^2));
            p_lh(:,m) = 2*tcdf(-abs(t),l-2);
        end
        clear energia1_alh energia1_blh
        if thresholding==1
            apu_lh= p_lh>=0.05/2;
            ener_cor1_lh(apu_lh)=NaN;
        end
        ener_cor1_lh_tot=ener_cor1_lh;
        over_time_lh=nanmean(ener_cor1_lh_tot,2);
        apu_lh=isnan(ener_cor1_lh);
        ener_cor1_lh(apu_lh)=0;
        energia1_lh.tmin=tmin;
        energia1_lh.tstep=tstep;
        energia1_lh.vertices=energy_lh1.vertices;
        energia1_lh.data=[over_time_lh,ener_cor1_lh];
        n=n+1;
        ener_name_lh=[cor_en(n,:) '-lh.stc'];
        mne_write_stc_file(ener_name_lh,energia1_lh);
        fprintf(1,'Wrote %s\n',ener_name_lh);
        clear A_lh B_lh r_lh p_lh energy_lh1 vertaus_lh1 ener_cor1_lh_tot ener_cor1_lh An Bn over_time_lh
        
        %right hemisphere:
        cd(char(folders{j}));
        name_rh1=[energy_names(j,:) '-rh.stc'];
        energy_rh1=mne_read_stc_file(name_rh1);
        cd(char(folders{k}));
        toka_rh1=[energy_names(k,:) '-rh.stc'];
        vertaus_rh1=mne_read_stc_file(toka_rh1);
        cd ../average
        A_rh=energy_rh1.data;
        B_rh=vertaus_rh1.data;
        clear vertaus_rh1
        x=1;
        ener_cor1_rh=zeros(size(A_rh,1),floor(size(A_rh,2)/(window/tstep)));
        p_rh=zeros(size(A_rh,1),floor(size(A_rh,2)/(window/tstep)));
        l=floor(size(A_rh,2)/(size(A_rh,2)/(window/tstep)));
        for m=1:floor(size(A_rh,2)/(window/tstep))
            An=bsxfun(@minus,A_rh(:,((m-1)*(window/tstep)+1):(m*(window/tstep))),mean(A_rh(:,((m-1)*(window/tstep)+1):(m*(window/tstep))),2));
            Bn=bsxfun(@minus,B_rh(:,((m-1)*(window/tstep)+1):(m*(window/tstep))),mean(B_rh(:,((m-1)*(window/tstep)+1):(m*(window/tstep))),2));
            An=bsxfun(@times,An,1./sqrt(sum(An.^2,2)));
            Bn=bsxfun(@times,Bn,1./sqrt(sum(Bn.^2,2)));
            ener_cor1_rh(:,m)=sum(An.*Bn,2);
            e_rh=find(isnan(ener_cor1_rh(:,m)));
            ener_cor1_rh(e_rh,m)=0;
            p_rh(e_rh,m)=1;
            rho=ener_cor1_rh(:,m);
            t = rho.*sqrt((l-2)./(1-rho.^2));
            p_rh(:,m) = 2*tcdf(-abs(t),l-2);
            x=x+1;
        end
        if thresholding==1
            apu_rh= p_rh>=0.05/2;
            ener_cor1_rh(apu_rh)=NaN;
        end
        ener_cor1_rh_tot=ener_cor1_rh;
        over_time_rh=nanmean(ener_cor1_rh_tot,2);
        apu_rh=isnan(ener_cor1_rh);
        ener_cor1_rh(apu_rh)=0;
        clear energia1_arh energia1_brh
        energia1_rh.tmin=tmin;
        parameters.l=l+1;
        energia1_rh.tstep=tstep;
        energia1_rh.vertices=energy_rh1.vertices;
        energia1_rh.data=[over_time_rh,ener_cor1_rh];
        ener_name_rh=[cor_en(n,:) '-rh.stc'];
        mne_write_stc_file(ener_name_rh, energia1_rh);
        fprintf(1,'Wrote %s\n',ener_name_rh);
        clear A_rh B_rh r_rh p_rh energy_rh1 vertaus_rh1 ener_cor1_rh_tot An Bn over_time_rh ener_cor1_rh
        cd(back)
    end
end
end
