import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

import tensorflow as tf
from keras.models import Model
from keras.optimizers import Adam
from keras.layers import Input, Dense, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Dropout, Reshape, Concatenate, LeakyReLU

def init_model(img_width): 
    x = Input(shape = (img_width, img_width, 3))
    x1 = Conv2D(8, (3, 3), padding='same', activation = 'relu')(x)
    x1 = BatchNormalization()(x1)
    x1 = MaxPooling2D(pool_size=(2, 2), padding='same')(x1)
        
    x2 = Conv2D(8, (5, 5), padding='same', activation = 'relu')(x1)
    x2 = BatchNormalization()(x2)
    x2 = MaxPooling2D(pool_size=(2, 2), padding='same')(x2)
        
    x3 = Conv2D(16, (5, 5), padding='same', activation = 'relu')(x2)
    x3 = BatchNormalization()(x3)
    x3 = MaxPooling2D(pool_size=(2, 2), padding='same')(x3)
        
    x4 = Conv2D(16, (5, 5), padding='same', activation = 'relu')(x3)
    x4 = BatchNormalization()(x4)
    x4 = MaxPooling2D(pool_size=(4, 4), padding='same')(x4)
        
    y = Flatten()(x4)
    y = Dropout(0.5)(y)
    y = Dense(16)(y)
    y = LeakyReLU(alpha=0.1)(y)
    y = Dropout(0.5)(y)
    y = Dense(1, activation = 'sigmoid')(y)
    return Model(inputs = x, outputs = y)

Meso4 = init_model(256)

opt = Adam(lr = 0.001)
Meso4.compile(optimizer = opt, loss = 'binary_crossentropy')
Meso4.load_weights('weights/Meso4_DF')

def convertToActual(probs):
    return np.round(probs)

def computeAccuracy(pred, real):
    cnt = 0
    for i in range(len(pred)):
        if pred[i] == real[i]:
            cnt += 1
    return cnt/len(pred)*100

# Testing on our data 
dataGenerator = ImageDataGenerator(rescale=1./255)
generator = dataGenerator.flow_from_directory(
        'extracted_imgs',
        shuffle=False,
        target_size=(256, 256),
        batch_size=5,
        class_mode='binary',
        subset='training')

# Predict 
# y: Deepfake, Deepfake, Deepfake, real, real 
X_test, y_test = generator.next()
image_names = generator.filenames

print("The order of the files are (df is DeepFake):")
for name in image_names:
        print(name)
prob_real_meso = Meso4.predict(X_test)

actual_pred_Meso = convertToActual(prob_real_meso)
print('Predicted probability of the image being real Meso:', prob_real_meso,'\nPredicted class :', actual_pred_Meso)
print('Deepfake detection accuracy is:', computeAccuracy(actual_pred_Meso, y_test), '%')
