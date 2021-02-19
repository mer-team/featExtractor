import essentia
import sys
import essentia.standard as es
import pika
import json
import os

mqhost = os.environ.get("HOST")
mquser = os.environ.get("USER")
mqpass = os.environ.get("PASS")
mqport = os.environ.get("PORT")

credentials =  pika.PlainCredentials(mquser, mqpass)
connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost, mqport,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='musicFeatures')
channel.queue_declare(queue='classifyMusic')

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(" [x] Received %r" % body)# See all feature names in the pool in a sorted order
    id = body
    # Compute all features, aggregate only 'mean' (media) and 'stdev' (desvio padrao) statistics for all low-level, rhythm and tonal frame features - https://essentia.upf.edu/documentation/essentia_python_examples.html
    features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
                                              rhythmStats=['mean', 'stdev'],
                                              tonalStats=['mean', 'stdev'])('/Audios/'+id+'.wav')
    print("Filename:", features['metadata.tags.file_name'])
    print(" Pitch Salience:")
    print("                Mean:", features['lowlevel.pitch_salience.mean'])
    print("                StDev:", features['lowlevel.pitch_salience.stdev'])
    print("Loudness:",features['lowlevel.average_loudness'])
    print("BPM:", features['rhythm.bpm'])
    print("Beat positions (sec.)", features['rhythm.beats_position'])
    toSend = [
        features['metadata.tags.file_name'],
        features['lowlevel.pitch_salience.mean'],
        features['lowlevel.average_loudness'],
        features['rhythm.bpm']
    ]
    channel.queue_declare(queue='classifyMusic')
    channel.basic_publish(exchange='',
                      routing_key='classifyMusic',
                      body=json.dumps(toSend))
    print(" [x] Sent ",features['metadata.tags.file_name']," to classify!!")
    print(' [*] Waiting for messages. To exit press CTRL+C')



channel.basic_consume(queue='musicFeatures',
                      auto_ack=False,
                      on_message_callback=callback)

channel.start_consuming()