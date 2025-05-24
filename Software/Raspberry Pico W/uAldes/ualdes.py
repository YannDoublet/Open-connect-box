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

import json

"""
UAldes - Python library for Aldes UART Protocol

This library provides functions for encoding and decoding frames
used to communicate with Aldes ventilation systems over UART.
It handles command creation, checksum calculation, and data interpretation
for various device operations such as mode switching and temperature control.

Author: Yann DOUBLET
License: MIT
Version: 1.0.0
"""

ITEMS_MAPPING = {
    "Soft": {"Index": 4, "Type": -1, "Publish": True},
    "Entree_HC": {"Index": 9, "Type": 0, "Publish": True},
    "Etat": {"Index": 6, "Type": 0, "Publish": True},
    "Comp_C": {"Index": 28, "Type": 1, "Publish": True},
    "Comp_R": {"Index": 29, "Type": 1, "Publish": True},
    "T_hp": {"Index": 32, "Type": 2, "Publish": True},
    "T_vmc": {"Index": 33, "Type": 2, "Publish": True},
    "T_evap": {"Index": 34, "Type": 2, "Publish": True},
    "T_haut": {"Index": 36, "Type": 2, "Publish": True},
    "T_bas": {"Index": 37, "Type": 2, "Publish": True},
    "DP": {"Index": 38, "Type": 0, "Publish": True},
    "Ventil_flow": {"Index": 39, "Type": 4, "Publish": True},
    "Ventil_rpm": {"Index": 40, "Type": 3, "Publish": True},
    "Conso_ventil": {"Index": 41, "Type": 101, "Publish": True},
    "Conso_eau": {"Index": 49, "Type": 100, "Publish": True},
}

# Auto-génération des byte_01 à byte_73 et leur version hex brute
for i in range(1, 74):
    key = f"byte_{i:02d}"
    key_raw = f"byte_{i:02d}_raw"
    ITEMS_MAPPING[key] = {"Index": i, "Type": 0, "Publish": True}      # Valeur décodée
    ITEMS_MAPPING[key_raw] = {"Index": i, "Type": -1, "Publish": True}  # Hex brute

def aldes_checksum(data):
    return -sum(data[:-1]) & 0xFF

def aldes_checksum_test(data):
    if (-sum(data[:-1]) & 0xFF) == data[-1]:
        print("Checksum OK")
        return True
    else:
        print("Checksum KO")
        return False

def frame_encode(command):
    try:
        command_data = json.loads(command)
        frame_type = command_data.get("type")
        params = command_data.get("params", {})
        base_frame = [0xFD, 0xA0, 0x09, 0xA0, 0xFF, 0xFF, 0xFF, 0xFF, 0x9F]

        if frame_type == "auto":
            base_frame[5] = 0x01
        elif frame_type == "boost":
            base_frame[5] = 0x02
        elif frame_type == "confort":
            base_frame[5] = 0x03
            base_frame[6] = 0x00
            base_frame[7] = params.get("duration", 0x02)
        elif frame_type == "vacances":
            base_frame[5] = 0x04
            base_frame[6] = 0x00
            base_frame[7] = params.get("duration", 0x0A)
        elif frame_type == "temp":
            base_frame[4] = int(params.get("temperature", 0x85) * 2)
        elif frame_type == "debug":
            base_frame[5] = params.get("duration", 0x01)

        checksum = -sum(base_frame) & 0xFF
        base_frame.append(checksum)
        return base_frame
    except:
        print("Invalid command")
        return None

def decode_value(value, type, data=None, index=None):
    if type == -1:
        return f"{value:02X}"
    elif type == 0:
        return value
    elif type == 1:
        return value / 2
    elif type == 2:
        return value * 0.5 - 20
    elif type == 3:
        return value * 10
    elif type == 4:
        return value * 2 - 1
    elif type == 100 and data is not None and index is not None:
        try:
            byte_49 = data[index]
            byte_50 = data[index + 1]
            byte_51 = data[index + 2]
            byte_52 = data[index + 3]
            coeffs = [0.0000152587890625, 0.00390625, 1, 256]
            valeurs = [
                byte_49 * coeffs[0],
                byte_50 * coeffs[1],
                byte_51 * coeffs[2],
                byte_52 * coeffs[3]
            ]
            valeur_brute = sum(valeurs)
            return round(valeur_brute + 657, 3)
        except IndexError:
            return None
    elif type == 101 and data is not None and index is not None:
        try:
            byte_41 = data[index]
            byte_42 = data[index + 1]
            byte_43 = data[index + 2]
            byte_44 = data[index + 3]
            coeffs = [0.0000152587890625, 0.00390625, 1, 256]
            valeurs = [
                byte_41 * coeffs[0] + 24,
                byte_42 * coeffs[1] + 24,
                byte_43 * coeffs[2] + 24,
                byte_44 * coeffs[3] + 24
            ]
            valeur_brute = sum(valeurs)
            return round(valeur_brute, 3)
        except IndexError:
            return None
    else:
        return value

def frame_decode(data):
    decoded_frame = {}
    if aldes_checksum_test(data):
        for item, properties in ITEMS_MAPPING.items():
            if properties["Publish"]:
                decoded_value = decode_value(
                    data[properties["Index"]],
                    properties["Type"],
                    data,
                    properties["Index"]
                )
                decoded_frame[item] = decoded_value
    else:
        decoded_frame = None
        print("Invalid frame")
    return decoded_frame
