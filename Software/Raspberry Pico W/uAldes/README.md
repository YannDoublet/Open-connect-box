# uAldes

## Présentation

Ce projet implémente une passerelle entre les communications série UART (depuis un STM32 lui meme raccorder à un chauffe-eau T.FLOW de chez ALDES) et un broker MQTT. Conçu pour fonctionner sur un microcontrôleur comme le Raspberry Pi Pico W, il permet de:

- Recevoir des données depuis un périphérique UART
- Décoder ces données via la bibliothèque `ualdes`
- Publier les données décodées sur des topics MQTT configurables
- Recevoir des commandes MQTT et les transmettre au périphérique UART

## Caractéristiques

- ✅ Configuration WiFi et MQTT simplifiée via fichier de configuration
- ✅ Détection automatique des trames UART
- ✅ Publication de données en temps réel
- ✅ Contrôle bidirectionnel (lecture/écriture)
- ✅ Indicateur LED pour visualiser l'état de connexion et les transmissions
- ✅ Reconnexion automatique en cas de perte de connexion

## Configuration

Toute la configuration se fait dans le fichier config.py :

# Paramètres WiFi
WIFI_NETWORKS = {
    "ssid": "votre_ssid",
    "password": "votre_mot_de_passe" 
}

# Configuration MQTT
MQTT_CONFIG = {
    "client_id": "gateway_uart",
    "broker": "adresse_du_broker",
    "port": 1883,
    "user": "utilisateur_mqtt",
    "password": "mot_de_passe_mqtt"
}

# Topics MQTT
MQTT_TOPICS = {
    "main": "home/device/",
    "command": "home/device/command"
}

# Options de la bibliothèque UALDES
UALDES_OPTIONS = {
    "refresh_time": 60  # Temps de rafraîchissement en secondes
}

## Installation

1. Flashez MicroPython sur votre Raspberry Pi Pico W
2. Transférez les fichiers suivants sur la carte:
   - main.py
   - config.py (à créer selon le modèle ci-dessus)
   - simple.py (bibliothèque MQTT)
   - ualdes.py (bibliothèque de décodage Aldes)

## Connexions matérielles

- **UART TX**: GPIO 0 (Pin 1)
- **UART RX**: GPIO 1 (Pin 2)
- **Alimentation**: USB ou source externe 5V

## Utilisation

Une fois configuré et démarré, le système:
1. Se connecte automatiquement au réseau WiFi
2. Établit une connexion avec le broker MQTT
3. Commence à écouter les données UART et les publie sur les topics correspondants
4. Écoute les commandes MQTT et les transmet via UART

## Format des données

Le système reçoit des trames UART au format binaire. Exemple de trame:

```
[0x33, 0xff, 0x4c, 0x33, 0x26, 0x00, ...]
```

Ces données sont décodées par ualdes.py et publiées sur des topics MQTT individuels.

## Licence

MIT License © 2025 Yann DOUBLET

## Version

Version: 2.0  
Date de publication: 11/05/2025

---

⚠️ **Avertissement**: Ne modifiez pas directement le fichier main.py. Toutes les configurations doivent être effectuées dans le fichier config.py.
