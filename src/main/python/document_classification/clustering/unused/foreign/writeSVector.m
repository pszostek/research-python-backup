function writeSVector(svector, path)
%   writeSVector(svector, path)
%
% Writes vector of strings into file of given path.

fout = fopen(path, 'w');
for l = 1: size(svector, 1)
    fprintf(fout, "%s", svector(l, :)' );
    fprintf(fout, "\n");
end;
fclose(fout);
