# -*- coding: utf-8 -*-
"""Multiclass MRI Classifiation

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BpCFIpPeEXPE0jdNCTQB9NjfmcqYJx52
"""

!pip install tflearn
import cv2
import glob
import tensorflow as tf
import os
import numpy as np
from tensorflow.keras import datasets, layers, models
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from skimage.io import imread_collection
from keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from sklearn.utils import shuffle
from google.colab.patches import cv2_imshow

from google.colab import drive
drive.mount('/content/drive')

!unzip /content/drive/MyDrive/Training.zip

path = "/content/content/8020"
IMG_SIZE=256
MODEL_NAME="Multiclass_BrainTumor"

def load_images_folder(path,l,Data,label):
    for filename in os.listdir(path):
        img = cv2.imread(os.path.join(path,filename))
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img,(IMG_SIZE,IMG_SIZE),interpolation=cv2.INTER_LINEAR)
        img = img.reshape(img.shape+(1,)) 
        if img is not None:
            Data.append(img)
            label.append(l)

def load_data(path2):
  fullpath=path+path2
  Data=[]
  label=[]
  load_images_folder(fullpath+"/glioma_tumor",np.array([0]),Data,label)
  load_images_folder(fullpath+"/meningioma_tumor",np.array([1]),Data,label)
  load_images_folder(fullpath+"/pituitary_tumor",np.array([2]),Data,label)

  Data=np.array(Data)
  label=np.array(label)
  return Data,label

Train_Data,Train_Label=load_data("/Training")
Test_Data,Test_Label=load_data("/Testing")
Val_Data,Val_Label=load_data("/Validation")

Train_Data,Train_Label=shuffle(Train_Data,Train_Label,random_state=10)

Train_Label = keras.utils.to_categorical(Train_Label, 3)
Test_Label = keras.utils.to_categorical(Test_Label, 3)
Val_Label = keras.utils.to_categorical(Val_Label, 3)

print(Train_Data.shape)
cv2_imshow(Train_Data[18])
 
print(Train_Label[0])

import keras.backend as K
K.clear_session()

model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(256,256,1)))
layers.BatchNormalization()
model.add(layers.Conv2D(64, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(96, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.Conv2D(128, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(160, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.Conv2D(192, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(224, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.Conv2D(256, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(288, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.Conv2D(320, (3,3), activation='relu'))
layers.BatchNormalization()
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(64))
model.add(layers.Dense(3,activation='softmax'))
opt = keras.optimizers.Adagrad(learning_rate=0.003)
model.compile(opt,loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),metrics=['accuracy'])

history = model.fit(Train_Data,Train_Label, epochs=10,batch_size=16,validation_data=(Val_Data, Val_Label))

import matplotlib.pyplot as plt 
plt.plot(history.history['acc'], label='accuracy')
plt.plot(history.history['val_acc'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(Test_Data,Test_Label, verbose=2)
print(test_acc)

loss_train = history.history['loss']
loss_val = history.history['val_loss']
epochs = range(1,35)
plt.plot(loss_train, 'g', label='Training loss')
plt.plot(loss_val, 'b', label='validation loss')
plt.title('Training and Validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

model.save("smulti967.tfl")

def main_run(img):
 from keras.models import load_model
 model = load_model('/content/smulti967.tfl')
 IMG_SIZE=256
 img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
 img = np.expand_dims(img, axis=0)
 img = np.array(img).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
 prediction=[]
 prediction = model.predict(img)
 print(prediction)
 if(prediction[0][0]>prediction[0][1] and prediction[0][0]>prediction[0][2]):
  print("glioma_tumor")
 elif(prediction[0][1]>prediction[0][0] and prediction[0][1]>prediction[0][2]):
  print("meningioma_tumor")
 else:
  print("pituitary_tumor")

from keras.models import load_model
model = load_model('/content/MulticlassModel.tfl')

y_predict=model.predict(Test_Data)

print(y_predict.shape)
print(y_predict[2][2])

classes_x=np.argmax(y_predict,axis=1)

y_predict = y_predict[:, 0]

for i in range(len(y_predict)):
  if(y_predict[i][0]>y_predict[i][1] and y_predict[i][0]>y_predict[i][2]):
     y_predict[i]=[1,0,0]
  elif(y_predict[i][1]>y_predict[i][0] and y_predict[i][1]>y_predict[i][2]):
     y_predict[i]=[0,1,0]
  else:
    y_predict[i]=[0,0,1]

print(y_predict[2])

print(classes_x[44])
print(Test_Label[44])

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix

matrix = multilabel_confusion_matrix(Test_Label, classes_x,labels=[0,1,2])
print(matrix)

glioma=np.flip(matrix[0]) 
menin=np.flip(matrix[1]) 
pitut=np.flip(matrix[2])

print(glioma)
acc = (glioma[0][0] + glioma[-1][-1]) / np.sum(glioma)
prec=(glioma[0][0]/(glioma[0][0]+glioma[1][0]))
recall=(glioma[0][0]/(glioma[0][0]+glioma[0][1]))
sp=(glioma[1][1]/(glioma[1][1]+glioma[1][0]))
F1  = 2 * (prec * recall) / (prec + recall)
print(acc)
print(prec)
print(recall)
print(sp)
print(F1)

print(menin)
acc = (menin[0][0] + menin[-1][-1]) / np.sum(menin)
prec=(menin[0][0]/(menin[0][0]+menin[1][0]))
recall=(menin[0][0]/(menin[0][0]+menin[0][1]))
sp=(menin[1][1]/(menin[1][1]+menin[1][0]))
F1  = 2 * (prec * recall) / (prec + recall)
print(acc)
print(prec)
print(recall)
print(sp)
print(F1)

print(pitut)
acc = (pitut[0][0] + pitut[-1][-1]) / np.sum(pitut)
print(acc)
prec=(pitut[0][0]/(pitut[0][0]+pitut[1][0]))
print(prec)
recall=(pitut[0][0]/(pitut[0][0]+pitut[0][1]))
sp=(pitut[1][1]/(pitut[1][1]+pitut[1][0]))
F1  = 2 * (prec * recall) / (prec + recall)
print(recall)
print(sp)
print(F1)