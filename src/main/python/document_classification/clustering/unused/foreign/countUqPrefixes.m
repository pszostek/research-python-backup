function uq = countUqPrefixes(labels, len)
% uq = countUqPrefixes(labels, len)
% 
% Takes vector of strings (labels) and generates new vector.
% New vector containts all unique prefixes of length len of labels.
% Returns: uq - unique prefixes of length of labels


prefixes = labels(:,1);
for i = 2: len
    prefixes = strcat(prefixes, labels(:,i));
end;

uq = unique(prefixes, "rows");

end


