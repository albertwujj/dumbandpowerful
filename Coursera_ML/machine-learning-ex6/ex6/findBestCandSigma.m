load('ex6data3.mat');



fprintf('Program paused. Press enter to continue.\n');
pause;

E = zeros(7,7);
for i = 1:7
    C = .01 * 3 ** (i - 1)
    for j = 1:7
        sigma = .01 * 3 ** (j - 1)
        model = svmTrain(X, y, C, @(x1,x2)gaussianKernel(x1,x2,sigma));
        E(i,j) = mean(double(svmPredict(model,Xval) ~= yval));
    end
end

#returns row vector of smallest value in each column
#(best C value for each sigma)
[EBC,I] = min(E);

#returns smallest value in row vector
[EB,j] = min(EBC);

fprintf("%f %f", .01 * 3 ** (I(j) - 1), .01 * 3 ** (j - 1))