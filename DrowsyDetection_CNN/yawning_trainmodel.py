import os
from keras.preprocessing import image
import matplotlib.pyplot as plt 
import numpy as np
from keras.utils.np_utils import to_categorical
import random,shutil
from keras.models import Sequential
from keras.layers import Dropout,Conv2D,Flatten,Dense, MaxPooling2D, BatchNormalization
from keras.models import load_model
import matplotlib.pyplot as plt

def generator(dir, gen=image.ImageDataGenerator(rescale=1./255), shuffle=True,batch_size=1,target_size=(24,24),class_mode='categorical' ):

    return gen.flow_from_directory(dir,batch_size=batch_size,shuffle=shuffle,color_mode='grayscale',class_mode=class_mode,target_size=target_size)

def yawning_cnnmodel():
    print("[Info] Start to Training the CNN model for Yawning...")
    BS= 32
    TS=(24,24)
    train_batch= generator('dataset2/train',shuffle=True, batch_size=BS,target_size=TS)
    valid_batch= generator('dataset2/valid',shuffle=True, batch_size=BS,target_size=TS)
    SPE= len(train_batch.classes)//BS
    VS = len(valid_batch.classes)//BS
    #print(SPE,VS)


    # img,labels= next(train_batch)
    # print(img.shape)

    model = Sequential([
        Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(24,24,1)),
        MaxPooling2D(pool_size=(1,1)),
        Conv2D(32,(3,3),activation='relu'),
        MaxPooling2D(pool_size=(1,1)),
    #32 convolution filters used each of size 3x3
    #again
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(1,1)),

    #64 convolution filters used each of size 3x3
    #choose the best features via pooling

    #randomly turn neurons on and off to improve convergence
        Dropout(0.25),
    #flatten since too many dimensions, we only want a classification output
        Flatten(),
    #fully connected to get all relevant data
        Dense(128, activation='relu'),
    #one more dropout for convergence' sake :)
        Dropout(0.5),
    #output a softmax to squash the matrix into output probabilities
        Dense(2, activation='softmax')
    ])

    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

    history=model.fit_generator(train_batch, validation_data=valid_batch,epochs=15,steps_per_epoch=SPE ,validation_steps=VS)

    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)
    # Train and validation accuracy
    plt.plot(epochs, acc, 'b', label='Training accurarcy')
    plt.plot(epochs, val_acc, 'r', label='Validation accurarcy')
    plt.title('Training and Validation accurarcy for Yawning dataset')
    plt.legend()
    plt.figure()
    # Train and validation loss
    plt.plot(epochs, loss, 'b', label='Training loss')
    plt.plot(epochs, val_loss, 'r', label='Validation loss')
    plt.title('Training and Validation loss for Yawning dataset')
    plt.legend()
    plt.show()


    model.save('models/cnn_yawning.h5', overwrite=True)

    print("[Info] Training the CNN model for Yawning Completed.")
#yawning_cnnmodel()