import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import esp
import esp32  
import json# import all needed libraries
esp.osdebug(None)     # debug set to none
import gc             # garbage collector
gc.collect()

mqtt_server = b"b-4a6fc5ce-85ec-440f-8582-11553261333b-1.mq.ap-south-1.amazonaws.com"
#mqtt_server = "broker.emqx.io"     # works best for me
#mqtt_server = "broker.hivemq.com"
#mqtt_server = '3.65.154.195:1883'  #broker.hivemq.com
#mqtt_server = '5.196.95.208'       #test.mosquitto.org
client_id = ubinascii.hexlify(machine.unique_id()) # gets ID
topic_pub = b'factri/predev/trident/budhni/sheeting/csp/eton1/rpi1/rfid' # toppic name

last_message = 0 
message_interval = 5
counter = 0


def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(5)
  machine.reset()

try:
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server, port = 8883,
                      user=b"predev_user",
                      password=b"sehpi3-Mobsyr-jojkym")
  client.connect()
  try:
    JSON =  { "tenant": "trident", "data": { "order": "order of 32", "station": "station of 32",
                                                                        "confirmations": { "user_filter_key": "Key of 32",
                                                                                        "user_filter_values": ["I am 32...ESP32"], "yield_quantity": 32 } } }
    json_payload = json.dumps(JSON)
    client.publish(topic_pub, json_payload)
    
  except:
    print("some error")
    
except OSError as e:
  restart_and_reconnect()

