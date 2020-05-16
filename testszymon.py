from time import gmtime, strftime
import paho.mqtt.client as mqtt
import sqlite3

temperature_topic = "project_3/temp"
humidity_topic = "project_3/humi"
gps_long = "project_3/location/lng"
gps_lat = "project_3/location/lat"
light = "project_3/ligh"
dbFile = "data.db"

dataTuple = [-1, -1, -1, -1, -1]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(temperature_topic)
    client.subscribe(humidity_topic)
    client.subscribe(gps_long)
    client.subscribe(gps_lat)
    client.subscribe(light)

def on_message(client, userdata, msg):
    theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    result = (theTime + "\t" + str(msg.payload.decode("utf-8")))
    print(msg.topic + ":\t" + result)
    print(dataTuple)
    if msg.topic == temperature_topic:
        dataTuple[0] = str(msg.payload.decode("utf-8"))
    if msg.topic == humidity_topic:
        dataTuple[1] = str(msg.payload.decode("utf-8"))
    if msg.topic == gps_long:
        dataTuple[2] = str(msg.payload.decode("utf-8"))
    if msg.topic == gps_lat:
        dataTuple[3] = str(msg.payload.decode("utf-8"))
    if msg.topic == light:
        dataTuple[4] = str(msg.payload.decode("utf-8"))
        return

    print("HerE!")
    if dataTuple[0] != -1 and dataTuple[1] != -1 and dataTuple[2] != -1 and dataTuple[3] != -1 and dataTuple[4] != -1:
        print("we are here")
        writeToDb(theTime, dataTuple[0], dataTuple[1], dataTuple[3], dataTuple[2], dataTuple[4])
        return

def writeToDb(theTime, temperature, humidity, gpsLat, gpsLong, Light):
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    print ("Writing to db...")
    c.execute("INSERT INTO climate VALUES(?,?,?,?,?,?)", (theTime, temperature, humidity, gpsLat, gpsLong, Light))
    conn.commit()
    print ("Data written")

    global dataTuple
    dataTuple = [-1, -1, -1, -1, -1]

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()