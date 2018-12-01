from data_processor import load_dict, get_encoding_dict, get_decoding_dict, process_data, vector_to_MIDI, one_hot_to_int, create_midi
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.utils import np_utils

import numpy as np
import os.path
import sys
import random


TRAIN_PATH = "./Pop_Music_Midi/train"
TEST_PATH = "./Pop_Music_Midi/test"
ALL_PATH = "./Pop_Music_Midi/all"
MODEL_FILE = "weights.hdf5"
DEFAULT_SONG_LENGTH = 100
SEQUENCE_LENGTH = 40

def get_model(inputs, num_classes): #model from Sigurður Skúli
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(inputs.shape[1], inputs.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.5))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(512))
    model.add(Dense(256))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    return model

def train(model, trainXs, trainYs, epochs=200):
    model.fit(trainXs, trainYs, epochs=epochs, batch_size=64)
    model.save(MODEL_FILE)

def test(model, testXs, testYs):
    loss = model.evaluate(testXs, testYs)
    print("Loss on test dataset: " + str(loss))

def generate(model, seed_sequence, distinct_notes, length):
    sequence = seed_sequence
    output = []
    
    for i in range(length):
        resized_sequence = np.reshape(sequence, (1, SEQUENCE_LENGTH, 1))
        resized_sequence = resized_sequence / float(distinct_notes)
        predicted_note_vector = model.predict(resized_sequence)
        predicted_note = np.argmax(predicted_note_vector)
        sequence = sequence[1:len(sequence)]
        sequence.append(predicted_note)
        output.append(predicted_note)
    return output


def get_random_seed(encodingDict): #TODO maybe don't use random??
    sequence = []
    for i in range(SEQUENCE_LENGTH):
        sequence.append(random.randint(0, len(encodingDict)))
    
    return sequence

def closest_in_training(output_sequence, training_Xs, distinct_notes):
    closest = None
    min_dist = None
    for x_sequence in training_Xs:
        curr_dist = distance.euclidean(x_sequence*distinct_notes, output_sequence)
        if min_dist == None or curr_dist < min_dist:
            min_dist = curr_dist
            closest = x_sequence*distinct_notes
    
    return closes, min_dist

if __name__ == '__main__':

    if (len(sys.argv) == 1 or sys.argv[1].lower() == 'generate' or sys.argv[1].lower() == 'gen'):
        song_length = DEFAULT_SONG_LENGTH
        if (len(sys.argv) >= 3):
            song_length = int(sys.argv[2])
        
        if (not os.path.isfile(MODEL_FILE)):
            print('Generate Error: model not found. Please run training (model.py train) to generate weights in ' + MODEL_FILE)

        model = keras.models.load_model(MODEL_FILE) 
        encodingDict = load_dict()
        decodingDict = get_decoding_dict(encodingDict)
        distinct_notes = len(encodingDict)

        seed_sequence = get_random_seed(encodingDict) #temp TODO
        print("seed sequence: ", seed_sequence)
        output = generate(model, seed_sequence, distinct_notes, song_length)
        print("Generated song: ", [decodingDict[char] for char in output])
        print("Song stored in test_output.midi.")
        vector_to_MIDI(output, decodingDict)

        closest, dist = closest_in_training(output_sequence, training_Xs, distinct_notes)
        print("Most similar training song", closest, "Distance", dist)

    elif (sys.argv[1].lower() == 'train' or sys.argv[1].lower() == 'retrain'):
        epochs = None
        if (len(sys.argv) >= 3):
            epochs = int(sys.argv[2])

        model = None
        if (sys.argv[1].lower() == 'retrain' or not os.path.isfile(MODEL_FILE)):
            distinct_notes, encodingDict = get_encoding_dict(ALL_PATH)
            trainXs, trainYs = process_data(TRAIN_PATH, distinct_notes, encodingDict, SEQUENCE_LENGTH)
            model = get_model(trainXs, distinct_notes)
            print(model.summary())
        else:
            encodingDict = load_dict()
            distinct_notes = len(encodingDict)
            trainXs, trainYs = process_data(TRAIN_PATH, distinct_notes, encodingDict, SEQUENCE_LENGTH)
            model = keras.models.load_model(MODEL_FILE)
            print(model.summary())

        if (epochs):
            train(model, trainXs, trainYs, epochs)
        else:
            train(model, trainXs, trainYs)

    elif (sys.argv[1].lower() == 'test'):
        if (not os.path.isfile(MODEL_FILE)):
            print('Test Error: model not found. Please run training (model.py train) to generate weights in ' + MODEL_FILE)

        model = keras.models.load_model(MODEL_FILE)
        print(model.summary())
        encodingDict = load_dict()
        distinct_notes = len(encodingDict)
        testXs, testYs = process_data(TEST_PATH, distinct_notes, encodingDict, SEQUENCE_LENGTH)
 
        test(model, testXs, testYs)

