from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np

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
model.add(Activation('softmax'))
# model.add(Activation('relu'))
# model.add(Activation('selu'))
# model.add(Activation('tanh')) #best so far


# Compile Model
model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train Model
history = model.fit(x_train, y_train,
                    validation_data = (x_val, y_val),
                    epochs=100,
                    batch_size=500)


# Report Results
# print(history.history)
print(model.evaluate(numbers, encodedLabels))

y_pred = model.predict(x_test)

#find guesses that dont match label
#reshape to 1,28,28
hold = []
for x in y_pred:
    max = x.max()
    y = np.where(x == max)
    hold.append(y[0])
hold = np.array(hold)

misses = []
counter = 0
print(hold[0][0], y_test[0])
for x in range(len(hold)):
    if hold[x][0] != y_test[x]:
        misses.append(x_test[x])
        counter+=1
        if counter == 3:
            break
#print each item in misses
print(confusion_matrix(y_test, hold))
