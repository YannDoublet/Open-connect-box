# Installer un fichier `.elf` avec STM32CubeProgrammer

Ce guide explique comment installer un fichier `.elf` sur une carte STM32F411CEU6 à l'aide de STM32CubeProgrammer.

## Prérequis
1. Télécharger et installer [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html).
2. Un fichier `.elf` compilé pour la carte STM32F411CEU6.
3. Un câble USB pour connecter la carte STM32 à votre ordinateur.

## Étapes pour flasher le fichier `.elf`
1. **Connecter la carte STM32 :**
   - Branchez la carte STM32F411CEU6 à votre ordinateur via le câble USB.

2. **Lancer STM32CubeProgrammer :**
   - Ouvrez STM32CubeProgrammer sur votre ordinateur.
   - Assurez-vous que la carte est détectée dans l'onglet `Port`.

3. **Charger le fichier .elf :**
   - Cliquez sur le bouton `Open File` et sélectionnez votre fichier `.elf`.

4. **Configurer les options :**
   - Vérifiez que l'adresse de programmation est correcte (par défaut, elle devrait être configurée pour votre carte).
   - Sélectionnez les options de flash pour inclure uniquement le fichier `.elf`.

5. **Programmer la carte :**
   - Cliquez sur le bouton `Download` pour flasher le fichier sur la carte.
   - Attendez que le processus se termine avec succès.

6. **Vérifier l'installation :**
   - Une fois l'installation terminée, déconnectez et redémarrez la carte pour exécuter le programme.

## Dépannage
- Si la carte n'est pas détectée, assurez-vous qu'elle est en mode Bootloader (appuyez sur le bouton Boot0 tout en connectant la carte).
- Consultez la documentation officielle [STM32CubeProgrammer User Manual](https://www.st.com/resource/en/user_manual/dm00403560-stm32cubeprogrammer-software-description-stmicroelectronics.pdf) pour des informations supplémentaires.

---
