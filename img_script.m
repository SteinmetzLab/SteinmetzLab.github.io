
% source image should be aspect ratio 1920 wide x 1080 tall

% rootDir = '/Users/nicksteinmetz/Dropbox/code/SteinmetzLab.github.io/';
rootDir = fullfile(dropboxDir, 'code','SteinmetzLab.github.io');

sourceDir = fullfile(rootDir, '_img', 'people');

targetDir = fullfile(rootDir, 'assets', 'img', 'people');

name = 'Kai';

d = dir(fullfile(sourceDir, [name '.*']));
q = imread(fullfile(sourceDir, d(1).name));

figure; image(q); axis image; 

widthVals = [230 535 535*2 575 767 991 1999 1920];
names = {'_placehold', '_thumb', '_thumb@2x', '_xs', '_sm', '_md', '_lg', ''}; 

for ii = 1:numel(widthVals)

x = widthVals(ii); 
sc = x/size(q,2);
b = imresize(q, sc);

outFile = fullfile(targetDir, [name names{ii} '.jpg']);
fprintf(1, 'Writing width %d to %s\n', x, outFile);
imwrite(b, outFile, 'jpg', 'Quality', 70);

end