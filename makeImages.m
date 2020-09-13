

function makeImages(sourceImg)

% load image data

img = imread(sourceImg); 

% is it too wide or 
desRatio = 1920/1080; 

[d,imName] = fileparts(sourceImg);
[~,dest] = fileparts(d);

outputDir = fullfile('assets', 'img', dest); 

targets = struct(); 
targets(end+1).width = 230; targets(end).suffix = 'placehold';
targets(end+1).width = 535; targets(end).suffix = 'thumb';
targets(end+1).width = 535*2; targets(end).suffix = 'thumb@2x';
targets(end+1).width = 575; targets(end).suffix = 'xs';
targets(end+1).width = 767; targets(end).suffix = 'sm';
targets(end+1).width = 991; targets(end).suffix = 'md';
targets(end+1).width = 1999; targets(end).suffix = 'lg';
targets(end+1).width = 1920; targets(end).suffix = '';

qual = 70; 

for ii = 1:numel(targets)
    if ~isempty(targets(ii).suffix)
        fn = [imName '_' targets(ii).suffix]; 
    else 
        fn = imName; 
    end
    imgR = imresize(img, origW/targets(ii).width); 
    imwrite(imgR, fullfile(outputDir,fn), 'JPEG', 'Quality', qual);
end