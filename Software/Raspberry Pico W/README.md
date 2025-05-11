---

# Installation du Firmware MicroPython sur le Raspberry Pi Pico W et les fichiers python

Ce guide vous explique comment installer le firmware MicroPython sur un Raspberry Pi Pico W et comment ajouter des fichiers Python disponibles dans le dossier `uAldes`.

---

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants :

- Un Raspberry Pi Pico W.
- Un câble micro-USB.
- Un ordinateur (Windows, macOS ou Linux).
- Le fichier firmware MicroPython (par exemple, `RPI_PICO_W-20250415-v1.25.0.uf2`) disponible dans le dossier.
- Un éditeur de code ou un IDE supportant MicroPython (comme [Thonny](https://thonny.org/)).

---

## Étapes d'installation du Firmware MicroPython

### 1. Téléchargez le Firmware

1. Téléchargez le fichier firmware MicroPython `RPI_PICO_W-20250415-v1.25.0.uf2`.

### 2. Installez le Firmware sur le Pico W

1. Connectez le Raspberry Pi Pico W à votre ordinateur tout en maintenant le bouton **BOOTSEL** enfoncé.
2. Une fois connecté, le Pico W apparaîtra comme un périphérique de stockage USB nommé `RPI-RP2`.
3. Glissez-déposez le fichier `RPI_PICO_W-20250415-v1.25.0.uf2` téléchargé dans le répertoire `RPI-RP2`.
4. Après la copie, le Pico W redémarrera automatiquement avec MicroPython installé.

---

## Ajouter des Fichiers Python depuis le Dossier `uAldes`

### 1. Connectez-vous au Pico W

1. Ouvrez un éditeur de code ou un IDE compatible MicroPython (par exemple, Thonny).
2. Configurez Thonny pour qu'il utilise MicroPython sur Raspberry Pi Pico W :
   - Allez dans **Outils > Options > Interpréteur**.
   - Sélectionnez **MicroPython (Raspberry Pi Pico)**.
   - Connectez-vous au port série correspondant.

### 2. Téléchargez les Fichiers Python

1. Accédez au dossier `uAldes` de ce dépôt.
2. Téléchargez les fichiers Python nécessaires.

### 3. Transférez les Fichiers vers le Pico W

1. Dans Thonny, ouvrez chaque fichier Python téléchargé.
2. Enregistrez chaque fichier sur le Pico W :
   - Allez dans **Fichier > Enregistrer sous**.
   - Sélectionnez **MicroPython device** comme destination.
3. Répétez ces étapes pour tous les fichiers nécessaires.

---

## Ressources supplémentaires

- [Documentation officielle MicroPython](https://micropython.org/)
- [Guide Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/)
- [Télécharger Thonny](https://thonny.org/)

---
