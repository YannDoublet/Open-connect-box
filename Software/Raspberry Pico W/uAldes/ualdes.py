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
Version: 1.1.0
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

    # --- Nouveaux compteurs (W·min -> kWh = raw / 60000) ---
    "Conso_vmc": {"Index": 41, "Type": 110, "Publish": True},           # Compteur 1 : b[41..44]
    "Conso_pac": {"Index": 49, "Type": 111, "Publish": True},           # Compteur 2 : b[49..52]
    "Conso_resistance": {"Index": 57, "Type": 112, "Publish": True},    # Compteur 3 : b[57..60]
    "Conso_totale": {"Index": 0, "Type": 113, "Publish": True},         # Somme (calculée)
    "Conso_eau": {"Index": 0, "Type": 114, "Publish": True},            # Somme (calculée)
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

def _u32_le(data, index):
    """Decode 32-bit little-endian unsigned int from data[index:index+4]."""
    return data[index] + (data[index + 1] << 8) + (data[index + 2] << 16) + (data[index + 3] << 24)

def _wmin_to_kwh(wmin):
    """Convert Watt-minutes (W·min) to kWh."""
    return wmin / 60000.0

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

    # --- Nouveaux compteurs en W·min ---
    elif type in (110, 111, 112) and data is not None and index is not None:
        # 110: Conso_vmc  -> Compteur 1 (b[41..44])
        # 111: Conso_pac  -> Compteur 2 (b[49..52])
        # 112: Conso_resistance -> Compteur 3 (b[57..60])
        try:
            raw_wmin = _u32_le(data, index)
            return round(_wmin_to_kwh(raw_wmin), 3)
        except IndexError:
            return None

    # Sommes calculées (nécessitent les 3 compteurs déjà décodés)
    elif type in (113, 114) and data is not None:
        try:
            c_vmc = _wmin_to_kwh(_u32_le(data, 41))
            c_pac = _wmin_to_kwh(_u32_le(data, 49))
            c_res = _wmin_to_kwh(_u32_le(data, 57))

            if type == 113:  # Conso_totale
                return round(c_vmc + c_pac + c_res, 3)
            else:            # 114: Conso_eau
                return round(c_pac + c_res, 3)
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