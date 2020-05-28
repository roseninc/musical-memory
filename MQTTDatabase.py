#Import necessary modules for MySQL connection and MQTT communication
#
from time import gmtime, strftime
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

temperature_topic = "project_3/temp"
humidity_topic = "project_3/humi"
GPSLong_topic ="project_3/location/lng"
GPSLat_topic ="project_3/location/lat"
Light_topic ="project_3/ligh"

globals()['dataTuple'] = [0, 0, 0, 0, 0] 

# The callback for when the client receives a CONNACK- response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    #Subscribing to topics. If we lose connection and reconnect, subscriptions will be renewed.
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

#Function that inserts IoT data recieved over MQTT into the database
def update_db(): 

    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    connection = mysql.connector.connect(host="34.89.101.80", #Connect to the MySQL database
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

def update_array(typ, data): #Temporary array gets updated when new data is received
    print("Update array : " + str(typ) + str(data))
    dataTuple[typ] = data
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    update_db()
    return

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    result = (theTime + "\t" + str(msg.payload))
    print(msg.topic + ":\t" + result)

# Matches tuples array index and updates if new package arrives
    if which_package(msg.topic) == 0:
        update_array(0, msg.payload)

    if which_package(msg.topic) == 1:
        update_array(1, msg.payload)
    
    if which_package(msg.topic) == 2:
        update_array(2, msg.payload)

    if which_package(msg.topic) == 3:
        update_array(3, msg.payload)
    
    if which_package(msg.topic) == 4:
        update_array(4, msg.payload)

    return

client = mqtt.Client()
client.on_connect = on_connect

client.connect("broker.hivemq.com", 1883, 60)

client.on_message = on_message


client.loop_forever()
