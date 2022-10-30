# This module’s main aim is to predict the presence of potholes in a certain number of images. The module loads the model and the images from the machine. 
# The images are again preprocessed in the same manner as in trainer module. The images are fed into the model and predictions and accuracies are printed on the 
# console.

import numpy as np
import cv2
import glob
from keras.models import Sequential
from keras.models import load_model
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.utils import np_utils

global size
size = 100
model = Sequential()
model = load_model('C:/Users/sample.h5')

nonPotholeTestImages = glob.glob("C:/Users/My Dataset/test/Plain/*.jpg")
test2 = [cv2.imread(img,0) for img in nonPotholeTestImages]

# train2[train2 != np.array(None)]
for i in range(0,len(test2)):
    test2[i] = cv2.resize(test2[i],(size,size))
temp4 = np.asarray(test2)


## load Testing data : potholes
potholeTestImages = glob.glob("C:/Users/My Dataset/test/Pothole/*.jpg")
test1 = [cv2.imread(img,0) for img in potholeTestImages]
# train2[train2 != np.array(None)]
for i in range(0,len(test1)):
    test1[i] = cv2.resize(test1[i],(size,size))
temp3 = np.asarray(test1)

X_test = []
X_test.extend(temp3)
X_test.extend(temp4)
X_test = np.asarray(X_test)
X_test = X_test.reshape(X_test.shape[0], size, size, 1)

y_test1 = np.ones([temp3.shape[0]],dtype = int)
y_test2 = np.zeros([temp4.shape[0]],dtype = int)

y_test = []
y_test.extend(y_test1)
y_test.extend(y_test2)
y_test = np.asarray(y_test)

y_test = np_utils.to_categorical(y_test)


tests = model.predict_classes(X_test)
for i in range(len(X_test)):
	print(">>> Predicted=%s" % (tests[i]))
