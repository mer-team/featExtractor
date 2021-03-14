import essentia
import sys
import essentia.standard as es
import os, os.path
import csv

folder = "../../MER_audio_taffc_dataset/"
total = len(os.listdir(folder+'Q1/'))+len(os.listdir(folder+'Q2/'))+len(os.listdir(folder+'Q3/'))+len(os.listdir(folder+'Q4/'))
counter = 0
with open('./features.csv', 'wb') as csvfile:
    for i in range(1,5):
        for music in os.listdir(folder+'Q'+str(i)+'/'):
            features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                              rhythmStats=['mean', 'stdev'],
                                              tonalStats=['mean', 'stdev'])(folder+'Q'+str(i)+'/'+music)
            spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([str(i), str(1)+':'+str(features['lowlevel.pitch_salience.mean']), str(2)+':'+str(features['lowlevel.average_loudness']),str(3)+':'+str(features['rhythm.bpm'])])
            counter = counter + 1
            print str(counter)+" em "+ str(total)
            

