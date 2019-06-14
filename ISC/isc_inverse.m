function save_names=isc_inverse(parameters,names)
% Reads inverse operator from mne-files into a matlab-format.

number=parameters.number;
back=parameters.back;
folders=parameters.folders;
inv_names=parameters.inv_names;
save_names=parameters.inv_s_names;
for j=1:number
    if (j~=1)
        clear cfg
        clear inv
        clear file1
    end
    cd(char(folders(j)));
    file1=fiff_setup_read_raw(names{j,:});
    %cd MNE;
    cfg=struct('invname',inv_names(j,:));
    
    if isfield(cfg,'invname')
        inv = mne_read_inverse_operator(cfg.invname);
        if ~isfield(cfg,'snr')
            cfg.snr = 1;
        end
        ntrials = 1;
        inv = mne_prepare_inverse_operator(inv, ntrials, 1/cfg.snr^2, 1);
        inv.chsel = fiff_pick_channels(file1.info.ch_names, inv.noise_cov.names);
        trans=diag(sparse(inv.reginv))*inv.eigen_fields.data*inv.whitener*inv.proj;
        if inv.eigen_leads_weighted
            fprintf(1,'(eigenleads already weighted)...\n');
            sol = inv.eigen_leads.data*trans;
        else
            fprintf(1,'(eigenleads need to be weighted)...\n');
            sol = diag(sparse(sqrt(inv.source_cov.data)))*inv.eigen_leads.data*trans;
        end
        inv.operator=sol;
        fprintf('Using an inverse operator: %d matching real -> %d virtual channels\n', length(inv.chsel), size(inv.operator,1));
    else
        inv.chsel = 1:file1.info.nchan;
        inv.operator = eye(file1.info.nchan);
        fprintf('Using sensor-level signals: %d real channels\n', length(inv.chsel));
    end
    save(save_names(j,:), 'inv')
end
cd(back)
