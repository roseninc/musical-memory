from time import gmtime, strftime
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import configparser

temperature_topic = "project_3/temp"
humidity_topic = "project_3/humi"
GPSLong_topic ="project_3/location/lng"
GPSLat_topic ="project_3/location/lat"
Light_topic ="project_3/ligh"

globals()['dataTuple'] = [0, 0, 0, 0, 0]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(temperature_topic)
    client.subscribe(humidity_topic)
    client.subscribe(GPSLong_topic)
    client.subscribe(GPSLat_topic)
    client.subscribe(Light_topic)
    return

def which_package(msg):

    if (msg in temperature_topic):
        return 0
    if (msg in humidity_topic):
        return 1
    if (msg in GPSLat_topic):
        return 2
    if (msg in GPSLong_topic):
        return 3
    if (msg in Light_topic):
        return 4
    return -1

def update_db():
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    reader = configparser.RawConfigParser()
    reader.read('information.cnf')
    connection = mysql.connector.connect(host="34.89.101.80",
                                        database="teaminternational",
                                        user="root",
                                        password="vc68HvL7Py5PdgK4")
    sql = "INSERT INTO climate (reading_time, temp, hum, gpslat, gpslong, light) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (current_time, dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3], dataTuple[4])
    cursor = connection.cursor()
    cursor.execute(sql, val)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into table")
    cursor.close()
    if (connection.is_connected()):
        connection.close()
        print("MySQL connection is closed")

    return

def update_array(typ, data):
    print("Update array : " + str(typ) + str(data))
    dataTuple[typ] = data
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    update_db()
   # conn = sqlite3.connect(dbFile)
   # c = conn.cursor()
    #print ("Writing to db...")
   # c.execute("INSERT INTO climate VALUES (?,?,?,?,?,?)", (current_time, dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3], dataTuple[4]))
    #conn.commit()
    return

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    result = (theTime + "\t" + str(msg.payload))
    print(msg.topic + ":\t" + result)

    if which_package(msg.topic) == 0:
        #print("Entered 0")
        update_array(0, msg.payload)

    if which_package(msg.topic) == 1:
        #print("Entered 1")
        update_array(1, msg.payload)
    
    if which_package(msg.topic) == 2:
        #print("Entered 2")
        update_array(2, msg.payload)

    if which_package(msg.topic) == 3:
        #print("Entered 3")
        update_array(3, msg.payload)
    
    if which_package(msg.topic) == 4:
        #print("Entered 4")
        update_array(4, msg.payload)

    return

client = mqtt.Client()
client.on_connect = on_connect

client.connect("broker.hivemq.com", 1883, 60)

client.on_message = on_message

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
