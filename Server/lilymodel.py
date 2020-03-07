import numpy as np
# import pandas as pd
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics import mean_squared_error
import keras as K
from keras.models import Model
from keras.layers import Dense, LSTM, Input, concatenate, BatchNormalization
import keras.losses
import tensorflow as tf


def mean_squared_error(a, b):
    return (a[0][0]-b[0][0])**2


class LilypodML():

    def __init__(self):
        self.model = self.initializeModel()

    def initializeModel(self):
        # define three sets of inputs
        inputSpec = Input(batch_shape=(1, 1, 1000))
        inputPh = Input(batch_shape=(1, 1, 1))
        inputCond = Input(batch_shape=(1, 1, 1))

        # # the first branch operates on the spectrometery input
        # w = LSTM(10, activation="relu", batch_input_shape=(1, 1, 10), return_sequences=True, stateful=True)(inputSpec)
        # w = BatchNormalization()(w)
        # w = LSTM(50, activation="relu", return_sequences=True, stateful=True)(w)
        # w = BatchNormalization()(w)
        # w = LSTM(10, activation="relu", return_sequences=False, stateful=True)(w)
        # w = Model(inputs=inputSpec, outputs=w)
        # # the second branch opreates on the pH input
        # x = LSTM(3, activation="relu", batch_input_shape=(1, 1, 1), return_sequences=True, stateful=True)(inputPh)
        # x = BatchNormalization()(x)
        # x = LSTM(1, activation="relu", return_sequences=False, stateful=True)(x)
        # x = BatchNormalization()(x)
        # x = Model(inputs=inputPh, outputs=x)
        # # the third branch opreates on the conductivity input
        # y = LSTM(3, activation="relu", batch_input_shape=(1, 1, 1), return_sequences=True, stateful=True)(inputCond)
        # y = BatchNormalization()(y)
        # y = LSTM(1, activation="relu", return_sequences=False, stateful=True)(y)
        # y = BatchNormalization()(y)
        # y = Model(inputs=inputCond, outputs=y)

        # the first branch operates on the spectrometery input
        w = Dense(100, activation="relu", batch_input_shape=(1, 1, 10))(inputSpec)
        w = BatchNormalization()(w)
        w = Dense(50, activation="relu")(w)
        w = BatchNormalization()(w)
        w = Dense(10, activation="relu")(w)
        w = Model(inputs=inputSpec, outputs=w)
        # the second branch opreates on the pH input
        x = Dense(3, activation="relu", batch_input_shape=(1, 1, 1))(inputPh)
        x = BatchNormalization()(x)
        x = Dense(1, activation="relu")(x)
        x = BatchNormalization()(x)
        x = Model(inputs=inputPh, outputs=x)
        # the third branch opreates on the conductivity input
        y = Dense(3, activation="relu", batch_input_shape=(1, 1, 1))(inputCond)
        y = BatchNormalization()(y)
        y = Dense(1, activation="relu")(y)
        y = BatchNormalization()(y)
        y = Model(inputs=inputCond, outputs=y)

        # combine the output of the three branches
        combined = concatenate([w.output, x.output, y.output], axis=-1)
        # apply a FC layer and then a regression prediction on the
        # combined outputs
        # z = Dense(10, activation="sigmoid")(combined)
        z = Dense(1, activation="linear")(combined)
        # our model will accept the inputs of the two branches and
        # then output a single value
        model = Model(inputs=[w.input, x.input, y.input], outputs=z)
        model.compile(loss="mse", optimizer='adam')
        return model

    def fitModel(self, nb_epoch, data, label):
        self.model.fit(data, label, epochs=nb_epoch, batch_size=1, shuffle=False)

    def predictScore(self, data):
        return self.model.predict(data)

    def resetStates(self):
        return self.model.reset_states()


if __name__ == '__main__':
    xdata = [np.array([[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]]), np.array([[[2]]]), np.array([[[3]]])]
    lilyML = LilypodML()
    lilyML.resetStates()
    lilyML.fitModel(2000, xdata, np.array([[0.5]]))
    score = lilyML.predictScore(xdata)
    loss = mean_squared_error(score, [[0.5]])
    print(score)
    print(loss)
