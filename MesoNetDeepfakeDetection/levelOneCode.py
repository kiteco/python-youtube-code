import tensorflow
import keras
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

# Inception ResNetV2 model 

googleNet_model = InceptionResNetV2(include_top=False, weights='imagenet', input_shape=input_shape)
# Specifying that the model is trainable
googleNet_model.trainable = True
# Sequential neural net
model = Sequential()
model.add(googleNet_model)
model.add(GlobalAveragePooling2D())
# Modify for a 2 class output
model.add(Dense(units=2, activation='softmax'))
# Compiling with the standard Adam optimizer 
model.compile(loss='binary_crossentropy',
              optimizer=optimizers.Adam(lr=1e-5, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False),
              metrics=['accuracy'])
model.summary()

EPOCHS = 20
BATCH_SIZE = 100
# Fitting model
history = model.fit(X_train, Y_train, batch_size = BATCH_SIZE, epochs = EPOCHS, validation_data = (X_val, Y_val), verbose = 1)