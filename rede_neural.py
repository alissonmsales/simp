from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import to_categorical

import numpy as np


samples = np.loadtxt('classificados/skip-gram/amostras_sg50.csv',
                     delimiter=',',
                     dtype=np.float32)
labels = np.loadtxt('classificados/skip-gram/amostras_sg50_label.csv',
                    delimiter=',',
                    dtype=np.float32)

train_samples = samples[200:]
validation_samples = samples[100:200]
test_samples = samples[:100]

train_labels = labels[200:]
validation_labels = labels[100:200]
test_labels = labels[:100]

#test_labels = to_categorical(test_labels, num_classes=1)
#train_labels = to_categorical(train_labels, num_classes=1)
model = Sequential()

model.add(Dense(300, input_dim=samples.shape[1], activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(300, activation='relu'))
model.add(Dropout(0.5))
#model.add(Dense(300, activation='relu'))
#model.add(Dropout(0.5))
#model.add(Dense(100, activation='relu'))
#model.add(Dropout(0.1))
model.add(Dense(1, activation='relu'))

model.summary()
model.compile(optimizer='sgd',
             loss='mean_squared_error',
             metrics=['accuracy'])
model.fit(train_samples, train_labels,
         epochs=200,
         batch_size=20,
         validation_data=(test_samples, test_labels))

score = model.evaluate(validation_samples, validation_labels)

print(score)

