

function makeImages(sourceImg)

% load image data

img = imread(sourceImg); 

[d,imName] = fileparts(sourceImg)
[~,dest] = fileparts(d);

outputDir = fullfile('assets', 'img', dest); 

targets = struct(); 
targets(end+1).width = 230; targets(end).suffix = 'placehold';
targets(end+1).width = 230; targets(end).suffix = 'placehold';
targets(end+1).width = 230; targets(end).suffix = 'placehold';
targets(end+1).width = 230; targets(end).suffix = 'placehold';
targets(end+1).width = 230; targets(end).suffix = 'placehold';
targets(end+1).width = 230; targets(end).suffix = 'placehold';
targets(end+1).width = 230; targets(end).suffix = 'placehold';

