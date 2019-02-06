# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 16:33:37 2019

@author: Anastasija
"""
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import MaxPooling2D
from keras.layers import Dropout
from keras.layers import Flatten

(x_train, y_train), (x_test, y_test) = mnist.load_data()          


def reshapeData(data,vectorDimension):
  dataReshaped = data.reshape(data.shape[0],28,28,1)        
  return dataReshaped

def prepareData(data):
    data = data.astype('float32')
    data = data/255
    return data

def toCategoricalMatrix(data):
    dataCat = np_utils.to_categorical(data)
    return dataCat

def ucitajModel():
    model = initModel();
    model.load_weights("weights.h5")
    return model

def initModel():
    model = Sequential()
    model.add(Conv2D(30,  kernel_size=(5, 5), activation='relu',input_shape=(28,28,1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(15, kernel_size=(3, 3), activation='relu'))
    
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
   
    model.add(Flatten())
    
    model.add(Dense(128, activation='relu'))
    model.add(Dense(50, activation='relu'))    
    model.add(Dense(10, activation='softmax'))
   
    #Compile model    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

x_train = reshapeData(x_train,x_train[0].shape[0] * x_train[0].shape[1])  
x_test = reshapeData(x_test,x_test[0].shape[0] * x_test[0].shape[1])  
x_train = prepareData(x_train)
x_test = prepareData(x_test) 
y_train =toCategoricalMatrix(y_train)
y_test =toCategoricalMatrix(y_test)

 
#model = initModel()
#print(model.summary())    
#history = model.fit(x_train,y_train,32,epochs = 10,validation_split = 0.25)
#scores = model.evaluate(x_test, y_test, verbose=1)
#print("Baseline Error: %.2f%%" % (100-scores[1]*100))
#model.save_weights("weights.h5")
    
    