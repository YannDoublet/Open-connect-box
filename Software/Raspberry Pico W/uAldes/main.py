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
import json

#from umqttsimple import MQTTClient
from simple import MQTTClient

#import ualdes
from ualdes import ITEMS_MAPPING, FRAME_INFO, frame_decode, frame_encode

from config import MQTT_CONFIG, MQTT_TOPICS, MQTT_GROUPS, MQTT_HA, WIFI_NETWORKS, UALDES_OPTIONS

RELEASE_DATE = "02_02_2026"
VERSION = "2.2"
# VERSION 2.2 implement EASYHOME VMC

# Circular Buffer to capture UART
RX_BUFFER_SIZE = 1024
rx_buffer = bytearray(RX_BUFFER_SIZE)
rx_write_pos = 0
rx_read_pos = 0
start = None
frame_type = None

# Statistics
stats_frames_ok = 0
stats_frames_bad_checksum = 0
stats_buffer_overflow = 0
stats_frames_skipped = 0

# Example of serial input format
example_serial_input = [0x33, 0xff, 0x4c, 0x33, 0x26, 0x00, 0x01, 0x01, 0x98, 0x03, 0x00, 0x00, 0x88, 0x00, 0x00, 0x28, 
                       0x95, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00, 0x00, 
                       0x56, 0x56, 0x56, 0x00, 0x93, 0x8b, 0xff, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                       0x00, 0x81, 0xc7, 0x2c, 0x01, 0x00, 0x00, 0x00, 0x00, 0xb0, 0xda, 0x38, 0x00, 0x00, 0x00, 0x00, 
                       0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x32, 0x7a]

print(f"Release Date : {RELEASE_DATE}")

if UALDES_OPTIONS["device"] == "T.Flow":
    # UART to STM32 setup :   
    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
    print("Info: ALDES DEVICE: T.Flow")
elif UALDES_OPTIONS["device"] == "EASYHOME":
    # UART to VMC setup :
    uart = UART(0, baudrate=2400, bits=8, parity=0, stop=1, 
             tx=Pin(0), rx=Pin(1), invert=UART.INV_TX)
    print("Info: ALDES DEVICE: EASYHOME")
else:
    print(f"Configuration error: ALDES DEVICE not recognized: ", UALDES_OPTIONS["device"])

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
led.on()
print('Connection successful')
print(wlan.ifconfig())

def try_reconnect(max_attempts=5):
    global client
    attempts = 0
    while attempts < max_attempts:
        try:
            print("Tentative de reconnexion MQTT...")
            client = connect_and_subscribe()
            print("Reconnexion MQTT réussie")
            return
        except Exception as e:
            print("Échec de reconnexion MQTT :", e)
            attempts += 1
            utime.sleep(10)
    print("Reconnexion impossible. Redémarrage du système.")
    reset()

def uart_to_buffer():
    global rx_write_pos, rx_read_pos, stats_buffer_overflow
    if not uart.any():
        return 0
    
    bytes_written = 0
    
    while uart.any():
        space_available = (rx_read_pos - rx_write_pos - 1) % RX_BUFFER_SIZE
        if space_available == 0:
            stats_buffer_overflow += 1
            print("Buffer overflow!")
            #break
        
        #read_size = min(space_available, uart.any())
        read_size = uart.any()
        data = uart.read(read_size)
        
        if not data:
            break
        
        for b in data:
            rx_buffer[rx_write_pos] = b
            rx_write_pos = (rx_write_pos + 1) % RX_BUFFER_SIZE
            bytes_written += 1
    
    return bytes_written

def extract_frame_from_buffer():
    global rx_read_pos, rx_write_pos, rx_buffer, start, frame_type
    available = (rx_write_pos - rx_read_pos) % RX_BUFFER_SIZE
    if available < 2:
        return None
    
    # Looking for RX_START_IDENTIFIER if not found
    if start is None:
        for i in range(0, available, 2):
            idx = (rx_read_pos + i) % RX_BUFFER_SIZE
            if rx_buffer[idx] == FRAME_INFO["RX_MASTER_IDENTIFIER"] and rx_buffer[(idx + 1)% RX_BUFFER_SIZE] == FRAME_INFO["RX_SLAVE_IDENTIFIER"]:
                frame_type = "VMC"
                start = idx
                break
            elif rx_buffer[idx] == FRAME_INFO["TX_MASTER_IDENTIFIER"] and rx_buffer[(idx + 1)% RX_BUFFER_SIZE] == FRAME_INFO["TX_SLAVE_IDENTIFIER"]:
                frame_type = "HUB"
                start = idx
                break

    # If start is still not found, move the rx position to last position in the buffer and come back later
    if start is None:
        rx_read_pos = rx_write_pos
        return None
    
    # The buffer need to be at least equal to data start + ITEM_MAPPING["Data_Lenght"]["Index"]
    Data_Lenght_Position = (start + ITEMS_MAPPING["Data_Lenght"]["Index"]) % RX_BUFFER_SIZE
    #print ("Data_Lenght_Position: ", Data_Lenght_Position)
    #print ("rx_read_pos: ", rx_read_pos)
    #print ("available: ", available)
    if (rx_read_pos + available - 1) < Data_Lenght_Position:
        return None
    
    # Looking for Data_Lenght
    frame_size = rx_buffer[Data_Lenght_Position]
    
    # Verify if the entire frame is in the buffer + the checksum
    end = start + frame_size + 1
    if (rx_read_pos + available) < end:
        return None
    
    frame = bytearray(frame_size + 1)
    # Extract then entire frame
    for j in range(frame_size + 1):
        frame[j] = rx_buffer[(start + j) % RX_BUFFER_SIZE]
    rx_read_pos = (start + j + 1) % RX_BUFFER_SIZE
    start = None
    return bytes(frame)

def connect_and_subscribe():
  global client
  client = MQTTClient(MQTT_CONFIG["client_id"], MQTT_CONFIG["broker"],MQTT_CONFIG["port"],MQTT_CONFIG["user"],MQTT_CONFIG["password"])
  client.set_callback(sub_cb)
  client.connect(timeout=5)
  client.subscribe(MQTT_TOPICS["command"])
  print('Connected to %s, subscribed to %s topic' % (MQTT_CONFIG["broker"], MQTT_TOPICS["command"]))
  return client

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == (MQTT_TOPICS["command"].encode()):
    led.off()
    print('Received command: %s' % msg)
    input_cmd = frame_encode(msg)
    print(bytes(input_cmd))
    if input_cmd != None:      
       print(uart.write(bytearray(input_cmd)))
       utime.sleep(0.5)
    led.on()

# Connect to MQTT broker
client = None
try_reconnect()

last_ping = utime.time()

while True:
  # Vérification périodique de la connexion Wi-Fi
  uart_data = None
  if not wlan.isconnected():
    print("Wi-Fi déconnecté. Tentative de reconnexion...")
    wlan.connect(WIFI_NETWORKS["ssid"], WIFI_NETWORKS["password"])
    for i in range(10):
      if wlan.isconnected():
        print("Reconnexion Wi-Fi réussie.")
        break
      print("Attente reconnexion Wi-Fi...")
      utime.sleep(1)
    if not wlan.isconnected():
      print("Impossible de se reconnecter au Wi-Fi. Redémarrage...")
      reset()

  try:
    client.check_msg()
    
    if UALDES_OPTIONS["device"] == "T.Flow":
        uart_data = uart.read()
    elif UALDES_OPTIONS["device"] == "EASYHOME":
        uart_to_buffer()
        uart_data = extract_frame_from_buffer()

    if (utime.time() - last_ping) > MQTT_CONFIG["keepalive"]:
        try:
            client.ping()
            print("Ping envoyé")
            last_ping = utime.time()
        except Exception as e:
            print("Erreur ping, tentative de reconnexion...")
            try_reconnect()

    if UALDES_OPTIONS["device"] == "T.Flow":
        if (utime.time() - last_message) > UALDES_OPTIONS["refresh_time"]:
            if uart_data is not None:
                print("Trame recue")
                print(uart_data)
                print("Taille : " + str(len(uart_data)))
                try:
                    led.off()
                    client.publish(MQTT_TOPICS["main"]+"trame", bytearray(uart_data).hex(" "))
                    decoded_data = frame_decode(uart_data)
                    if decoded_data is not None:  # Check if data was decoded successfully
                        for topic in decoded_data:
                            client.publish(MQTT_TOPICS["main"]+topic, str(decoded_data[topic]))
                            print(f"{MQTT_TOPICS['main']}{topic}: {decoded_data[topic]}")

                    last_message = utime.time()
                    utime.sleep(0.2)
                    led.on()
                except Exception as e:
                    print("Error publishing data:", e)
            
    elif UALDES_OPTIONS["device"] == "EASYHOME":
        if uart_data is not None:
            print("Trame received at: ", utime.time())
            print(frame_type, uart_data)
            print("Taille : " + str(len(uart_data)))
            try:
                led.off()
                client.publish(MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/trame_"+frame_type, bytearray(uart_data).hex(" "))
                if frame_type == "VMC":
                    decoded_data = frame_decode(uart_data)
                    if decoded_data is not None:  # Check if data was decoded successfully
                        for group, properties in MQTT_GROUPS.items():
                            payload = "{"
                            for topic, data in properties.items():
                                # Add a comma in case it is not the first one
                                if payload != "{":
                                    payload = payload+","
                                payload = payload+"\""+topic+"\":"+str(decoded_data[data])+""
                            payload = payload+"}"
                            client.publish(MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/"+group, payload)
                            #print(f"{MQTT_TOPICS['main']}{group}: \{{topic}: {decoded_data[topic]}\}")
                            uart_data = None
                        if UALDES_OPTIONS["device_in_ha"]:
                            for sensor, info in MQTT_HA.items():
                                payload = json.dumps(info["properties"])
                                client.publish(MQTT_TOPICS["haPrefix"]+info["type"]+"/aldes/"+UALDES_OPTIONS["serial_number"]+"_"+str(sensor)+"/config", payload)
                                #print(f"{MQTT_TOPICS['main']}{group}: \{{topic}: {decoded_data[topic]}\}")
                                uart_data = None
                last_message = utime.time()
                utime.sleep(0.2)
                led.on()
            except Exception as e:
                print("Error publishing data:", e)
            
  except Exception as e:
    led.off()
    print('General error:', e)
    utime.sleep(10)
    try_reconnect()