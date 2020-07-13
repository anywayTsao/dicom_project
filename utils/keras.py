import tensorflow.compat.v1 as tf
from tensorflow.keras import backend as K
# import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as plt
import numpy as np
import gc

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from sklearn.metrics import confusion_matrix
from datetime import datetime

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
    model = None
    drop_out_rate1 = 0.25
    drop_out_rate2 = 0.25
    validation_split = 0.2
    current_time = datetime.now()

    def __init__(self, x_train, y_train, x_test, y_test, loss="categorical_crossentropy"):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.loss = loss

    def _compile_model(self):
        self.model = Sequential()

        for config in self.conv2D_config_list:
            # 建立卷積層，filter=16,即 output space 的深度, Kernal Size: 5x5, activation function 採用 relu
            self.model.add(Conv2D(filters=config.get('filters'),
                                  kernel_size=config.get('kernel_size'),
                                  padding=config.get('padding', 'same'),  # 預設 same
                                  activation=config.get('activation', 'relu'),
                                  input_shape=config.get('input_shape'),
                                  strides=config.get('strides')))
            # 建立池化層，池化大小=2x2，取最大值
            self.model.add(MaxPooling2D(pool_size=config.get('pool_size'), padding=config.get('padding', 'same')))

        # Dropout層隨機斷開輸入神經元，用於防止過度擬合，斷開比例 = drop_out_rate
        self.model.add(Dropout(self.drop_out_rate1))

        # Flatten層把多維的輸入一維化，常用在從卷積層到全連接層的過渡。
        self.model.add(Flatten())

        for config in self.dense_config_list:
            # 全連接層: unit 個 output
            self.model.add(Dense(config.get('unit'), activation='relu'))

        # Dropout層隨機斷開輸入神經元，用於防止過度擬合，斷開比例 = drop_out_rate
        self.model.add(Dropout(self.drop_out_rate2))

        # 使用 softmax activation function，將結果分類
        self.model.add(Dense(np.shape(self.y_test[1])[0], activation='softmax'))

        # 編譯: 選擇損失函數、優化方法及成效衡量方式
        self.model.compile(loss=self.loss,
                           optimizer="adam",
                           metrics=['accuracy'])

    def summary(self):
        print(self.model.summary())

    def _output_history(self, train_history, test_loss, test_accuracy, sensitivity, specificity):
        filename = f"model_result_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        accuracy = train_history.history['accuracy'][-1]
        val_accuracy = train_history.history['val_accuracy'][-1]
        loss = train_history.history['loss'][-1]
        val_loss = train_history.history['val_loss'][-1]
        with open(filename, "a") as my_file:
            my_file.write(f'{self.index+1},{accuracy},{val_accuracy},{loss},{val_loss},{test_loss},{test_accuracy},{sensitivity},{specificity}\n')
        print(f"===file output to {filename}===")

    def _get_sensitivity_specificity(self, predictions, y_test):
        y_test = np.argmax(y_test, axis=-1)
        predictions = np.argmax(predictions, axis=-1)

        c = confusion_matrix(y_test, predictions)
        # print(f'Confusion matrix:')
        # print(c)
        # print(type(c))
        # print('sensitivity = ', c[0, 0] / (c[0, 1] + c[0, 0]))
        # print('specificity = ', c[1, 1] / (c[1, 1] + c[1, 0]))

        dims = np.shape(c)
        if dims == (2,2):
            sensitivity = c[0, 0] / (c[0, 1] + c[0, 0])
            specificity = c[1, 1] / (c[1, 1] + c[1, 0])
        elif dims == (3,3):
            sensitivity = [
                    c[0, 0] / (c[0, 0] + c[0, 1] + c[0, 2]),
                    c[1, 1] / (c[1, 0] + c[1, 1] + c[1, 2]),
                    c[2, 2] / (c[2, 1] + c[2, 1] + c[2, 2]),
            ]
            specificity = [
                    (c[1, 1] + c[1, 2] + c[2, 1] + c[2, 2]) / (c[1, 1] + c[1, 2] + c[2, 1] + c[2, 2] + c[1,0] + c[2, 0]),
                    (c[0, 0] + c[0, 2] + c[2, 0] + c[2, 2]) / (c[0, 0] + c[0, 2] + c[2, 0] + c[2, 2] + c[0, 1] + c[2, 1]),
                    (c[0, 0] + c[0, 1] + c[1, 0] + c[1, 1]) / (c[0, 0] + c[0, 1] + c[1, 0] + c[1, 1] + c[0, 2] + c[1, 2]),
            ]

        return sensitivity, specificity, c

    def run(self, index, batch_size, epochs, conv2D_config_list, dense_config_list, drop_out_rate1, drop_out_rate2, enable_log=0):
        self.index = index
        self.batch_size = batch_size
        self.epochs = epochs
        self.conv2D_config_list = conv2D_config_list
        self.dense_config_list = dense_config_list
        self.drop_out_rate1 = drop_out_rate1
        self.drop_out_rate2 = drop_out_rate2
        # 編譯 model
        self._compile_model()
        # 進行訓練, 訓練過程會存在 train_history 變數中
        train_history = self.model.fit(self.x_train,
                                       self.y_train,
                                       batch_size=self.batch_size,
                                       epochs=self.epochs,
                                       validation_split=self.validation_split,
                                       verbose=enable_log)

        # 顯示損失函數、訓練成果(分數)
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        predictions = self.model.predict(self.x_test)
        sensitivity, specificity, confusion_matrix = self._get_sensitivity_specificity(predictions, self.y_test)
        test_loss = score[0]
        test_accuracy = score[1]
        last_accuracy = train_history.history['accuracy'][-1]
        last_loss = train_history.history['loss'][-1]
        print('Train accuracy:', last_accuracy)
        print('Train loss:', last_loss)
        print('Test accuracy:', test_accuracy)
        print('Test loss:', test_loss)
        print('Sensitivity:', sensitivity)
        print('Specificity:', specificity)
        print('confusion_matrix:', confusion_matrix)
        # self._output_history(train_history, test_loss, test_accuracy, sensitivity, specificity)

        K.clear_session()
        gc.collect()
        return {
            'model': self.model,
            'train_history': train_history, 
            'test_loss': test_loss, 
            'test_accuracy': test_accuracy,
            'sensitivity': sensitivity,
            'specificity': specificity,
            'confusion_matrix': confusion_matrix
            }


def show_train_history(train_history, type='accuracy'):
    if type == 'accuracy':
        plt.plot(train_history.history['accuracy'])
        plt.plot(train_history.history['val_accuracy'])
        plt.title('Train History')
        plt.xlabel('Epoch')
        plt.ylabel('accuracy')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.show()
    else:
        plt.plot(train_history.history['loss'])
        plt.plot(train_history.history['val_loss'])
        plt.title('Train History')
        plt.xlabel('Epoch')
        plt.ylabel('loss')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.show()

def show_train_history2(train_history, type='accuracy'):
    if type == 'accuracy':
        plt.plot(train_history['accuracy'])
        plt.plot(train_history['val_accuracy'])
        plt.title('Train History')
        plt.xlabel('Epoch')
        plt.ylabel('accuracy')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.show()
    else:
        plt.plot(train_history['loss'])
        plt.plot(train_history['val_loss'])
        plt.title('Train History')
        plt.xlabel('Epoch')
        plt.ylabel('loss')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.show()
