# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import time
import random
import base64
import serial.tools.list_ports

from Adafruit_IO import MQTTClient

AIO_FEED_ID = "Fan_1"
AIO_FEED_ID1 = "Light_1"
AIO_FEED_ID2 = "Humidity_sensor"
AIO_FEED_ID3 = "Heat_sensor"
AIO_FEED_ID4 = "Light_sensor"
AIO_USERNAME = "Ailasoi"
AIO_KEY = "aio_WEcd27gk7UJYd7IANkWs4AESAGkR"


def connected(client):
    print("Ket noi thanh cong...")
    client.subscribe(AIO_FEED_ID)
    client.subscribe(AIO_FEED_ID1)
    client.subscribe(AIO_FEED_ID2)
    client.subscribe(AIO_FEED_ID3)
    client.subscribe(AIO_FEED_ID4)


def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong...")


def disconnected(client):
    print("Ngat ket noi...")
    sys.exit(1)


def message(client, feed_id, payload):
    print(feed_id)
    if feed_id == AIO_FEED_ID:
        if payload == "0":
            ser.write(("#0").encode())
            print("#0")
        if payload == "1":
            ser.write(("#1").encode())
            print("#1")
    if feed_id == AIO_FEED_ID1:
        if payload == "0":
            ser.write(("#2").encode())
            print("#2")
        if payload == "1":
            ser.write(("#3").encode())
            print("#3")


def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            # if "Electronic Team" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort


def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end + 1:]


mess = ""


def processData(data):
    print(data)
    # for x in count:
    #     count = 0
    #     if
    data = data.replace("!", "")
    data = data.replace("#", "")
    values = data.split(':')
    if len(values) != 3:
        print("Syntax error: " + data)
    else:

        print(values[0])
        time.sleep(2)
        client.publish(AIO_FEED_ID3, values[1])
        print(values[1])
        time.sleep(2)
        client.publish(AIO_FEED_ID4, values[2])
        print(values[2])
        time.sleep(2)


ser = serial.Serial(port=getPort(), baudrate=115200)
mess = ""
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    readSerial()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
