function drawHist(count, l, u, s)
%   drawHist(count, l, u, s)
%
% Takes vector that contains count of elements and draws histogram.
% Arguments:
%  count - count of elements
%  [l u] - histogram range
%  s - histogam's bar width


edges = l:s:u;
N = histc (count, edges);
bar(edges, N, 1);
xlim([l u]);
title(strcat("Range=",num2str(l),"-",num2str(u),"; Bin width=",num2str(s)));
xlabel('Count');
ylabel('No of elements');
