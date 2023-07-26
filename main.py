import json
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

