import sys
from music21 import converter, instrument, note, chord, stream
from scipy.spatial import distance
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy as np
import math
import pickle


def closest_in_training(sequence, path, encodingDict):
    closest = None
    min_dist = None

    # Note: commented out code was used to generate the average song sequence 
    # sum = []
    # count = 0

    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    for file in files:
        midi = converter.parse(file)

        notes_to_parse = None

        try: # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        notes = []
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

        notes = [encodingDict[x] for x in notes]

        if len(notes) == len(sequence):
            curr_dist = distance.euclidean(notes, sequence)
            temp = notes
        elif len(notes) < len(sequence):
            temp = np.tile(notes, math.ceil(len(sequence)/len(notes)))
            temp = temp[0:len(sequence)] #repeat shorter training sequences to make them same length as output sequence
            curr_dist = distance.euclidean(temp, sequence)
        elif (len(notes) > len(sequence)):
            all_dists = []
            for i in range(len(notes) - len(sequence)):
                temp = notes[i: i + len(sequence)] 
                all_dists.append(distance.euclidean(temp, sequence))
            curr_dist = max(all_dists)

        # if len(sum) == 0: sum = temp
        # else: sum = np.add(sum, temp)
        # count = count + 1

        if min_dist == None or curr_dist < min_dist:
            min_dist = curr_dist
            closest = temp
            closest_name = file
        
    # sum = sum/count
    # sum = [int(x) for x in sum]

    # with open("avg_song.pkl", 'wb') as f:
    #     pickle.dump(sum, f, pickle.HIGHEST_PROTOCOL)

    return closest_name, closest, min_dist


text_file = open("graphme.txt", "r")
read = text_file.read() 
sequences = read.split('//')
for i, sequence in enumerate(sequences):
    sequence_name = sys.argv[1] + '-' + str(i+1)
    sequence = sequence.split(',')
    sequence = [x.replace("\'", "").replace("\n","").replace(' ', '') for x in sequence]
    
    with open("../note_dict.pkl", 'rb') as f:
            encodingDict = pickle.load(f)
    distinct_notes = len(encodingDict)

    sequence = [encodingDict[x] for x in sequence]

    closest_name, closest, dist = closest_in_training(sequence, "../Pop_Music_Midi/train", encodingDict)
    print("Closest song to", sequence_name, "is", closest_name, "with distance", dist)
    plt.plot(closest, color="blue", label='Closest Training Song = Blue')
    if (len(closest) < len(sequence)):
        plt.plot(sequence[0:len(closest)], color="orange", label='Generated Song = Orange')
    else:
        plt.plot(sequence, color="orange", label='Generated Song = Orange')

    plt.title(sequence_name + ' vs. ' + closest_name.split('\\')[1])
    plt.ylabel('Value In Dictionary')
    plt.xlabel('Position in sequence')
    plt.legend()
    # plt.show()
    plt.savefig(sequence_name+'-'+str(round(dist))+'.png')
    plt.clf()
    plt.cla()
    plt.close()


#Note: this code is kinda iffy but loading the sequences from the midi files
#themselves was causing problems because music21 would interpret the notes differently
#or miss notes
#so to get the exact sequences that were generated i had to use the 
#sequences that were outputted during the generation process and pass them in
#as strings
#So to run this code you need to paste the sequence into graphme.txt and then it'll
#read in that song, find the closest to it in the training set, graph them over 
#each other and save the result

#i also had problems with naming, so you need to pass in the prefix you want for the file
#names as a command line argument

# so if you want to graph 3 songs and have them saved to output-1.png, output-2.png, output-3.png
#you could set up graphme.txt as:
# 'E4', 'D4', '0.2.7', 'D4', 'D3', '9.0.4', 'A2', 'E5', '9.0.4', 'G4', 'G4', '7.11.2', 'F2', 'C5', '7.11.2', 'A2', 'G2', '6.9.0', 'F2', 'F5', 'E4', '7.11.2', 'F2', 'E4', '7.11.2', 'F2', 'D5', 'D4', '9.0.4', 'C4', 'C4', '9.0.4', 'F2', 'C5', 'D4', '9.0.4', 'A2', 'F2', 'E5', '9.0.4', 'A5', 'D4', '5.9.0', 'F2', 'F5', 'A5', 'F5', '5.9.0', 'E6', 'F5', '5.9.0', 'A5', 'C6', 'D6', '5.9.0', 'A5', 'C6', '0.4.7', 'C3', 'G5', 'A5', 'C5', '0.4.7', 'C6', 'G5', '0.4.7', 'A5', 'C5', 'A5', '0.4.7', 'C6', 'C6', '0.4.7', 'C3', 'G5', '0.4.7', 'E6', 'C3', 'D6', '7.11.2', 'G2', 'C4', '7.11.2', 'G5', 'A3', '7.11.2', 'G2', 'B3', '7.11.2', 'G2', 'B3', '7.11.2', 'G2', 'B3', '7.11.2', 'G2', 'C4', '7.11.2', 'G2', '5.9.0'
# //
# '9.0.4', 'A2', 'A3', 'A4', '9.0.4', 'A2', 'A2', 'E5', 'A2', 'A2', 'D5', '5.9.0', 'C3', 'D5', 'A5', 'C4', 'D5', '2.5.9', 'G2', 'D5', 'A4', '7.11.2', 'G2', 'G4', '7.11.2', 'G2', 'A4', '7.11.2', 'C5', 'G2', 'G4', '0.4.7', 'C3', 'E3', '0.4.7', 'G3', 'C3', 'E3', '7.11.2', 'D3', 'C4', '7.11.2', 'E3', 'C4', '7.11.2', 'G2', 'C5', '7.11.2', 'G2', 'C4', '7.11.2', 'G2', 'F3', '2.5.9', 'D3', '2.5.9', 'D3', 'E4', '2.5.9', 'D3', '2.5.9', 'D3', 'E4', '5.9.0', 'F2', '5.9.0', 'F2', 'E4', '5.9.0', 'F2', 'D4', '0.4.7', 'C3', '0.4.7', 'D3', '0.4.7', 'C3', 'E4', 'C4', '0.4.7', 'D4', 'C3', '7.11.2', 'G2', '7.11.2', 'G2', 'D4', '7.11.2', 'G2', 'C4', 'E4', '7.11.2', 'C4', 'G2', '9.0.4', 'A2', '9.0.4', 'A2', '9.0.4', 'A2'
# //
# '7.11.2', 'G2', 'G4', 'E4', '7.11.2', 'G2', 'G4', '7.11.2', 'G2', 'G4', 'E4', '7.11.2', 'G2', 'F4', 'E4', '7.11.2', 'D4', 'G2', 'E4', '7.11.2', 'D3', 'D4', 'E4', '5.8.0', 'D3', 'F4', 'A5', 'A2', 'A2', 'D4', '9.0.4', 'E3', 'A2', 'F4', '0.4.7', 'E3', 'B4', '0.4.7', 'C4', '0.4.7', 'C3', 'C4', '0.4.7', 'C3', 'D3', '0.4.7', 'C3', 'D5', '0.4.7', 'C4', 'C3', '9.0.4', 'F2', 'C4', 'G2', '9.0.4', 'A2', 'C4', 'E5', '9.0.4', 'F2', 'D5', 'A4', '9.0.4', 'D5', 'G2', '9.0.4', 'F2', 'D5', 'D5', '7.11.2', 'G2', 'D5', '7.11.2', 'G2', 'B4', '7.11.2', 'G2', 'A4', '7.11.2', 'G2', 'A4', '7.11.2', 'G2', '0.4.7', 'C3', 'E4', '0.4.7', 'C3', 'E4', 'E4', '0.4.7', 'C3', 'G4', '0.4.7', 'C3', 'G4', '0.4.7', 'C3', '9.0.4'
#and then call graph_nearest.py output