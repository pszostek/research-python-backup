
%Skrypt wczytuje macierz podobienstw i generuje klastry.
% assignment - wektor przyporzadkowan do klastrow elementow
% labels - wektor etykiek elementow
% prefix_len - jaka jest dlugosc prefiksu wyzszego rzedu

args = argv();
if length(args) ~= 2
    error("[ERROR] Exactly two arguments are expected: input-matrix-path labels'-prefix-length");
end;

simMatrixPath   = args(1){1,1}
prefix_len      = str2num( args(2){1,1} )

[pathstr, name, ext] = fileparts(simMatrixPath);
assignmentPath  = strcat('/tmp/tr_', name, '_assignment_', num2str(prefix_len), '.vector')
labelsPath      = strcat('/tmp/tr_', name, '_labels_', num2str(prefix_len),'.svector')



fprintf('Reading similarity matrix...\n');
[S rows cols] = freadFloatMatrix(simMatrixPath);
labels = rows;
N = size(labels, 1);

fprintf('Count prefixes of %i labels...\n', size(labels, 1) );
uq = countUqPrefixes(labels, prefix_len);
K = size(uq, 1);

fprintf('%i-centroids clustering...\n', K);
[assignments, dpsims]=kcc(S, K, 1, 10000); % nruns, maxits
assignment = assignments(:,1);
clusters = unique(assignment);

fprintf('Writing results: assignment of %i elements to %i clusters...\n', ...
        length(assignment), length(clusters));
save(assignmentPath, 'assignment', '-ascii');


fprintf('Writing labels...\n');
writeSVector(labels, labelsPath)



