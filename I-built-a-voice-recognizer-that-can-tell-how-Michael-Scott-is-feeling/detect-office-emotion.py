"""
Part one: loading the model
"""
# Imports
import os
from tensorflow import keras
from keras.models import model_from_json
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Read in the JSON file
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

# Load the model from JSON 
loaded_model = model_from_json(loaded_model_json)

# Load weights into new model
loaded_model.load_weights('saved_models/Emotion_Voice_Detection_Model.h5')
print('Loaded model from disk')
o = keras.optimizers.RMSprop(lr = 0.00001, decay = 1e-6)
# evaluate loaded model on test data
loaded_model.compile(loss ='categorical_crossentropy', optimizer = o, metrics = ['accuracy'])

"""
Part two: reading in the audio files
"""

# Method for reading in the audio files and extracting features
def read_audio_files(dir):
    for audiofile in os.listdir(dir):
        # Load file using librosa
         X, sample_rate = librosa.load()

# Method for 




    



