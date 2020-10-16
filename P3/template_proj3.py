from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Model Template

#Data pre-processing
numbers = np.load("images.npy")
numbers = numbers.reshape(6500, 784)
labels = np.load("labels.npy")
encodedLabels = to_categorical(labels)
encodedLabels = np.array(encodedLabels)

#Data splitting
x_train, x_test, y_train, y_test = train_test_split(numbers, labels, test_size=0.25, stratify = labels, random_state=1)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.1125, stratify = y_train, random_state=1)

#one hot encoding
# y_test = to_categorical(y_test)
y_train = to_categorical(y_train)
y_val = to_categorical(y_val)

model = Sequential() # declare model
model.add(Dense(10, input_shape=(28*28, ), kernel_initializer='he_normal')) # first layer

#different initializations
#different dense numbers f.e: 10

# model.add(Activation('relu'))
# model.add(Activation('selu'))
# model.add(Activation('softmax'))
model.add(Activation('tanh')) #best so far
#
#
#
# Fill in Model Here
#
#
model.add(Dense(10, kernel_initializer='he_normal')) # last layer
# model.add(Activation('softmax'))
# model.add(Activation('relu'))
# model.add(Activation('selu'))
model.add(Activation('tanh')) #best so far


# Compile Model
model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train Model
history = model.fit(x_train, y_train,
                    validation_data = (x_val, y_val),
                    epochs=100,
                    batch_size=500)


#### Report Results

#Print avg Loss and Accuracy
print(model.evaluate(numbers, encodedLabels))


# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
####
#Saves the model
model.save('model')

#### Confusion matrix and pictures
#gets the predicted guesses on the testing set
y_pred = model.predict(x_test)

hold = [] #list of predicted values by the model
#this loop gets the actual guess and puts them as a numpy array
for x in y_pred:
    max = x.max()
    y = np.where(x == max)
    hold.append(y[0])
hold = np.array(hold)

misses = np.empty((3, 784)) #empty array for 3 missed images
counter = 0
#this loop will check for three images that match missed guess in order to print them out
for x in range(1625):
    if hold[x][0] is not y_test[x]:
        misses[x] = x_test[x]
        counter+=1
        if counter == 3:
            break
#print each item in misses
misses = misses.reshape(3, 28, 28)


#this loop saves the 3 pictures that we got wrong, oopsie
counter = 0
for x in misses:
    counter+=1
    plt.imshow(x)
    plt.savefig(('error ' + str(counter) + ".png"))

#this prints the confusion matrix, simple dimple
print(confusion_matrix(y_test, hold))
####


# Description of the set of experiments that you performed: 20 pts

# For your best performing model:
# Description of the model and the model training procedure: 10 pts
# Training performance plot: 10 pts DONE
# Performance (accuracy, precision and recall) of your best performing model: 5 pts
# Confusion matrix of your best performing model: 5 pts DONE
# Visualization of three misclassified images: 10 pts DONE
#
#Copy of best performing model DONE
