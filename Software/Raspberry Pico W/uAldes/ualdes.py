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

def decode_value(value,type):
    def decode_value(value, type):
        """
        Decodes a given value based on the specified type.

        Parameters:
            value (float or int): The input value to be decoded.
            type (int): The decoding type. Acceptable values are:
                - 0: Returns the value as is.
                - 1: Divides the value by 2.
                - 2: Multiplies the value by 0.5 and subtracts 20.
                - Any other value: Returns the value as is.

        Returns:
            float: The decoded value based on the specified type.
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
                    decoded_value = decode_value(data[properties["Index"]], properties["Type"])
                    # Store the decoded value in the dictionary
                    decoded_frame[item] = decoded_value

    else:
        decoded_frame = None
        print("Invalid frame")

    return decoded_frame


