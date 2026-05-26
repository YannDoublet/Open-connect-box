# Configuration file for ualdes project
# Contains WiFi and MQTT credentials

WIFI_NETWORKS ={
        "ssid": "SSID",
        "password": "PASSWORD"
    }

# MQTT Configuration
MQTT_CONFIG = {
    "broker": "192.168.1.1",
    "port": 1883,
    "client_id": "cleint_id",
    "user": "user",
    "password": "password",
    "ssl": False,
    "keepalive": 60
}


# ALDES
UALDES_OPTIONS = {  
    "refresh_time": 60, # Time in seconds to refresh data
    "device": "EASYHOME", #T.FLOW or EASYHOME
    "serial_number": "ualdes",
    "device_in_ha": True
}

ITEMS_MAPPING = {
        "Slave":        {"Index": 0, "Type": 0, "Publish": False},
        "Data_Lenght":  {"Index": 2, "Type": 0, "Publish": False},
        "StartPattern": {"Index": 3, "Type": 0, "Publish": False},
        "PwmQAI_1": 	{"LSB_Index": 8, "MSB_Index": 9, "Type": 10, "Publish": True},
        "Mode":         {"Index": 9, "Type": 7, "Publish": True},
        "Temp_Kitchen": {"Index": 14, "Type": 6, "Publish": True},
        "Hum_Kitchen":  {"Index": 15, "Type": 0, "Publish": True},
        "Temp_Bath1":   {"Index": 16, "Type": 6, "Publish": True},
        "Hum_Bath1":    {"Index": 17, "Type": 0, "Publish": True},
        "Temp_Bath2":   {"Index": 18, "Type": 6, "Publish": True},
        "Hum_Bath2":    {"Index": 19, "Type": 0, "Publish": True},
        "CO2": 		    {"LSB_Index": 20, "MSB_Index": 21, "Type": 10, "Publish": True},
        "Hum_Variat":   {"Index": 23, "Type": 0, "Publish": True},
        "PwmQAI_2": 	{"LSB_Index": 24, "MSB_Index": 25, "Type": 10, "Publish": False},
        "EndPattern":   {"Index": 26, "Type": 0, "Publish": False}
}

ITEMS = {
    "Slave":"test"
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
            "command_template": "{\"type\":\"{{ value }}\"}",
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
