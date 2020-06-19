# import tensorflow.compat.v1 as tf
import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as plt
import numpy as np

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from sklearn.metrics import confusion_matrix


class CnnModel:
    index = 0
    x_train = None
    y_train = None
    x_test = None
    y_test = None
    batch_size = None
    epochs = None
    # conv2D_config:
    # {'filters': 16, 'kernel_size': (2, 2), 'input_shape': (128, 128, 1), 'strides': (2, 2)}
    conv2D_config_list = list()
    # dense_config:
    # {'unit': 128}
    dense_config_list = list()
    model = Sequential()
    drop_out_rate = 0.25
    validation_split = 0.2

    def __init__(self, index, x_train, y_train, x_test, y_test, batch_size, epochs, conv2D_config_list, dense_config_list):
        self.index = index
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.batch_size = batch_size
        self.epochs = epochs
        self.conv2D_config_list = conv2D_config_list
        self.dense_config_list = dense_config_list

    def _compile_model(self):
        for config in self.conv2D_config_list:
            # 建立卷積層，filter=16,即 output space 的深度, Kernal Size: 5x5, activation function 採用 relu
            self.model.add(Conv2D(filters=config.get('filters'),
                                  kernel_size=config.get('kernel_size'),
                                  padding=config.get('padding', 'same'),
                                  activation=config.get('activation', 'relu'),
                                  input_shape=config.get('input_shape')),
                           strides=config.get('strides', (2, 2)))
            # 建立池化層，池化大小=2x2，取最大值
            self.model.add(MaxPooling2D(pool_size=(2, 2)))

        # Dropout層隨機斷開輸入神經元，用於防止過度擬合，斷開比例 = drop_out_rate
        self.model.add(Dropout(self.drop_out_rate))

        # Flatten層把多維的輸入一維化，常用在從卷積層到全連接層的過渡。
        self.model.add(Flatten())

        for config in self.dense_config_list:
            # 全連接層: unit 個 output
            self.model.add(Dense(config.get('unit'), activation='relu'))

        # Dropout層隨機斷開輸入神經元，用於防止過度擬合，斷開比例 = drop_out_rate
        self.model.add(Dropout(self.drop_out_rate))

        # 使用 softmax activation function，將結果分類
        self.model.add(Dense(self.y_train[1], activation='softmax'))

        # 編譯: 選擇損失函數、優化方法及成效衡量方式
        self.model.compile(loss="categorical_crossentropy",
                           optimizer="adam",
                           metrics=['accuracy'])

    def summary(self):
        print(self.model.summary())

    def _output_history(self, train_history, test_loss, test_accuracy, sensitivity, specificity):

        accuracy = train_history.history['accuracy']
        val_accuracy = train_history.history['val_accuracy']
        loss = train_history.history['loss']
        val_loss = train_history.history['val_loss']
        with open("model_result.txt", "a") as my_file:
            my_file.write(f'{self.index+1},{accuracy},{val_accuracy},{loss},{val_loss},{self.test_loss},{self.test_accuracy},{self.sensitivity},{self.specificity}\n')
        pass

    def _get_sensitivity_specificity(self, predictions, y_test):
        y_test = np.argmax(y_test, axis=-1)
        predictions = np.argmax(predictions, axis=-1)

        c = confusion_matrix(y_test, predictions)
        print('Confusion matrix:')
        print(c)
        print('sensitivity = ', c[0, 0] / (c[0, 1] + c[0, 0]))
        print('specificity = ', c[1, 1] / (c[1, 1] + c[1, 0]))

        return c[0, 0] / (c[0, 1] + c[0, 0]), c[1, 1] / (c[1, 1] + c[1, 0])

    def run(self):
        # 編譯 model
        self._compile_model()
        # 進行訓練, 訓練過程會存在 train_history 變數中
        train_history = self.model.fit(self.x_train,
                                       self.y_train,
                                       batch_size=self.batch_size,
                                       epochs=self.epochs,
                                       validation_split=self.validation_split,
                                       verbose=1)

        # 顯示損失函數、訓練成果(分數)
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        predictions = self.model.predict(self.x_test)
        sensitivity, specificity = self._get_sensitivity_specificity(predictions, self.y_test)
        test_loss = score[0]
        test_accuracy = score[1]
        print('Test loss:', test_loss)
        print('Test accuracy:', test_accuracy)
        print('Sensitivity:', sensitivity)
        print('Specificity:', specificity)
        self._output_history(self, train_history, test_loss, test_accuracy, sensitivity, specificity)


def show_train_history(train_history, t, v):
    plt.plot(train_history.history['accuracy'])
    plt.plot(train_history.history['val_accuracy'])
    plt.title('Train History')
    plt.xlabel('Epoch')
    plt.ylabel('accuracy')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()

    plt.plot(train_history.history['loss'])
    plt.plot(train_history.history['val_loss'])
    plt.title('Train History')
    plt.xlabel('Epoch')
    plt.ylabel('loss')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()


