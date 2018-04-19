function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

% Setup some useful variables
m = size(X, 1);
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));
Y = zeros(size(y), 10);

# MY CODE STARTS HERE
% =========================================================================

% -------------------------------------------------------------

#Convert y (row vector) into a row "vector" of one-hot column vectors
Y = y == [1:max(y)];
y = Y;

#add bias value (1) to inputs
XWBias = [ones(size(X, 1), 1) X];

#calculate activation of second layer
#for each input example in X
a2 = sigmoid(Theta1 * XWBias.');

#add bias value (1) to activation of second layer
a2WBias = [ones(1, size(a2, 2)); a2];

#calculate output/activation of output layer
h = sigmoid(Theta2 * a2WBias);

#compute cost from cost function, by multiplying the proper matrices element-wise, and summing all matrice values
J = 1/m * sum(sum(y .* -log(h).' + (1-y) .* -log(1 - h).')) + lambda/(2*m) * sum(sum([Theta1(:, 2:end) Theta2(:, 2:end).'] .* [Theta1(:,2:end) Theta2(:, 2:end).']))

#compute the error values for backpropagation
error3 = h - y.';
error2 = Theta2(:, 2:end).' * error3 .* sigmoidGradient(Theta1 * XWBias.');

#compute the delta values based on activations and error values
#the activations and error values already have an additional dimension storing the different training examples
#so matrix multiplication works to sum the delta values across all training examples
delta2 = error3 * a2WBias.';
delta1 = error2 * XWBias;

#calculate gradients based on delta values
#add regularization to gradients, but not for the "bias values" (first columns) of thetas
Theta1_grad = 1/m * delta1 + lambda/m * [zeros(size(Theta1, 1), 1) Theta1(:,2:end)];
Theta2_grad = 1/m * delta2 + lambda/m * [zeros(size(Theta2, 1), 1) Theta2(:,2:end)];

% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];

end
