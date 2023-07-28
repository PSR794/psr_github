import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import esp
import esp32
import network
import json# import all needed libraries
esp.osdebug(None)     # debug set to none
import gc             # garbage collector
gc.collect()
from mfrc522 import MFRC522
from machine import Pin
from machine import SPI

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(5)
  client = MQTTClient(b"client2", mqtt_server, port = 1883,
                          user=b"abc",#b"predev_user",
                          password=b"abc")#b"sehpi3-Mobsyr-jojkym"

  connect_mqtt(client)

def connect_mqtt(client):
    try:
      print('trying to connect')

      client.connect()
        
    except OSError as e:
      restart_and_reconnect()

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        
        while not wlan.isconnected():
            pass
        
    print('network config:', wlan.ifconfig())

led = machine.Pin(2, machine.Pin.OUT)
ssid = 'FAI GF 2.4GHz'
password = 'F@ctri4321'
do_connect()

mqtt_server = b"192.168.100.121"#b"b-4a6fc5ce-85ec-440f-8582-11553261333b-1.mq.ap-south-1.amazonaws.com"#
client_id = ubinascii.hexlify(machine.unique_id()) # gets ID
print(client_id)
topic_pub = b'Assembly1/Rfid_2'#b'factri/predev/trident/budhni/sheeting/csp/eton1/rpi1/rfid'# # toppic name
client = MQTTClient(b"client2", mqtt_server, port = 1883,
                          user=b"abc",#b"predev_user",
                          password=b"abc")#b"sehpi3-Mobsyr-jojkym"
connect_mqtt(client)

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
print("Place card")
led.value(1)
time.sleep(1)
led.value(0)
while True:    
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            card_id = "uid: 0x%02x%02x%02x%02x" % (raw_uid[3], raw_uid[2], raw_uid[1], raw_uid[0])
            #print(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            card_id = str(int(card_id[7:],16))
            if len(card_id) == 9:
                card_id = '0' + card_id
            try:                      
              JSON =  { "data": { "order": "IoTOrder", "station": "IoTStation",
                                  "confirmations": { "custom_form_field_values": [card_id],
                                                     "custom_form_field": "rfid_tag",
                                                     "yield_quantity": 0} }, "tenant": "clg"}
              json_payload = json.dumps(JSON)
              client.publish(topic_pub, json_payload)
              print(card_id," published!")
              led.value(1)
              time.sleep(0.5)
              led.value(0)
            except :
                print('some error')
            
                while True:
                    try:
                        client.connect()
                        led.value(1)
                        time.sleep(0.2)
                        led.value(0)
                        led.value(1)
                        time.sleep(0.2)
                        led.value(0)
                        break
                    except OSError as e:
                        print("MQTT Disconnected with error: ",e)
                        
                    time.sleep(15)                    
                
                continue

