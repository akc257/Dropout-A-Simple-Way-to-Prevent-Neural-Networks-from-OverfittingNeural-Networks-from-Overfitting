# Dropout: A Simple Way to Prevent Neural Networks from Overfitting
# Austin Corum
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import decimal
import os
import csv

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
# gets rid of an error about cpu on Macbook Pro 2017
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Calculate hidden layer values, and add to list
def findValueN(prob):
    # pn = 256 for 2 first hidden layers
    # pn = 512 for last layer
        # n values are the number of hidden units at each layer
    n1 = 256.0/prob
    n2 = 256.0/prob
    n3 = 512.0/prob
    n = [n1,n2,n3,prob]
        # return number o
    return n

# Create the archetecture for constant archetecture
def addPValue(prob):
        # layers all have 2048 hidden units as described in the research paper
    n1 = 2048
    n2 = 2048
    n3 = 2048
    n = [n1,n2,n3,prob]
    return n

# Runs dropout in an neural network for specific layer values
def runDropout(*layer):
        # Sequential model and the layers that describe the model
    model = Sequential()
    model.add(Conv2D(28, kernel_size=(3,3), input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten()) # Flattening the 2D arrays for fully connected layers
    model.add(Dense(layer[0], activation=tf.nn.relu))
    model.add(Dense(layer[1], activation=tf.nn.relu))
        # probability to keep value is third index in the list
    model.add(Dropout(layer[3]))
    model.add(Dense(layer[2], activation=tf.nn.softmax))

        # Configure model before training
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

        # Train the model for a fixed number of epochs
    history_dropout = model.fit(x=x_train, y=y_train, validation_split=0.1, epochs=1, batch_size=10)

        # Training accuracy
            # Training error = 1 - Training accuracy
    accuracy = history_dropout.history['accuracy']
    train_err = 1.00 - accuracy[-1]

        # Test Accuracy
            # Test error = 1 - Test Accuracy
    val_acc = history_dropout.history['val_accuracy']
    test_err = 1.00 - accuracy[-1]
    # *** Calculate error bars HERE ***
    finalError = [test_error, train_error, layer[3]]
    return finalError
    # END OF RUN DROPOUT #

# Function to calculate all p values in a float range
def float_range(start, stop, step):
  while start <= stop:
    yield float(start)
    start += decimal.Decimal(step)

def runForAllValuesOfP():
    # lists to store ploting values locally
        # figure a error
    a_test_error = []
    a_train_error = []
        # figure b
    b_test_error = []
    b_train_error = []
        # returns the list of p values from 0.1-1.0, into list
    pValues = list(float_range(0, 1.0, '0.1'))
        # remove 0 from the pValue list
    del pValues[0]
        # run dropout on all values of p for both figures
    for i in pValues:
        # check if pValue was already calculated
            # if so, import values and don't run
            # Currently running without storing/checking for previous runs
        varyLayer = findValueN(i)
        constLayer = addPValue(i)
            # Store error values for figure a
        errorFigA = runDropout(*constLayer)
        errorFigA[0].append(a_test_list_y)
        errorFigA[1].append(a_train_list_y)
            # Store error values for figure b
        errorFigB = runDropout(*varyLayer)
        errorFigA[0].append(b_test_list_y)
        errorFigA[1].append(b_test_list_y)
    # Figure 9a
    plt.subplot(2, 2, 1)
    plt.ylabel('Classification Error %')
    plt.xlabel('Probability of retaining a unit (p)')
    plt.yticks(np.arange(0, 4, 0.5))
    plt.plot(pValues, a_test_error, label = "Test Error")
    plt.plot(pValues, a_train_error, label = "Training Error")
    plt.legend(loc='upper right')
    # Figure 9b
    plt.subplot(2, 2, 2)
    plt.ylabel('Classification Error %')
    plt.xlabel('Probability of retaining a unit (p)')
    plt.yticks(np.arange(0, 3.5, 0.5))
    plt.plot(pValues, b_test_error, label = "Test Error")
    plt.plot(pValues, b_train_error, label = "Training Error")
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

# Load dataket to appropriate valiables
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Reshaping the array to 4-dims so that it can work with the API
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
input_shape = (28, 28, 1)
# Set values to float so that we can get decimal points after division
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
# Normalizing the RGB codes by dividing it to the max RGB value
x_train /= 255
x_test /= 255

# runs both archetectures for all values of p (from 0.1-1.0, inclusive)
# Currently takes too long to run, but I'm confident that the output will come
    # close to the results in the figure
runForAllValuesOfP()
