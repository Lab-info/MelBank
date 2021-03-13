import os
from tensorflow.keras import layers
from tensorflow.keras import Model
import numpy as np

from core import config


class NNet:
    def __init__(self):
        self.nnet: Model = self.make_nnet()

    # make nnet with keras
    def make_nnet(self) -> Model:
        input_layer = layers.Input(shape=config.INPUT_SHAPE)
        hidden_layer1 = layers.Dense(256, activation='relu')(input_layer)
        drop_layer1 = layers.Dropout(0.5)(hidden_layer1)
        hidden_layer2 = layers.Dense(256, activation='relu')(drop_layer1)
        drop_layer2 = layers.Dropout(0.5)(hidden_layer2)
        output_layer = layers.Dense(
            config.DATA_SAMPLES, activation='sigmoid')(drop_layer2)

        # make & compile
        result: Model = Model(inputs=input_layer, outputs=output_layer)
        result.compile(
            optimizer=config.OPTIMIZER,
            loss=config.LOSS,
            metrics=['accuracy'],
        )

        # load trained weights
        if os.path.exists(config.MODEL_PATH):
            result.load_weights(config.MODEL_PATH)

        return result

    # predict the time-freq mask
    def predict(self, data: np.ndarray) -> np.ndarray:
        result: np.ndarray = self.nnet.predict(data)[0]
        return result
