
%Skrypt wczytuje macierz podobienstw i generuje klastry.
% assignment - wektor przyporzadkowan do klastrow elementow
% labels - wektor etykiek elementow

args = argv();
if length(args) ~= 4
    error("[ERROR] Exactly four arguments are expected: input-matrix-path k-value maxits assignment-out-path");
end;

simMatrixPath   = args(1){1,1}
K               = str2num( args(2){1,1} )
maxits          = str2num( args(3){1,1} )
assignmentPath  = args(4){1,1}

fprintf('[kmedoids.m] Reading similarity matrix...\n');
[S rows cols] = freadFloatMatrix(simMatrixPath);
labels = rows;
N = size(labels, 1);

fprintf('[kmedoids.m] %i-centroids clustering of %i elements...\n', K, N);
[assignments, dpsims]=kcc(S, K, 1, maxits); % nruns, maxits
assignment = assignments(:,1);
clusters = unique(assignment);

fprintf('[kmedoids.m] Writing results: assignment of %i elements to %i clusters...\n', ...
        length(assignment), length(clusters));
save(assignmentPath, 'assignment', '-ascii');

fprintf('[kmedoids.m] Done.');




