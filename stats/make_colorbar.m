% Create colorbar for ISC figures.

% author: Anja Thiede <anja.thiede@helsinki.fi>

%% for colorbar with three labels
% first time compile this section, then edit in colormapeditor
axes('Clim',[-6.00 6.00],'visible','off');
fig = gcf;
x_width=20 ;y_width=91.25;
fig.PaperPosition = [0 0 x_width y_width];
fig.Color = [1 1 1];

colorbar('Location','east');
drawnow;

colormapeditor

%%
% second time run this section, check if everything is fine

colorbar('YTick',[-6,0,6],'YTickLabel',{[char(hex2dec('2212')) '6.00'],'\pm3.41','+6.00'},'Location','east');
set(gca,'fontsize',60,'fontweight','demi')

%% save

F = getframe(fig);
imwrite(F.cdata, 'E:/free_listening/results/legends/T-stats-colorbar.tif', 'tif','Compression','None')

%% loop

files = {'/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/clim_5.000000e-01-4Hz.mat',
    '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/clim_4-8Hz.mat',
    '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/clim_8-12Hz.mat',
    '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/clim_12-25Hz.mat',
    '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/clim_25-45Hz.mat',
    '/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/clim_55-90Hz.mat'};

for i=1:length(files)
    load(files{i})
    colorbar('YTick',[-6,0,6],'YTickLabel',{sprintf('%.0f',clim.lims(1,1)), sprintf('%.0f',clim.lims(1,2)),sprintf('%.0f',clim.lims(1,3))},'Location','east');
    set(gca,'fontsize',60,'fontweight','demi')
    F = getframe(fig);
    imwrite(F.cdata, ['/media/cbru/SMEDY/results/ISCs_comp_against_0/legend/T-stats-colorbar', num2str(i),'.jpg'], 'jpg', 'quality', 100)
end
%% for colorbar with two labels
% first time compile this section, then edit in colormapeditor
b=axes('Clim',[-6.00 6.00],'visible','off');
fig = gcf;
x_width=20 ;y_width=91.25;
fig.PaperPosition = [0 0 x_width y_width];

c = colorbar('Location','east');
drawnow;

colormapeditor

%%
% second time run this section, check if everything is fine

colorbar('YTick',[-6,0,6],'YTickLabel',{'0.0179','0.0001','0.0290'},'Location','east');
set(gca,'fontsize',60,'fontweight','demi')

%% save

F    = getframe(fig);
imwrite(F.cdata, '/media/cbru/SMEDY/results/legends/ISC-colorbar.jpg', 'jpg','quality',100)

%% loop

load('/media/cbru/SMEDY/results/legends/labels.mat') %matrix of min and max values in order of frequency bands

for i=1:length(labels)
    colorbar('YTick',[-6,6],'YTickLabel',{sprintf('%.4f',labels(i)),sprintf('%.4f',labels(i,2))},'Location','east');
    set(gca,'fontsize',38,'fontweight','demi')
    set(gcf, 'color','w')
    F = getframe(fig);
    imwrite(F.cdata, ['/media/cbru/SMEDY/results/legends/ISC-colorbar',num2str(i)],'jpg','quality',100)
end

