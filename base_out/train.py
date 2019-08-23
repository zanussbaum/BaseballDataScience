import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split, RandomizedSearchCV


def load_data():    
    X = np.load('x_data.npy')
    y = np.load('y_data.npy')

    classes = np.unique(y)

    num_classes = len(classes)

    print(X.shape)
    print(y.shape)
    print(classes)
    print("there are {} classes".format(num_classes))

    return train_test_split(X, y, train_size=.8), num_classes

def create_model(num_classes, epochs=50, num_layers=2, 
                    num_nodes=50, activation=tf.nn.relu, optimizer='adam'):
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(24,10)))

    for i in range(num_layers-1):
        model.add(keras.layers.Dense(num_nodes,activation=activation))
        model.add(keras.layers.Dropout(.5))

    model.add(keras.layers.Dense(num_classes,activation=tf.nn.softmax))

    model.compile(optimizer=optimizer, 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

    return model

def random_search():
    (X_train, X_test, y_train, y_test), num_classes = load_data()

    model = keras.wrappers.scikit_learn.KerasClassifier(build_fn=create_model) 

    epochs = np.random.randint(10,100, size=5)

    num_layers = [i for i in range(2,6)]

    num_nodes = np.random.randint(50,300, size=5)

    activation = [tf.nn.relu, tf.nn.elu, tf.nn.leaky_relu,tf.nn.sigmoid]

    optimizer = ['adam', 'sgd', 'adagrad', 'adadelta']

    h_params = dict(epochs=epochs,
    num_layers=num_layers, num_nodes=num_nodes,
    activation=activation, optimizer=optimizer, num_classes=[num_classes])

    n_iter_search = 10 # Number of parameter settings that are sampled.
    random_search = RandomizedSearchCV(estimator=model, 
                                   param_distributions=h_params,
                                   n_iter=n_iter_search,
                                   n_jobs=4,
								   verbose=3)
    random_search.fit(X_train, y_train)


    print("Best: %f using %s" % (random_search.best_score_, random_search.best_params_))
    means = random_search.cv_results_['mean_test_score']
    stds = random_search.cv_results_['std_test_score']
    params = random_search.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))

    return random_search, (X_train, X_test, y_train, y_test)

def main():
    search, (X_train, X_test, y_train, y_test) = random_search()
    
    estimator = search.best_estimator_

    history = estimator.fit(
    X_train, y_train, epochs=search.best_params_['epochs'], validation_split=.2
    )

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

    test_acc = estimator.score(X_test,y_test)

    print("the test accuracy was {}".format(test_acc))

    try:
        tf.keras.models.save_model(estimator,'model.h5')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()