function fwriteMatrix(filePath, data, rows, cols)
%   [data rows cols] = fwriteMatrix(filePath, data rows cols)
%
% Writes matrix of data to file of path = filePath.
% Returns:
%   data - matrix values
%   rows - labels of rows
%   cols - labels of cols

f = fopen(filePath, 'w');

for i = 1: size(rows, 1)
    fprintf(f, '%s\t', rows(i,:))
end;
fprintf(f, '\n');

for i = 1: size(cols, 1)
    fprintf(f, '%s\t', cols(i,:))
end;
fprintf(f, '\n');

for r = 1:size(data, 1)
    fprintf(f, '%i\t', data(r,:) );
    fprintf(f, '\n');
end;

fclose(f);
