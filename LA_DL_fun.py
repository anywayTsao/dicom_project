import os, time, socket, datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
from random import sample 
import random

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.utils import to_categorical


def sim(filen,type,scenario,sample):
    allimgs = []
    y = []
    if sample==1:
        sd=1
    elif sample==2:
        sd=15
    elif sample==3:
        sd=25
    elif sample==4:
        sd=65
    elif sample==5:
        sd=1000
    random.seed(sd)
    for ii in range(1, 4):
        if type==1:
            with open(file='D:/python/LA/image2S{}.pkl'.format(ii),mode='br') as inpf:
                imgs2 = pickle.load(inpf)
            with open(file='D:/python/LA/image4S{}.pkl'.format(ii),mode='br') as inpf:
                imgs4 = pickle.load(inpf)
        elif type==2:
            with open(file='D:/python/LA/image2SR{}.pkl'.format(ii),mode='br') as inpf:
                imgs2 = pickle.load(inpf)
            with open(file='D:/python/LA/image4SR{}.pkl'.format(ii),mode='br') as inpf:
                imgs4 = pickle.load(inpf)
        if ii==1: 
            imgs2=random.sample(imgs2,250)
            imgs4=random.sample(imgs4,250)
        elif ii==2: 
            imgs2 = imgs2 + random.sample(imgs2,40)
            imgs4 = imgs4 + random.sample(imgs4,40)
        elif ii==3:
            imgs2 = imgs2 + random.sample(imgs2,26)
            imgs4 = imgs4 + random.sample(imgs4,26)
        allimgs = allimgs + imgs2 + imgs4        
        y = y + list(np.ones([len(imgs2)+len(imgs4),])*(ii-1))     #相對應產生 y 的label, 必須是 0, 1, 2
    X = np.stack(allimgs)
    Y = np.stack(y)
    X_train, X_test, y_train, y_test = \
    train_test_split(X, Y, test_size=0.2, random_state=2100, shuffle=True)
    y_train_onehot = to_categorical(y_train)
    y_test_onehot = to_categorical(y_test)
    #找最大值與最小值進行標準化
    x_train_images=X_train.reshape(len(X_train),X_train.shape[1]*X_train.shape[2]).astype('float32') #資料型態 float32
    x_test_images=X_test.reshape(len(X_test),X_test.shape[1]*X_test.shape[2]).astype('float32')
    # 標準化
    x_train_normalize=(x_train_images-min(x_train_images[0,:]))/(max(x_train_images[0,:])-min(x_train_images[0,:]))
    X_test_normalize=(x_test_images-min(x_train_images[0,:]))/(max(x_train_images[0,:])-min(x_train_images[0,:]))
    x_train_images4D=x_train_normalize.reshape(len(X_train),X_train.shape[1],X_train.shape[2],1).astype('float32') #資料型態 float32
    x_test_images4D=X_test_normalize.reshape(len(X_test),X_test.shape[1],X_test.shape[2],1).astype('float32')
    y_train_OneHot=keras.utils.to_categorical(y_train)
    y_test_OneHot=keras.utils.to_categorical(y_test)
    if scenario==1:
        par={'filter1':128,'filter2':256,'strides':1,'kernel': 4,'height':128,'width':128,'dropout1':0.5,'dropout2': 0.5,'Neural':512}
    elif scenario==2:
        par={'filter1':128,'filter2':256,'strides':1,'kernel': 5,'height':128,'width':128,'dropout1':0.5,'dropout2': 0.5,'Neural':512}
    elif scenario==6:
        par={'filter1':128,'filter2':128,'strides':1,'kernel': 4,'height':128,'width':128,'dropout1':0.5,'dropout2': 0.5,'Neural':512}
    elif scenario==9:
        par={'filter1':128,'filter2':128,'strides':1,'kernel': 5,'height':128,'width':128,'dropout1':0.5,'dropout2': 0.5,'Neural':512}
    rep=50
    test_acc = np.zeros((rep,9))
    train_acc = np.zeros((rep,9))
    acc = np.zeros((rep,2))
    outf = open(r'D:/python/LA/final/LA_result_' + filen + '.txt','at') #append text 
    for i in range(0, rep):
        par1={'Validation': 0.2, 'epoch': 40, 'Batch': 100}
        result=DL_fun1(par,par1,x_train_images4D,y_train,x_test_images4D,y_test)
        h1_test=np.array(result['Test_acc'].iloc[0,0:3])
        h2_test=np.array(result['Test_acc'].iloc[1,0:3])
        h3_test=np.array(result['Test_acc'].iloc[2,0:3])
        test_acc[i,]=np.hstack((h1_test,h2_test,h3_test))
        train_acc[i,]=np.hstack((np.array(result['Train_acc'].iloc[0,0:3]),np.array(result['Train_acc'].iloc[1,0:3]),np.array(result['Train_acc'].iloc[2,0:3])))
        acc[i,]=np.hstack((result['History'].history['accuracy'][par1['epoch']-1],result['History'].history['val_accuracy'][par1['epoch']-1]))
        all_result={'Test': test_acc, 'Train': train_acc, 'Acc': acc}
        allresult=np.hstack((train_acc[i,],test_acc[i,],acc[i,])).reshape([1,20])
        np.savetxt(outf, allresult, delimiter=",")
        outf.flush()
    outf.close()

def DL_fun1(par,par1,x_train,y_train,x_test,y_test):
    nf=par['filter1']
    nf1=par['filter2']
    ks=par['kernel']
    hs=par['height']
    ws=par['width']
    dr1=par['dropout1']
    dr2=par['dropout2']
    nn=par['Neural']
    vsr=par1['Validation']
    epn=par1['epoch']
    bs=par1['Batch']
    y_train_onehot = to_categorical(y_train)
    y_test_onehot = to_categorical(y_test)
    model = Sequential()
    model.add(Conv2D(filters=nf,kernel_size=(ks,ks),strides=(par['strides'],par['strides']),padding='same',input_shape=(hs,ws,1),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2))) 
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Conv2D(filters=nf1,kernel_size=(ks,ks),strides=(par['strides'],par['strides']),padding='same',input_shape=(hs,ws,1),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))   
    model.add(Dropout(dr1))
    model.add(Flatten())
    model.add(Dense(nn, activation='relu'))
    model.add(Dropout(dr2))
    model.add(Dense(3,activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    train_history=model.fit(x=x_train,
                            y=y_train_onehot,
                            validation_split=vsr,
                            epochs=epn,
                            batch_size=bs,
                            verbose=2)
    scores=model.evaluate(x=x_test,y=y_test_onehot)
    train_pred=model.predict_classes(x=x_train)
    train_acc=pd.crosstab(y_train,train_pred,rownames=['Observed'],colnames=['Predicted'])
    test_pred=model.predict_classes(x=x_test)
    test_acc=pd.crosstab(y_test,test_pred,rownames=['Observed'],colnames=['Predicted'])
    result={'History':train_history, 'Score': scores, 'Train_P': train_pred, 'Train_acc': train_acc, 'Test_P': test_pred, 'Test_acc': test_acc}
    return result

def DL_fun2(par,par1,x_train,y_train,x_test,y_test):
    nf=par['filter1']
    nf1=par['filter2']
    nf3=par['filter3']
    ks=par['kernel']
    hs=par['height']
    ws=par['width']
    dr1=par['dropout1']
    dr2=par['dropout2']
    nn=par['Neural']
    vsr=par1['Validation']
    epn=par1['epoch']
    bs=par1['Batch']
    y_train_onehot = to_categorical(y_train)
    y_test_onehot = to_categorical(y_test)
    model = Sequential()
    model.add(Conv2D(filters=nf,kernel_size=(ks,ks),padding='same',input_shape=(hs,ws,1),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(dr1))
    model.add(Conv2D(filters=nf1,kernel_size=(ks,ks),padding='same',input_shape=(hs,ws,1),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))   
    model.add(Conv2D(filters=par['filter3'],kernel_size=(ks,ks),padding='same',input_shape=(hs,ws,1),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))   
    model.add(Flatten())
    model.add(Dense(nn, activation='relu'))
    model.add(Dropout(dr2))
    model.add(Dense(3,activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    train_history=model.fit(x=x_train,
                            y=y_train_onehot,
                            validation_split=vsr,
                            epochs=epn,
                            batch_size=bs,
                            verbose=2)
    scores=model.evaluate(x=x_test,y=y_test_onehot)
    train_pred=model.predict_classes(x=x_train)
    train_acc=pd.crosstab(y_train,train_pred,rownames=['Observed'],colnames=['Predicted'])
    test_pred=model.predict_classes(x=x_test)
    test_acc=pd.crosstab(y_test,test_pred,rownames=['Observed'],colnames=['Predicted'])
    result={'History':train_history, 'Score': scores, 'Train_P': train_pred, 'Train_acc': train_acc, 'Test_P': test_pred, 'Test_acc': test_acc}
    return result
