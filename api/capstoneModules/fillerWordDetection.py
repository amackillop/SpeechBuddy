
# Importing required modules for using the model
from capstoneModules.audioFunctions import loadAudio, splitAudio
from capstoneModules.dataGenerator import createMelSpectrogram
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

import numpy as np
from os import listdir, remove

# GLOBAL VARIABLES
PATH = "C:/Users/Austin/Desktop/School/Capstone/"
IMG_HEIGHT = 300
IMG_WIDTH = 400
    # Generate the image data to be fed into the network from the spectrograms.
def detectFillers(classifier, fname):
    """Detect filler words in an audio file with a conv-net classifier object.

    # Arguments
        classifier: A classifier object loaded with `keras.models.load_model`
        or generated with `buildClassifier`
        fname: Name of the audio file to analyze

    # Returns
        None

    # Raises
        Not handled yet
    """
    # Nueral Network Model
    classifier = load_model(PATH + classifier)
    sample_length = 2 # Window length in seconds for input into the network, this model uses 4
    outFolder = "live/Images/"
    
    for file in listdir(PATH + outFolder):
        remove(PATH + "live/Images/" + file)
        
    signal = loadAudio(fname)
    samples = splitAudio(signal, sample_length)
    
    for i in range(len(samples)):
        createMelSpectrogram(samples[i,:]/1.0, "demo" + str(i) + ".wav", outFolder)
    
    live_datagen = ImageDataGenerator(rescale = 1./255)
    live_set = live_datagen.flow_from_directory('live',
                                            target_size = (IMG_HEIGHT, IMG_WIDTH),
                                            color_mode = "grayscale",
                                            batch_size = 32,
                                            class_mode = 'binary')
    
    # Output a count of all detected instances of the word
    print("Filler words detected: ", np.sum(classifier.predict_classes(live_set[0][0])))
    
    # Use this to see which clips contained the word
    for ind, x in enumerate(classifier.predict_classes(live_set[0][0])):
        print("Clip ", ind,": ", x[0])


    