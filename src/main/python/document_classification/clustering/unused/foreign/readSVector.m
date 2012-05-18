function [svector len] = readSVector(path)
%   svector = readSVector(path)
%
% Reads vector of strings from file of given path.

f = fopen(path, 'r');
len = 0;
width = 0;
while ~feof(f) 
    line = strtrim(fgets(f));
    len = len + 1;
    width = max([width length(line)]);
end;
fclose(f);

svector = char(zeros(len, width));
f = fopen(path, 'r');
for i = 1:len
    line = strtrim(fgets(f));
    svector(i,1:length(line)) = line;
end;
fclose(f);

