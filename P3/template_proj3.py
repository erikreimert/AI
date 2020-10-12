from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np

# Model Template

#Data pre-processing
numbers = np.load("images.npy")
numbers = numbers.flatten()
labels = np.load("labels.npy")
encodedLabels = to_categorical(labels)

#Data splitting
x_train, x_test, y_train, y_test = train_test_split(numbers, labels, test_size=0.25, stratify = 'array-like', random_state=1)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.15, random_state=1)


model = Sequential() # declare model
model.add(Dense(10, input_shape=(28*28, ), kernel_initializer='he_normal')) # first layer
model.add(Activation('relu'))
# model.add(Activation('selu'))
# model.add(Activation('tanh'))
#
#
#
# Fill in Model Here
#
#
model.add(Dense(10, kernel_initializer='he_normal')) # last layer
model.add(Activation('softmax'))


# Compile Model
model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train Model
history = model.fit(x_train, y_train,
                    validation_data = (x_val, y_val),
                    epochs=10,
                    batch_size=512)


# Report Results

print(history.history)
model.predict()
