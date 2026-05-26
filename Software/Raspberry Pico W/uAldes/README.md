# uAldes

## Présentation

Ce projet implémente une passerelle entre les communications série UART d'appareils ALDES et un broker MQTT. Conçu pour fonctionner sur un microcontrôleur comme le Raspberry Pi Pico W, il supporte deux équipements :

- **T.FLOW** : chauffe-eau thermodynamique ALDES (communication passive, réception des trames envoyées par le STM32)
- **EASYHOME** : VMC hygroréglable ALDES (communication active par polling, le Pico envoie une trame toutes les N secondes et lit la réponse)

Le système permet de :

- Recevoir des données depuis un périphérique UART
- Décoder ces données via la bibliothèque `ualdes`
- Publier les données décodées sur des topics MQTT configurables
- Recevoir des commandes MQTT et les transmettre au périphérique UART
- Publier automatiquement la configuration des entités dans Home Assistant (MQTT Discovery)

## Caractéristiques

- ✅ Configuration WiFi et MQTT simplifiée via fichier de configuration
- ✅ Support T.FLOW et EASYHOME sélectionnable dans `config.py`
- ✅ Détection automatique des trames UART avec buffer circulaire (EASYHOME)
- ✅ Polling actif configurable (EASYHOME)
- ✅ Publication de données en temps réel par groupes thématiques
- ✅ Contrôle bidirectionnel (lecture/écriture)
- ✅ Intégration Home Assistant via MQTT Discovery
- ✅ Indicateur LED pour visualiser l'état de connexion et les transmissions
- ✅ Reconnexion automatique en cas de perte de connexion WiFi ou MQTT

## Configuration

Toute la configuration se fait dans le fichier `config.py` :

```python
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
    "password": "mot_de_passe_mqtt",
    "keepalive": 60
}

# Options ALDES
UALDES_OPTIONS = {
    "refresh_time": 60,       # Intervalle de polling/publication en secondes
    "device": "EASYHOME",     # "TFLOW" ou "EASYHOME"
    "serial_number": "ualdes", # Identifiant unique utilisé dans les topics MQTT
    "device_in_ha": True      # Activer la découverte automatique Home Assistant
}
```

### Topics MQTT générés (EASYHOME)

| Topic | Description |
|---|---|
| `aldes/<serial>/trame_VMC` | Trame brute reçue (hex) |
| `aldes/<serial>/mode` | Mode en cours et mode converti |
| `aldes/<serial>/qai` | PWM QAI, CO2, variation d'humidité |
| `aldes/<serial>/kitchen` | Température et humidité cuisine |
| `aldes/<serial>/bathroom` | Températures et humidités salles de bain |

### Commandes MQTT (EASYHOME)

Publier sur `aldes/<serial>/set_mode` avec un payload JSON :

| Commande | Payload |
|---|---|
| Mode Journalier | `{"type": "Daily"}` |
| Mode Invité | `{"type": "Guest"}` |
| Mode Boost | `{"type": "Boost"}` |
| Mode Vacances | `{"type": "Holiday"}` |
| Mode Programmation | `{"type": "Programming"}` |

## Installation

1. Flashez MicroPython sur votre Raspberry Pi Pico W
2. Transférez les fichiers suivants sur la carte :
   - `main.py`
   - `config.py` (à créer selon le modèle ci-dessus)
   - `simple.py` (bibliothèque MQTT)
   - `ualdes.py` (bibliothèque de décodage Aldes)

## Connexions matérielles

| Signal | GPIO | Pin physique |
|---|---|---|
| UART TX | GPIO 0 | Pin 1 |
| UART RX | GPIO 1 | Pin 2 |
| Alimentation | — | USB ou 5V externe |

> **EASYHOME** : la ligne TX est inversée logiquement (`UART.INV_TX`) et fonctionne à 2400 bauds, 8N1.  
> **T.FLOW** : UART à 115200 bauds, réception seule.

## Utilisation

Une fois configuré et démarré, le système :
1. Se connecte automatiquement au réseau WiFi
2. Établit une connexion avec le broker MQTT
3. (EASYHOME) Envoie périodiquement une trame de polling et lit la réponse de la VMC
4. Décode les trames et publie les valeurs sur les topics MQTT correspondants
5. Écoute les commandes MQTT et les transmet via UART

## Format des données

### Trame brute reçue (EASYHOME)

```
87 00 1B 4B ... <checksum>
```

La trame est identifiée par les octets `0x87 0x00` en début de trame. Elle est extraite d'un buffer circulaire et validée par somme de contrôle (complément à 2).

### Données décodées

Les données publiées incluent notamment :

- `Mode` : mode VMC actif (`Daily`, `Guest`, `Boost`, `Holiday`, `Programming`)
- `PwmQAI_1` : débit PWM (16 bits)
- `CO2` : concentration CO2 (16 bits)
- `Hum_Variat` : variation d'humidité
- `Temp_Kitchen`, `Hum_Kitchen` : température (BCD 0.25°C) et humidité cuisine
- `Temp_Bath1/2`, `Hum_Bath1/2` : température et humidité salles de bain

## Licence

MIT License © 2025 Yann DOUBLET

## Version

Version: 2.2  
Date de publication: 26/05/2026

---

⚠️ **Avertissement**: Ne modifiez pas directement le fichier `main.py`. Toutes les configurations doivent être effectuées dans le fichier `config.py`.
