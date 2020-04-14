import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import numpy as np
import skimage
from skimage.io import imread, imshow
from skimage.transform import resize
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from keras.layers import Dense
from keras import Model
from keras.applications.xception import Xception

def readImgs(path):
    imgs = []
    i = 0
    for filename in os.listdir(path): 
        i += 1
        if i == 251:
            break
        if filename.endswith('.jpg'):
            img = imread(os.path.join(path,filename))
            resized = resize(img, (256, 256), anti_aliasing=True)
            imgs.append(resized)
    return imgs

train_df_path = 'deepfake_database/deepfake_database/train:test/df'
train_real_path = 'deepfake_database/deepfake_database/train:test/real'
deepfakes_train = readImgs(train_df_path)
real_train = readImgs(train_real_path)

y_train = [0]*250 + [1]*250
X_train = deepfakes_train + real_train

y_train = np.array(y_train)
X_train = np.array(X_train)


conv_base = Xception(include_top = False, weights = None, pooling = 'avg', input_shape = (256, 256, 3))

output_layer =  Dense(activation = 'sigmoid')(conv_base.output)

modified_classifier = Model(conv_base.input, output_layer)

modified_classifier.compile(optimizer = 'Adam', loss = 'binary_crossentropy')

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

prob_real_Xception = Xception.predict(X_test)



actual_pred_Xception = convertToActual(prob_real_Xception)
print(prob_real_Xception.shape)
print('Predicted probability of the image being real Xception:', prob_real_Xception,'\nPredicted class :', actual_pred_Xception)
print('Deepfake detection accuracy is:', computeAccuracy(actual_pred_Xception, y_test), '%')
