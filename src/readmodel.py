import numpy as np
import matplotlib.pyplot as plt
from tensorflow.contrib.learn.python.learn.datasets.mnist import extract_images, extract_labels
import tensorflow as tf
from tensorflow.python.keras.models import Sequential, load_model


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
x_train.resize(60000, 28, 28, 1)
x_test.resize(10000, 28, 28, 1)

new_model = load_model('num_reader_model_DIGITS.h5')

predictions = new_model.predict([x_test])
print(x_test.shape)
print('Number read: ' + str(np.argmax(predictions[1000])))
x_test.resize(10000, 28, 28)
plt.imshow(x_test[1000], cmap=plt.cm.binary)
plt.show()

with open('data//emnist-letters-train-images-idx3-ubyte.gz', 'rb') as f:
    train_img = extract_images(f)
with open('data//emnist-letters-train-labels-idx1-ubyte.gz', 'rb') as f:
    train_lbl = extract_labels(f)
with open('data//emnist-letters-test-images-idx3-ubyte.gz', 'rb') as f:
    test_img = extract_images(f)
with open('data//emnist-letters-test-labels-idx1-ubyte.gz', 'rb') as f:
    test_lbl = extract_labels(f)

train_img.resize(124800, 28, 28, 1)
test_img.resize(20800, 28, 28, 1)
new_model = load_model('num_reader_model_ALPHA.h5')

predictions = new_model.predict([test_img])
print('Char read: ' + str(np.argmax(predictions[12000])))
plt.imshow(test_img[12000].squeeze())
plt.show()
