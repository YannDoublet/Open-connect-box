
# Passerelle USB pour Chauffe-eau TFlow Aldes

Ce projet propose une passerelle USB permettant d'interfacer un chauffe-eau TFlow de la marque **Aldes** avec un système domotique basé sur le protocole **MQTT**. L'objectif est de permettre le contrôle à distance du chauffe-eau, la collecte de données et l'automatisation de certaines fonctions dans un environnement domotique.

---

## Hardware

### 1. Carte BLACKPILL (STM32)
- Convertit les trames reçues/envoyées au chauffe-eau.
- Transfère les données via UART à la carte Raspberry Pi Pico W.

### 2. Carte Raspberry Pi Pico W
- Gère la connexion WiFi, le protocole MQTT et le décodage des trames reçues de la carte STM32.

### 3. Boitier
- Boitier référence 1551WTFLBK de chez HAMMOND pour intégrer le pcb,la carte STM32 et la Pico W

---

## Schéma & PCB

- **Schéma** : ![Schéma électronique](Hardware/Schéma.pdf)
- **PCB** : ![PCB](Hardware/Pcb.jpg)
- **Boitier** : ![Boitier](Hardware/1551WTFLBK.pdf)

---

## Software

### 1. Carte BLACKPILL (STM32F401)
- Programmée en C via l'IDE STMicroelectronics.

### 2. Carte Raspberry Pi Pico W
- Programmée en MicroPython.

---

## Commandes MQTT

Ce document explique comment utiliser les commandes MQTT pour piloter votre système Aldes via la passerelle UART/MQTT, ainsi que la personnalisation des commandes envoyées par défaut.

### 1. Commandes reçues via MQTT (`home/device/command`)

Pour piloter votre système, publiez une commande JSON sur le topic :

```
home/device/command
```

#### Format général

Chaque commande doit être une chaîne JSON, par exemple :

```json
{"type": "auto"}
```

#### Commandes supportées
```
| Type de commande | Exemple de payload JSON                                 | Effet                                      |
|------------------|--------------------------------------------------------|--------------------------------------------|
| auto             | `{"type": "auto"}`                                     | Passe en mode automatique                  |
| boost            | `{"type": "boost"}`                                    | Active le mode boost                       |
| confort          | `{"type": "confort", "params": {"duration": 2}}`       | Mode confort pour X jours (défaut : 2)     |
| vacances         | `{"type": "vacances", "params": {"duration": 10}}`     | Mode vacances pour X jours (défaut : 10)   |
| temp             | `{"type": "temp", "params": {"temperature": 20.5}}`    | Définit la température cible (en °C)       |
```
> **Remarque :**  
> Les paramètres (`params`) sont optionnels selon la commande.  
> Le format exact et les effets dépendent de l’implémentation dans `ualdes.py`.

---

### 2. Données envoyées par MQTT (UART → MQTT)

Les trames reçues du système Aldes sont :
- **Publiées brutes (hexadécimal)** sur :
  ```
  home/device/trame
  ```
- **Décodées et publiées** sur des topics individuels, par exemple :
  ```
  home/device/Etat
  home/device/T_vmc
  ```
  (selon la configuration dans `ITEMS_MAPPING` de `ualdes.py`)

Seuls les paramètres avec `"Publish": True` dans `ITEMS_MAPPING` sont publiés.

---

### 3. Personnalisation avancée

Pour ajouter ou modifier les paramètres publiés, éditez le dictionnaire `ITEMS_MAPPING` dans `ualdes.py` :

```python
ITEMS_MAPPING = {
    "Etat": {"Index": 6, "Type": 0, "Publish": True},
    "T_vmc": {"Index": 33, "Type": 2, "Publish": True},
    # ...
}
```

Pour toute adaptation du protocole ou des commandes, modifiez la fonction `frame_encode()` dans `ualdes.py`.

---

## Avertissement

Ce projet n'a pas de but commercial et est fourni **en l'état**.  
L'auteur se dégage de toute responsabilité en cas de dommages directs ou indirects liés à l'utilisation de ce projet, y compris mais sans se limiter aux problèmes techniques, matériels, ou de sécurité qui pourraient survenir lors de l'utilisation de cette passerelle avec un chauffe-eau TFlow.

> Il est fortement recommandé de toujours consulter les documents techniques officiels d'Aldes avant d'interagir avec le chauffe-eau, et d'effectuer des tests dans un environnement contrôlé.

---

## Contribuer

Les contributions à ce projet sont les bienvenues !  
Si vous souhaitez contribuer, veuillez ouvrir une issue ou soumettre une pull request.  
Assurez-vous de respecter les bonnes pratiques de développement et de documentation.
```
