# Configuration file for ualdes project
# Contains WiFi and MQTT credentials

# WiFi Configuration
WIFI_NETWORKS ={
        "ssid": "your_wifi_ssid",
        "password": "your_wifi_password"
    }

# MQTT Configuration
MQTT_CONFIG = {
    "broker": "mqtt.broker.address",
    "port": 1883,
    "client_id": "uart_usb_device",
    "user": "mqtt_username",
    "password": "mqtt_password",
    "ssl": False,
    "keepalive": 60
}

# MQTT Topics
MQTT_TOPICS = {
    "publish": "uart_usb/data",
    "subscribe": "uart_usb/commands",
    "status": "uart_usb/status"
}

UALDES_OPTIONS = {  
    "refresh_time": 60 # Time in seconds to refresh data
}