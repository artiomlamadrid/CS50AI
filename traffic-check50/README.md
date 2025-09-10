Test 1:

Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Flatten
Dense 128 ReLU
Dense softmax (output layer)
--> accuracy: 0.9366 - loss: 0.4659

Test 2:

Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (64 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Max pooling (2x2)
Flatten
Dense 128 ReLU
Dense softmax (output layer)
--> accuracy: 0.9555 - loss: 0.2773

Test 3:

Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (64 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Max pooling (2x2)
Flatten
Dense 128 ReLU
Dropout 0.5
Dense softmax (output layer)
--> accuracy: 0.9703 - loss: 0.1052

Test 4:

Convolution layer (64 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Max pooling (2x2)
Flatten
Dense 128 ReLU
Dropout 0.5
Dense softmax (output layer)
--> accuracy: 0.9263 - loss: 0.2823

Test 5:

Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (64 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Max pooling (2x2)
Flatten
Dense 256 ReLU
Dropout 0.5
Dense softmax (output layer)
--> accuracy: accuracy: 0.9474 - loss: 0.2036

Test 6:

Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (64 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Max pooling (2x2)
Flatten
Dense 128 ReLU
Dense 128 ReLU
Dropout 0.5
Dense softmax (output layer)
--> accuracy: accuracy: 0.9560 - loss: 0.2334

Test 7:

Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (64 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Max pooling (2x2)
Flatten
Dense 128 ReLU
Dropout 0.5
Dense softmax (output layer)
--> accuracy: accuracy: 0.0543 - loss: 3.5018

Test 8:

Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (64 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Max pooling (2x2)
Dense 128 ReLU
Dropout 0.5
Flatten
Dense softmax (output layer)
--> accuracy: accuracy: 0.9622 - loss: 0.1799

Test 9:

Convolution layer (32 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Convolution layer (64 feature detectors) (3x3) ReLU (input layer)
Pooling layer (2x2)
Max pooling (2x2)
Batch normalization
Dense 128 ReLU
Dropout 0.5
Flatten
Dense softmax (output layer)
--> accuracy: 0.9773 - loss: 0.0971
