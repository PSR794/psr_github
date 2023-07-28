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

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        
        while not wlan.isconnected():
            pass
        
    print('network config:', wlan.ifconfig())

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'ESP1/Updates' and msg == b'reboot':
    print('I am 32....ESP32')
    machine.reset()

def debug_led(n,f):
    i = 0
    while i<n:
        led.value(1)
        time.sleep(f)
        led.value(0)
        i+=1
    
def client_reconnect():
    while True:
        try:
            client.connect()
            debug_led(2,0.5)
            break
        except OSError as e:
            print("MQTT Disconnected with error: ",e)
            
        time.sleep(15)                    

led = machine.Pin(2, machine.Pin.OUT)
ssid = 'FAI GF 2.4GHz'
password = 'F@ctri4321'
do_connect()

mqtt_server = b"192.168.100.121"#b"b-4a6fc5ce-85ec-440f-8582-11553261333b-1.mq.ap-south-1.amazonaws.com"#
client_id = ubinascii.hexlify(machine.unique_id()) # gets ID
print(client_id)
topic_pub = b'Assembly1/Rfid_2'#b'factri/predev/trident/budhni/sheeting/csp/eton1/rpi1/rfid'# # toppic name
topic_sub = b'ESP1/Updates'
client = MQTTClient(b"client2", mqtt_server, port = 1883,
                          user=b"abc",#b"predev_user",
                          password=b"abc")#b"sehpi3-Mobsyr-jojkym"

client.set_callback(sub_cb)
while True:
    try:
        print("connecting...")
        client.connect()
        debug_led(1,1)
        break
    except OSError as e:
        print("MQTT Disconnected with error: ",e)
        
    time.sleep(10)
    

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)
print("Place card")

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
              debug_led(1,0.5)
            except :
                print('some error')
                continue
    try:
        client.subscribe(topic_sub)
    except OSError as e:
        client_reconnect()
            

