import pika
import os

mqhost = os.environ.get("MQHOST")
mquser = os.environ.get("MQUSER")
mqpass = os.environ.get("MQPASS")
mqport = os.environ.get("MQPORT")

credentials =  pika.PlainCredentials(mquser, mqpass)
connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost, mqport, '/', credentials))

vID = 'JiF3pbvR5G0'
queue_send = 'musicFeatures'
queue_receive = 'classifyMusic'
should_receive = 'JiF3pbvR5G0.wav'


def test_rabbitmq():
    """Check rabbitmq connection"""
    channel = connection.channel()

    assert connection.is_open == True and channel.is_open == True
    connection.close()

def test_send_message():
    """Send rabbitmq vID to process"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost, mqport, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_send)
    channel.basic_publish(exchange='', routing_key=queue_send, body=vID)
    print(" [x] Sent " + vID + " to process.")
    connection.close()

    assert connection.is_closed == True and channel.is_closed == True 

#def test_receive_message():
#    """Wait for message"""
#    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
#    channel = connection.channel()
#    channel.queue_declare(queue=queue_receive)
#    channel.basic_consume(queue=queue_receive, on_message_callback=callback, auto_ack=False)
#    print(' [*] Waiting for messages in '+queue_receive)
#    channel.start_consuming()

#def callback(ch, method, properties, body):
#    print(" [x] Received message in "+queue_receive)
    #message = str(body.decode("utf-8"))
#    message = str(body.decode("utf-8"))
    #assert re.match(r"\[\"JiF3pbvR5G0.wav\", 0.44834503531455994, \d+, 115.56307220458984]$",)
    #assert re.match(r"bob\|\d+\|abc\|manual$", incoming_string)
#    assert body.decode("utf-8") == '["JiF3pbvR5G0.wav", 0.44834503531455994, 0.9279613494873047, 115.56307220458984]'


    

