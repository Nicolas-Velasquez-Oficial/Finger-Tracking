function [NUM_MVS] = computeNUM_MVS(X)

for i=1:size(X,1)
    NUM_MVS(i) = max(find(X(i,:)~=0));
end

end