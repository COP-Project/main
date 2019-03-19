import tensorflow as tf
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.contrib.learn.python.learn.datasets.mnist import extract_images, extract_labels

def create_digit_model():
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)
    x_train.resize(60000, 28, 28, 1)
    x_test.resize(10000, 28, 28, 1)
    print(x_train.shape)
    print(x_test.shape)

    model = Sequential()                            # creating the Convolutional Neural Network
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=3)

    val_loss, val_acc = model.evaluate(x_test, y_test)
    print(val_loss, val_acc)

    model.save('num_reader_model_DIGITS.h5')

def create_alpha_model():
    with open('data//emnist-letters-train-images-idx3-ubyte.gz', 'rb') as f:
        train_img = extract_images(f)
    with open('data//emnist-letters-train-labels-idx1-ubyte.gz', 'rb') as f:
        train_lbl = extract_labels(f)
    with open('data//emnist-letters-test-images-idx3-ubyte.gz', 'rb') as f:
        test_img = extract_images(f)
    with open('data//emnist-letters-test-labels-idx1-ubyte.gz', 'rb') as f:
        test_lbl = extract_labels(f)

    train_img = tf.keras.utils.normalize(train_img, axis=1)
    test_img = tf.keras.utils.normalize(test_img, axis=1)
    train_img.resize(124800, 28, 28, 1)
    test_img.resize(20800, 28, 28, 1)

    model = tf.keras.models.Sequential()  # create Convolutional Neural Network
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), padding='same'))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(27, activation='softmax'))
    model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_img, train_lbl, epochs=3)

    val_loss, val_acc = model.evaluate(test_img, test_lbl)
    print(val_loss, val_acc)

    model.save('num_reader_model_ALPHA.h5')

create_digit_model()
create_alpha_model()
