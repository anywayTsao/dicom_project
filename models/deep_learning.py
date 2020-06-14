
par1={
    'Validation': 0.2, 
    'epoch': 40, 
    'Batch': 100
}
param_dict = {
    'filter1':128,
    'filter2':256,
    'strides':1,
    'kernel': 4,
    'height':128,
    'width':128,
    'dropout1':0.5,
    'dropout2':0.5,
    'Neural':512
}

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
    result={'History':train_history, 'Score': scores}
    return result