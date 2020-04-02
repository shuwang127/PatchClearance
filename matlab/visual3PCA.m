function [ ] = visual3PCA( data, label )
% Funct:  visualize the features in 3-dimension using PCA.
% Input:  data - The feature matrix.
%         label - The label vector.
% Output: None.
% Author: Shu Wang, George Mason University.
% Date:   2019-10-24.

%% PCA
[COEFF, SCORE, latent] = pca(data);
SelectNum = latent ./ sum(latent);

tranMatrix = COEFF(:, 1:3);
[row , col] = size(data);
meanValue = mean(data);
normData = data - repmat(meanValue, [row, 1]);
NewData = normData * tranMatrix;

%% Plot reduced-dim data
figure();
dim = size(data, 2);
for i = 1 : numel(label)
    if (label(i) == 1)
        plot3(NewData(i,1), NewData(i,2), NewData(i,3), 'ro');
        hold on;
    elseif (label(i) == 0)
        plot3(NewData(i,1), NewData(i,2), NewData(i,3), 'b*');
        hold on;
    end
end

g = gca;
g.GridColor = 'k';
grid on;
grid minor;

end

