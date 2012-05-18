function count = loadDrawHist(countPath)
%   count = loadDrawHist(countPath)
%
% Loads from file vector of counts of elements and draws histogram of it.

count = load(countPath);
l = min(count);
u = max(count);
s = ceil((u-l)/20);

drawHist(count, l, u, s);
