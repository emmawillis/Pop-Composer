
from music21 import converter, instrument, note, chord
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

from os import listdir
from os.path import isfile, join

path = "./Pop_Music_Midi"
files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
sequence_length = 40 #100
DEBUG = True

def process_data():
    notes, maxNotes, minNotes, meanNotes = get_notes()

    if DEBUG: print("\nRESULTS:\nThere are an average of " + str(meanNotes) + " notes per song. The min number of notes is " + str(minNotes) + " and the max is " + str(maxNotes) + ".")
    if DEBUG: print("Setting sequence length to " + str(sequence_length))

    n_vocab = len(set(notes))

    note_values = sorted(set(item for item in notes))

    notes_as_ints = dict((note, number) for number, note in enumerate(note_values))
    
    if DEBUG: print ("There are " + str(n_vocab) + " distinct notes in the training dataset, with dictionary mappings: ")
    if DEBUG: print (notes_as_ints)

    training_Xs = []
    training_Ys = []

    print ("TEST " + str(len(notes)))
    for i in range(len(notes) - sequence_length):
        sequence_xs = notes[i: i + sequence_length] #note 0 to 39 of first song = input
        sequence_y = notes[i + sequence_length] #note 40 = output 
        training_Xs.append([notes_as_ints[char] for char in sequence_xs])
        training_Ys.append(notes_as_ints[sequence_y])

    num_patterns = len(training_Xs)
    if DEBUG: print("Using sequence length of " + str(sequence_length) + ", " + str(num_patterns) + " input-output pairs were generated.")
    # reshape the input into a format compatible with LSTM layers
    training_Xs = numpy.reshape(training_Xs, (num_patterns, sequence_length, 1))
    if DEBUG: print("Example training sample before normalization: \ninput: \n" + str(training_Xs[0]) + "\noutput:\n " + str(training_Ys[0]))
    
    # normalize input
    training_Xs = training_Xs / float(n_vocab)
    training_Ys = np_utils.to_categorical(training_Ys)
    if DEBUG: print("Example training sample after normalization: \ninput: \n" + str(training_Xs[0]) + "\noutput:\n " + str(training_Ys[0]))

    return (notes_as_ints, training_Xs, training_Ys)


def get_notes(): #this function written by Sigurður Skúli
    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    notes = []
    notes_per_song = []

    for file in files:
        midi = converter.parse(file)

        if DEBUG: print("Parsing %s" % file)

        notes_to_parse = None

        try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        notes_per_song.append(len(notes_to_parse))

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
        
    
    return (notes, max(notes_per_song), min(notes_per_song), int(numpy.mean(notes_per_song)))



if __name__ == '__main__':
    parsingDict, inputs, outputs = process_data()

    