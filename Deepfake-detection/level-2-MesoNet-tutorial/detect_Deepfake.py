import numpy as np
from classifiers import *
from keras.preprocessing.image import ImageDataGenerator
# We don't need to use this 
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# load weights and declare instance of model
classifier = Meso4()
classifier.load('weights/Meso4_DF')

# load image generator

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
X, y = generator.next()
image_names = generator.filenames

print("The order of the files are (df is DeepFake):")
for name in image_names:
        print(name)

prob_real = classifier.predict(X)
print('Predicted probability of the image being real:', prob_real, '\nReal class :', y)