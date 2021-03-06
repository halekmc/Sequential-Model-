import numpy as np
import random
from sklearn.utils import shuffle
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy



train_labels = []
train_samples = []
test_labels =  []
test_samples = []

for i in range(50):
    random_younger = random.randint(13,64)
    train_samples.append(random_younger)
    train_labels.append(1)

    random_older = random.randint(65,100)
    train_samples.append(random_older)
    train_labels.append(0)

for i in range(1000):
    random_younger = random.randint(13,64)
    train_samples.append(random_younger)
    train_labels.append(0)

    random_older = random.randint(65,100)
    train_samples.append(random_older)
    train_labels.append(1)

for i in train_samples:
    print(i)

train_labels = np.array(train_labels)
train_samples = np.array(train_samples)
train_labels, train_samples = shuffle(train_labels, train_samples)

scaler = MinMaxScaler(feature_range=(0,1))
scaled_train_samples = scaler.fit_transform(train_samples.reshape(-1,1))
for i in range(10):
    # The 5% of younger individuals who did experience side effects
    random_younger = random.randint(13,64)
    test_samples.append(random_younger)
    test_labels.append(1)

    # The 5% of older individuals who did not experience side effects
    random_older = random.randint(65,100)
    test_samples.append(random_older)
    test_labels.append(0)

for i in range(200):
    # The 95% of younger individuals who did not experience side effects
    random_younger = random.randint(13,64)
    test_samples.append(random_younger)
    test_labels.append(0)

    # The 95% of older individuals who did experience side effects
    random_older = random.randint(65,100)
    test_samples.append(random_older)
    test_labels.append(1)

test_labels = np.array(test_labels)
test_samples = np.array(test_samples)
test_labels, test_samples = shuffle(test_labels, test_samples)
scaled_test_samples=scaler.fit_transform(test_samples.reshape(-1,1))


physical_devices=tf.config.experimental.list_physical_devices('GPU')
print("Num GPUs Available:", len(physical_devices))
tf.config.experimental.set_memory_growth(physical_devices[0], True)

model=Sequential([

    Dense(units=16, input_shape=(1,), activation='relu'),
    Dense(units=32, activation='relu'),
    Dense(units=2, activation='softmax')
])

model.summary()

model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x=scaled_train_samples, y=train_labels,validation_split=0.1, batch_size=10, epochs=30, verbose=2)

predictions = model.predict(
      x=scaled_test_samples
    , batch_size=10
    , verbose=0
)  

for i in predictions:
    print(i)

rounded_predictions=np.argmax(predictions, axis=-1)
for i in rounded_predictions:
    print(i)


