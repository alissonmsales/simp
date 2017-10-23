from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, BatchNormalization, \
    regularizers
from keras.utils import to_categorical
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

import numpy as np

def treino(printar):

    #samples = np.loadtxt('classificados/skip-gram/amostras_sg50.csv',
    #samples = np.loadtxt('classificados/fasttext/amostras_sg-fsg50.csv',
    samples = np.loadtxt('classificados/glove/amostras_g50_NOK.csv',
    #samples=np.loadtxt('classificados/fasttext/amostras_sg-fsg50.csv',
                         delimiter=',',
                         dtype=np.float32)
    #labels = np.loadtxt('classificados/skip-gram/amostras_sg50_label.csv',
    #labels = np.loadtxt('classificados/fasttext/amostras_sg-f50_label.csv',
    labels = np.loadtxt('classificados/glove/amostras_g50_label.csv',
                        delimiter=',',
                        dtype=np.float32)

    train_samples = samples[100:]
    validation_samples = samples[:100]
    test_samples = samples[:100]

    train_labels = labels[100:]
    validation_labels = labels[:100]
    test_labels = labels[:100]

    #test_labels = to_categorical(test_labels, num_classes=1)
    #train_labels = to_categorical(train_labels, num_classes=1)
    model = Sequential()

    #model.add(Dense(100, input_dim=samples.shape[1], activation='relu', kernel_regularizer=regularizers.l2(0.05)))
    #model.add(Dense(100, input_dim=samples.shape[1], activation='relu', kernel_regularizer=regularizers.l2(0.05)))
    model.add(Dense(100, input_dim=samples.shape[1], activation='relu', kernel_regularizer=regularizers.l2(0.03)))
    #model.add(Dense(100, input_dim=samples.shape[1], activation='relu'))
    model.add(Dropout(0.01))
    #model.add(Dense(300, activation='relu'))
    #model.add(Dense(700, activation='relu', kernel_regularizer=regularizers.l2(0.03)))
    #model.add(Dropout(0.05))
    #model.add(Dense(300, activation='relu'))
    #model.add(Dense(500, activation='relu', kernel_regularizer=regularizers.l2(0.03)))
    #model.add(Dropout(0.5))
    #model.add(Dense(300, activation='relu'))
    #model.add(Dense(500, activation='relu', kernel_regularizer=regularizers.l2(0.03)))
    #model.add(Dropout(0.5))
    #model.add(BatchNormalization())
    model.add(Dense(1, activation='relu'))

    #model.summary()
    model.compile(optimizer='sgd',
                 loss='mean_squared_error',
                 metrics=['accuracy'])

    history = model.fit(train_samples, train_labels,
             epochs=1000,
             batch_size=75,
             validation_data=(test_samples, test_labels),
                        verbose=1)
    #print(history.history.keys())

    if printar:
        #  "Accuracy"
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Modelo da Acurácia')
        plt.ylabel('acurácia')
        plt.xlabel('número de épocas')
        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(['treino', 'teste'], prop=fontP)
        plt.show()
        # "Loss"
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Modelo de erro')
        plt.ylabel('erro')
        plt.xlabel('número de épocas')
        plt.legend(['treino', 'teste'], prop=fontP)
        plt.show()

    return (model.evaluate(validation_samples, validation_labels))

if __name__ == '__main__':
    t = []
    for i in range(6):
        t.append(treino(False))
        #print(treino(False))

    t.append(treino(True))
    print("")
    for k in t:
        print(k)
