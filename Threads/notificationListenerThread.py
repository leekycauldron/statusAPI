import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import os, time, blinkt, sys, threading, queue
sys.path.insert(1,".")
from uberEatsThread import uberEatsThread
from config import MQTT_USER,MQTT_PASS,MQTT_PORT

user = MQTT_USER
passwd = MQTT_PASS
port = MQTT_PORT

uberEatsQueue = queue.Queue()

def uberEatsQueueThread():
    global uberEatsQueue
    while True:
        # If there are available threads, then take the links in the queue and take up a spot.
        if uberEatsQueue.empty() is False:
            currentLink = uberEatsQueue.get()
            if threading.active_count() <= 14:
                threading.Thread(target=uberEatsThread,args=(currentLink),daemon=True).start()


def notificationListenerThread():
    queueListenerThread = threading.Thread(target=uberEatsThread,daemon=True)
    queueListenerThread.start()
    blinkt.set_clear_on_exit()

    def on_connect(client, userdata, flags, rc):
        print("rc: " + str(rc))

    def on_message(client, obj, msg):
        global last_time
        temp = msg.payload.decode('utf-8')
        try:
            temp = temp.split("#")
        
            print(temp)
            print("Sender: {0}, Subject: {1}".format(temp[0],temp[1]))
        except:
            return -1
        formatSender = temp[0].lower()
        #Color stuff
        if "leekwen" in formatSender or "lee-kwen" in formatSender or "lee kwen" in formatSender:
            blinkt.set_pixel(0,255,0,0)
        elif "@gmail.com" in formatSender:
            blinkt.set_pixel(0,0,255,0)
        elif "dont" in formatSender:
            blinkt.set_pixel(0,0,0,255)
        else:
            blinkt.set_pixel(0,255,255,255)
        #Uber Eats Stuff
        if "https://www.ubereats.com/ca/orders/" in temp[1]:
            # Check if max amt of thread has exceeded, if so store links in a queue.
            count = threading.active_count()
            if count > 14:
                uberEatsQueue.put(temp[1])
            else: # Create a new thread
                threading.Thread(target=uberEatsThread,args=(temp[1]),daemon=True).start()

            
        blinkt.show()
        time.sleep(5)
        blinkt.clear()
        blinkt.show()
        time.sleep(0.5)

            

    def on_publish(client, obj, mid):
        print("mid: " + str(mid))

    def on_subscribe(client, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_print(client, obj, level, string):
        print("mqtt print {}".format(string))

    mqttc = mqtt.Client()

    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe


    url_str = "http://tailor.cloudmqtt.com"
    url = urlparse(url_str)
    topic = url.path[1:] or 'info1'
    # Connect
    mqttc.username_pw_set(user, passwd)
    def connect():
        print("Connected to MQTT...")
        mqttc.connect("tailor.cloudmqtt.com", port)
        mqttc.subscribe(topic,0)


    # Start subscribe, with QoS level 0
    while True:
        connect()
        rc = 0
        while rc == 0:
            rc = mqttc.loop()