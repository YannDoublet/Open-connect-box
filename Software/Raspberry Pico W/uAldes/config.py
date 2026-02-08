# Configuration file for ualdes project
# Contains WiFi and MQTT credentials

# WiFi Configuration
WIFI_NETWORKS ={
        "ssid": "xxxxxxxx",
        "password": "xxxxxxxx"
    }

# ALDES
UALDES_OPTIONS = {  
    "refresh_time": 60, # Time in seconds to refresh data
    "device": "EASYHOME", #T.FLOW or EASYHOME
    "serial_number": "ualdes",
    "device_in_ha": True
}

# MQTT Configuration
MQTT_CONFIG = {
    "broker": "xxx.xxx.xxx.xxx",
    "port": 1883,
    "client_id": "aldes",
    "user": "aldes",
    "password": "aldes",
    "ssl": False,
    "keepalive": 30
}

# MQTT Topics
MQTT_TOPICS = {
    "main": "aldes/",
    "command": "aldes/"+UALDES_OPTIONS["serial_number"]+"/set_mode",
    "haPrefix": "homeassistant/",
}

# MQTT Topics
MQTT_GROUPS = {
    "mode": {"main": "Mode", "conve": "Mode"},
    "qai": {"pwmqai": "PwmQAI_1", "co2": "CO2", "varhr": "Hum_Variat"},
    "kitchen": {"tmpcu": "Temp_Kitchen","hrcu": "Hum_Kitchen"},
    "bathroom": {"tmpba1": "Temp_Bath1","hrba1": "Hum_Bath1", "tmpba2": "Temp_Bath2","hrba2": "Hum_Bath2"},
}

# HA DEVICE Information
MQTT_HA = {
    "main_mode_select": {
        "type": "select",
        "properties": {
            "name": "Main mode",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_main_mode_selector",
            "object_id": UALDES_OPTIONS["serial_number"]+"_main_mode",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/mode",
            "value_template": "{{ value_json.main }}",
            "command_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/set_mode",
            "options": ["Daily", "Guest", "Boost", "Holiday", "Programming"],
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "main_mode": {
        "type": "sensor",
        "properties": {
            "name": "Main mode",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_main_mode",
            "object_id": UALDES_OPTIONS["serial_number"]+"_main_mode",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/mode",
            "value_template": "{{ value_json.main }}",
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "pwmqai": {
        "type": "sensor",
        "properties": {
            "name": "PwmQai",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_pwmqai",
            "object_id": UALDES_OPTIONS["serial_number"]+"_pwmqai",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/qai",
            "value_template": "{{ value_json.pwmqai }}",
            "min": 0,
            "max": 1000,
            "step": 1,
            "qos": 1,
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "co2": {
        "type": "sensor",
        "properties": {
            "name": "PwmQai",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_co2",
            "object_id": UALDES_OPTIONS["serial_number"]+"_co2",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/qai",
            "value_template": "{{ value_json.co2 }}",
            "qos": 1,
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "varhr": {
        "type": "sensor",
        "properties": {
            "name": "Variation Humidite",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_varhr",
            "object_id": UALDES_OPTIONS["serial_number"]+"_varhr",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/qai",
            "value_template": "{{ value_json.varhr }}",
            "qos": 1,
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "tmpcu": {
        "type": "sensor",
        "properties": {
            "name": "Temperature Cuisine",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_tmpcu",
            "object_id": UALDES_OPTIONS["serial_number"]+"_tmpcu",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/kitchen",
            "value_template": "{{ value_json.tmpcu }}",
            "min": 0,
            "max": 100,
            "qos": 1,
            "device_class": "Temperature",
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "hrcu": {
        "type": "sensor",
        "properties": {
            "name": "Humidite Cuisine",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_hrcu",
            "object_id": UALDES_OPTIONS["serial_number"]+"_hrcu",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/kitchen",
            "value_template": "{{ value_json.hrcu }}",
            "min": 0,
            "max": 100,
            "qos": 1,
            "device_class": "Humidity",
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "tmpba1": {
        "type": "sensor",
        "properties": {
            "name": "Temperature Salle de bain 1",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_tmpba1",
            "object_id": UALDES_OPTIONS["serial_number"]+"_tmpba1",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/bathroom",
            "value_template": "{{ value_json.tmpba1 }}",
            "min": 0,
            "max": 100,
            "qos": 1,
            "device_class": "Temperature",
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "hrba1": {
        "type": "sensor",
        "properties": {
            "name": "Humidite Salle de bain 1",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_hrba1",
            "object_id": UALDES_OPTIONS["serial_number"]+"_hrba1",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/bathroom",
            "value_template": "{{ value_json.hrba1 }}",
            "min": 0,
            "max": 100,
            "qos": 1,
            "device_class": "Humidity",
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "tmpba2": {
        "type": "sensor",
        "properties": {
            "name": "Temperature Salle de bain 2",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_tmpba2",
            "object_id": UALDES_OPTIONS["serial_number"]+"_tmpba2",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/bathroom",
            "value_template": "{{ value_json.tmpba2 }}",
            "min": 0,
            "max": 100,
            "qos": 1,
            "device_class": "Temperature",
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
    "hrba2": {
        "type": "sensor",
        "properties": {
            "name": "Humidite Salle de bain 2",
            "unique_id": UALDES_OPTIONS["serial_number"]+"_hrba2",
            "object_id": UALDES_OPTIONS["serial_number"]+"_hrba2",
            "state_topic": MQTT_TOPICS["main"]+UALDES_OPTIONS["serial_number"]+"/bathroom",
            "value_template": "{{ value_json.hrba2 }}",
            "min": 0,
            "max": 100,
            "qos": 1,
            "device_class": "Humidity",
            "device": {
                "identifiers": [
                    UALDES_OPTIONS["serial_number"]
                ],
                "name": UALDES_OPTIONS["device"],
                "manufacturer": "Aldes",
                "model": "EASY_HOME",
            },
        }
    },
}
