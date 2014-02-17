MSS5.rst    8-bit unsigned integer data from the MSS sensor;
gcp.txt     ground control points. Columns are: id, x_RT90, y_RT90, column_MSS, row_MSS;

MSS data starts at lower-left corner. Size of the data is 512x512 pixels and each 512 pixels
segment represents line from left to right, until to the end (higher-right corner). 

% Read satellite data in Matlab
fid = fopen('MSS5.rst','r');
data = fread(fid,[512,512],'uint8')';
fclose(fid);
% ... and visualize
figure
imagesc(data) 
set(gca,'YDir','normal','CLim',[10 60])
colormap(gray)
colorbar
