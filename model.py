from data_processor import get_note_encodings, process_data, vector_to_MIDI, one_hot_to_int
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.callbacks import ModelCheckpoint

import os.path

import sys

TRAIN_PATH = "./Pop_Music_Midi/train"
TEST_PATH = "./Pop_Music_Midi/test"
ALL_PATH = "./Pop_Music_Midi/all"
MODEL_FILE = "weights.hdf5"

def get_model(inputs, num_classes): #model from Sigurður Skúli
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(inputs.shape[1], inputs.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    return model

def train(model, trainXs, trainYs, epochs=200):
    model.fit(trainXs, trainYs, epochs=epochs, batch_size=64)
    model.save(MODEL_FILE)

def test(model, testXs, testYs):
    loss = model.evaluate(testXs, testYs)
    print("loss on test:") #TODO remove
    print(loss) #TODO remove


if __name__ == '__main__':

    if (len(sys.argv) == 1 or sys.argv[1].lower() == 'generate' or sys.argv[1].lower() == 'gen'):
        #????
        print("idk") #TODO write generate code!!
        # vector_to_MIDI(ys, decodingDict) #check test_output.midi for result

    elif (sys.argv[1].lower() == 'train' or sys.argv[1].lower() == 'retrain'):
        epochs = None
        if (len(sys.argv) >= 3):
            epochs = int(sys.argv[2])

        distinct_notes, encodingDict, decodingDict = get_note_encodings(ALL_PATH)
        trainXs, trainYs = process_data(TRAIN_PATH, distinct_notes, encodingDict)
        
        model = None
        if (sys.argv[1].lower() == 'retrain' or not os.path.isfile(MODEL_FILE)):        
            model = get_model(trainXs, distinct_notes)
        else:
            model = keras.models.load_model(MODEL_FILE)

        if (epochs):
            train(model, trainXs, trainYs, epochs)
        else:
            train(model, trainXs, trainYs)

    elif (sys.argv[1].lower() == 'test'):
        if (not os.path.isfile(MODEL_FILE)):
            print('Test Error: model not found. Please run training to generate weights in ' + MODEL_FILE)
        model = keras.models.load_model(MODEL_FILE)
        distinct_notes, encodingDict, decodingDict = get_note_encodings(ALL_PATH)
        testXs, testYs = process_data(TEST_PATH, distinct_notes, encodingDict)
        
        test(model, testXs, testYs)

