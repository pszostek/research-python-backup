function [data rows cols] = freadMatrix(filePath)
%   [data rows cols] = freadMatrix(filePath)
%
% Reads matrix of data from file of path = filePath.
% Returns:
%   data - matrix values
%   rows - labels of rows
%   cols - labels of cols

f = fopen(filePath);

rowsLine = fgetl(f);
rows = split(rowsLine, "\t");
rows = rows(1:(length(rows)-1), :);

colsLine = fgetl(f);
cols = split(colsLine, "\t");
cols = cols(1:(length(cols)-1), :);

data = fscanf(f, "%i", [length(rows) length(cols)]);

