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
    "Soft": {"Index": 4, "Type": 0, "Publish": True},
    "Entree_HC": {"Index": 9, "Type": 0, "Publish": True}, #3 => HC entrée non active / 7 => HC entrée active
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
    "Conso_eau": {"Index": 49, "Type": 100, "Publish": True},
    "Conso_ventil": {"Index": 41, "Type": 101, "Publish": True},
    "byte_01": {"Index": 1, "Type": 0, "Publish": True},
    "byte_02": {"Index": 2, "Type": 0, "Publish": True},
    "byte_03": {"Index": 3, "Type": 0, "Publish": True},
    "byte_05": {"Index": 5, "Type": 0, "Publish": True},
    "byte_07": {"Index": 7, "Type": 0, "Publish": True},
    "byte_08": {"Index": 8, "Type": 0, "Publish": True},
    "byte_09": {"Index": 9, "Type": 0, "Publish": True},
    "byte_10": {"Index": 10, "Type": 0, "Publish": True},
    "byte_11": {"Index": 11, "Type": 0, "Publish": True},
    "byte_12": {"Index": 12, "Type": 0, "Publish": True},
    "byte_13": {"Index": 13, "Type": 0, "Publish": True},
    "byte_14": {"Index": 14, "Type": 0, "Publish": True},
    "byte_15": {"Index": 15, "Type": 0, "Publish": True},
    "byte_16": {"Index": 16, "Type": 0, "Publish": True},
    "byte_17": {"Index": 17, "Type": 0, "Publish": True},
    "byte_18": {"Index": 18, "Type": 0, "Publish": True},
    "byte_19": {"Index": 19, "Type": 0, "Publish": True},
    "byte_20": {"Index": 20, "Type": 0, "Publish": True},
    "byte_21": {"Index": 21, "Type": 0, "Publish": True},
    "byte_22": {"Index": 22, "Type": 0, "Publish": True},
    "byte_23": {"Index": 23, "Type": 0, "Publish": True},
    "byte_24": {"Index": 24, "Type": 0, "Publish": True},
    "byte_25": {"Index": 25, "Type": 0, "Publish": True},
    "byte_26": {"Index": 26, "Type": 0, "Publish": True},
    "byte_27": {"Index": 27, "Type": 0, "Publish": True},
    "byte_30": {"Index": 30, "Type": 0, "Publish": True},
    "byte_31": {"Index": 31, "Type": 0, "Publish": True},
    "byte_35": {"Index": 35, "Type": 0, "Publish": True},
    "byte_41": {"Index": 41, "Type": 0, "Publish": True},
    "byte_42": {"Index": 42, "Type": 0, "Publish": True},
    "byte_43": {"Index": 43, "Type": 0, "Publish": True},
    "byte_44": {"Index": 44, "Type": 0, "Publish": True},
    "byte_45": {"Index": 45, "Type": 0, "Publish": True},
    "byte_46": {"Index": 46, "Type": 0, "Publish": True},
    "byte_47": {"Index": 47, "Type": 0, "Publish": True},
    "byte_48": {"Index": 48, "Type": 0, "Publish": True},
    "byte_49": {"Index": 49, "Type": 0, "Publish": True},
    "byte_50": {"Index": 50, "Type": 0, "Publish": True},
    "byte_51": {"Index": 51, "Type": 0, "Publish": True},
    "byte_52": {"Index": 52, "Type": 0, "Publish": True},
    "byte_53": {"Index": 53, "Type": 0, "Publish": True},
    "byte_54": {"Index": 54, "Type": 0, "Publish": True},
    "byte_55": {"Index": 55, "Type": 0, "Publish": True},
    "byte_56": {"Index": 56, "Type": 0, "Publish": True},
    "byte_57": {"Index": 57, "Type": 0, "Publish": True},
    "byte_58": {"Index": 58, "Type": 0, "Publish": True},
    "byte_59": {"Index": 59, "Type": 0, "Publish": True},
    "byte_60": {"Index": 60, "Type": 0, "Publish": True},
    "byte_61": {"Index": 61, "Type": 0, "Publish": True},
    "byte_62": {"Index": 62, "Type": 0, "Publish": True},
    "byte_63": {"Index": 63, "Type": 0, "Publish": True},
    "byte_64": {"Index": 64, "Type": 0, "Publish": True},
    "byte_65": {"Index": 65, "Type": 0, "Publish": True},
    "byte_66": {"Index": 66, "Type": 0, "Publish": True},
    "byte_67": {"Index": 67, "Type": 0, "Publish": True},
    "byte_68": {"Index": 68, "Type": 0, "Publish": True},
    "byte_69": {"Index": 69, "Type": 0, "Publish": True},
    "byte_70": {"Index": 70, "Type": 0, "Publish": True},
    "byte_71": {"Index": 71, "Type": 0, "Publish": True},
    "byte_72": {"Index": 72, "Type": 0, "Publish": True},
    "Test_type_0": {"Index": 39, "Type": 0, "Publish": False},
    "Test_type_1": {"Index": 39, "Type": 1, "Publish": False},
    "Test_type_2": {"Index": 39, "Type": 2, "Publish": False},
    "Test_type_3": {"Index": 39, "Type": 3, "Publish": False},
    "Test_type_4": {"Index": 39, "Type": 4, "Publish": False},
}





def aldes_checksum(data):
    """
        Returns the checksum of the data.
        The checksum is the last byte of the data, and is calculated as the 2's complement of the sum of all previous bytes.
        The checksum is valid if the sum of all bytes (including the checksum) is equal to 0x00.
        :param data: list of integers (bytes)
        :return: checksum of the data
    """

    checksum = -sum(data[:-1]) & 0xFF
    return checksum

def aldes_checksum_test(data):
    """
    Verify the ALDES checksum of a data packet.

    The ALDES checksum is calculated by summing all bytes except the last one, 
    negating the sum, and taking the least significant byte (modulo 256). 
    The checksum is valid if this calculated value equals the last byte of the data.

    Parameters
    ----------
    data : list or bytes
        The data packet including the checksum as the last byte.

    Returns
    -------
    bool
        True if the checksum matches, False otherwise.

    Notes
    -----
    The function also prints "Checksum OK" if the checksum is valid, 
    or "Checksum KO" if it is invalid.
    """

    if (-sum(data[:-1]) & 0xFF) == data[-1]:
        print("Checksum OK")
        return True
    else:
        print("Checksum KO")
        return False

def frame_encode(command):
    """
    Encodes a JSON command into a specific frame format for UART communication.
    
    This function takes a JSON string command, parses it to extract the frame type
    and parameters, then creates a properly formatted byte array according to the
    specified protocol. It also calculates and appends the appropriate checksum.
    
    Parameters:
    -----------
    command : str
        A JSON string containing the command type and parameters.
        Expected format: {"type": "<command_type>", "params": {...}}
        
        Supported command types:
        - "auto": Sets the device to automatic mode
        - "boost": Sets the device to boost mode
        - "confort": Sets the device to comfort mode with specified duration in days
        - "vacances": Sets the device to vacation mode with specified duration in days
        - "temp": Sets a specific temperature
        - "debug": Sets a debug mode with specified duration
        
        Parameters vary by command type:
        - "confort": {"duration": int} (days, default: 2)
        - "vacances": {"duration": int} (days, default: 10)
        - "temp": {"temperature": float} (degrees Celsius)
        - "debug": {"duration": int} (default: 1)
    
    Returns:
    --------
    list or None
        A list of integers representing the encoded frame bytes if successful,
        or None if the command parsing fails.
        
    Format of returned frame:
    [0xFD, 0xA0, 0x09, 0xA0, temp_byte, cmd_byte, param1, param2, 0x9F, checksum]
    
    Example:
    --------
    >>> frame_encode('{"type": "auto"}')
    [253, 160, 9, 160, 255, 1, 255, 255, 159, 117]
    
    >>> frame_encode('{"type": "temp", "params": {"temperature": 20.5}}')
    [253, 160, 9, 160, 41, 255, 255, 255, 159, 75]
    """

    try:
        # Decode the JSON command
        command_data = json.loads(command)

        # Extract the frame type and parameters
        frame_type = command_data.get("type")
        params = command_data.get("params", {})

        # Define the base frame structure
        base_frame = [0xFD, 0xA0, 0x09, 0xA0, 0xFF, 0xFF, 0xFF, 0xFF, 0x9F]

        # Modify the frame based on the type and parameters
        if frame_type == "auto":
            base_frame[5] = 0x01
        elif frame_type == "boost":
            base_frame[5] = 0x02
        elif frame_type == "confort":
            base_frame[5] = 0x03
            base_frame[6] = 0x00
            base_frame[7] = params.get("duration", 0x02) # int in days
        elif frame_type == "vacances":
            base_frame[5] = 0x04
            base_frame[6] = 0x00
            base_frame[7] = params.get("duration", 0x0A) # int in days
        elif frame_type == "temp":
            base_frame[4] = int(params.get("temperature", 0x85)*2) # float in °C
        elif frame_type == "debug":
            base_frame[5] = params.get("duration", 0x01)

        # Calculate the checksum
        checksum = -sum(base_frame) & 0xFF
        base_frame.append(checksum)
        return base_frame

    except :
        print("Invalid command")
        return None

def decode_value(value, type, data=None, index=None):
    """
    Decode a value based on its type.
    type:
    - 0: No processing
    - 1: Divide by 2
    - 2: Multiply by 0.5 then subtract 20
    - 3: Multiply by 10
    - 4: Multiply by 2 then subtract 1
    - 100: Special processing for conso_eau
    - 101: Special processing for conso_ventil
    """
    if type == 0:
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
            valeur_finale = valeur_brute + 657

            return round(valeur_finale, 3)
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
                byte_41 * coeffs[0] -1,
                byte_42 * coeffs[1] -1,
                byte_43 * coeffs[2] -1,
                byte_44 * coeffs[3] -1
            ]
            valeur_brute = sum(valeurs)
            valeur_finale = valeur_brute

            return round(valeur_finale, 3)
        except IndexError:
            return None
    else:
        return value



def frame_decode(data):
    """
    Decodes a given data frame into a dictionary of interpreted values.

    The function checks the validity of the input data frame using a checksum test.
    If the frame is valid, it decodes the values based on predefined mappings and types.
    If the frame is invalid, it sets the "Etat" key in the decoded frame to 0 and prints an error message.

    Args:
        data (list): A list of integers representing the data frame to be decoded.

    Returns:
        dict: A dictionary containing the decoded values. If the frame is invalid, the dictionary
              will contain only the key "Etat" with a value of 0.
    """

    decoded_frame = {}

    # Check if the frame is valid
    if aldes_checksum_test(data):
        for item, properties in ITEMS_MAPPING.items():
            # Decode the value based on its type
            if properties["Publish"]:
                if item == "Soft":
                    decoded_frame[item] = f"{data[properties['Index']]:02X}"
                else:
                    # Decode the value using the decode_value function
                    # decoded_value = decode_value(data[properties["Index"]], properties["Type"])
                    # decoded_value = decode_value(data[properties["Index"]], properties["Type"], data, properties["Index"])
                    decoded_value = decode_value(data[properties["Index"]], properties["Type"], data, properties["Index"])


                    # Store the decoded value in the dictionary
                    decoded_frame[item] = decoded_value

    else:
        decoded_frame = None
        print("Invalid frame")

    return decoded_frame


