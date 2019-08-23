import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from train import load_data

(X_train, X_test, y_train, y_test), num_classes = load_data()

model = keras.Sequential()
model.add(keras.layers.Flatten(input_shape=(24,10)))
model.add(keras.layers.Dense(491,activation=tf.nn.relu))
model.add(keras.layers.Dropout(.5))
model.add(keras.layers.Dense(491,activation=tf.nn.relu))
model.add(keras.layers.Dropout(.5))
model.add(keras.layers.Dense(num_classes,activation=tf.nn.softmax))

model.compile(optimizer='sgd', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train,y_train, epochs=70, validation_split=.2)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.savefig("model_accuracy")
plt.figure()
plt.show(block=False)
plt.pause(3)
plt.close()
plt.cla()


plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.savefig("model_loss")
plt.figure()
plt.show(block=False)
plt.pause(3)
plt.close()

test_loss, test_acc = model.evaluate(X_test, y_test)

model.save('saved_model')

print('Test accuracy:', test_acc)

print("model weights: {}".format(model.weights))