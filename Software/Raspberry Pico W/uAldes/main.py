"""
MIT License

Copyright (c) 2025 Yann DOUBLET

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# WARNING: Do not modify this code directly.
# All configuration should be done in the 'config.py' file.
# This includes MQTT settings, WiFi credentials, and topic paths.
# Make any changes to the configuration file instead of modifying this main script.

from machine import Pin, UART, reset
import utime
import network, rp2

#from umqttsimple import MQTTClient
from simple import MQTTClient

import ualdes
from config import MQTT_CONFIG,MQTT_TOPICS, WIFI_NETWORKS,UALDES_OPTIONS

RELEASE_DATE = "11_05_2025"
VERSION = "2.0"

# Example of serial input format
example_serial_input = [0x33, 0xff, 0x4c, 0x33, 0x26, 0x00, 0x01, 0x01, 0x98, 0x03, 0x00, 0x00, 0x88, 0x00, 0x00, 0x28, 
                       0x95, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00, 0x00, 
                       0x56, 0x56, 0x56, 0x00, 0x93, 0x8b, 0xff, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                       0x00, 0x81, 0xc7, 0x2c, 0x01, 0x00, 0x00, 0x00, 0x00, 0xb0, 0xda, 0x38, 0x00, 0x00, 0x00, 0x00, 
                       0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x32, 0x7a]

print(f"Release Date : {RELEASE_DATE}")

# UART to STM32 setup :   
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# Software variables : 
last_message = 0

led=Pin("LED",Pin.OUT)
led.off()
rp2.country('FR')
wlan = network.WLAN(network.STA_IF)

wlan.active(True)
wlan.connect(WIFI_NETWORKS["ssid"], WIFI_NETWORKS["password"])
print(f"Trying to connect to WiFi...")
# Add timeout for connection attempts
max_wait = 10
while max_wait > 0:
  if wlan.isconnected():
    break
  max_wait -= 1
  print('Waiting for connection...')
  utime.sleep(1)
if not wlan.isconnected():
  print('Failed to connect to WiFi. Restarting...')
  reset()
  utime.sleep(0.1)
led.on()
print('Connection successful')
print(wlan.ifconfig())

def connect_and_subscribe():
  global client
  client = MQTTClient(MQTT_CONFIG["client_id"], MQTT_CONFIG["broker"],MQTT_CONFIG["port"],MQTT_CONFIG["user"],MQTT_CONFIG["password"])
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(MQTT_TOPICS["command"])
  print('Connected to %s, subscribed to %s topic' % (MQTT_CONFIG["broker"], MQTT_TOPICS["command"]))
  return client

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == (MQTT_TOPICS["command"].encode()):
    led.off()
    print('Received command: %s' % msg)
    input_cmd = ualdes.frame_encode(msg)
    print(input_cmd)
    if input_cmd != None:      
       print(uart.write(bytearray(input_cmd)))
       utime.sleep(0.5)
    led.on()

# Connect to MQTT broker
connect_and_subscribe()
while True:
  try:
    client.check_msg()
    uart_data = uart.read()

    if (utime.time() - last_message) > UALDES_OPTIONS["refresh_time"]:
        if uart_data is not None:
            print("Trame recue")
            print(uart_data)
            print("Taille : " + str(len(uart_data)))
            try:
                led.off()
                client.publish(MQTT_TOPICS["main"]+"trame", bytearray(uart_data).hex(" "))
                decoded_data = ualdes.frame_decode(uart_data)
                if decoded_data is not None:  # Check if data was decoded successfully
                    for topic in decoded_data:
                        client.publish(MQTT_TOPICS["main"]+topic, str(decoded_data[topic]))
                        print(f"{MQTT_TOPICS['main']}{topic}: {decoded_data[topic]}")
                last_message = utime.time()
                utime.sleep(0.2)
                led.on()
            except Exception as e:
                print("Error publishing data:", e)
            
  except Exception as e:
    led.off()
    print('General error:', e)
    utime.sleep(10)
    connect_and_subscribe()