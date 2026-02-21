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
from config import UALDES_OPTIONS
"""
UAldes - Python library for Aldes UART Protocol

This library provides functions for encoding and decoding frames
used to communicate with Aldes ventilation systems over UART.
It handles command creation, checksum calculation, and data interpretation
for various device operations such as mode switching and temperature control.

Author: Yann DOUBLET
License: MIT
"""
RELEASE_DATE = "02_02_2026"
VERSION = "1.3"
# VERSION 1.3 implement EASYHOME VMC

if UALDES_OPTIONS["device"] == "T.Flow":
    ITEMS_MAPPING = {
        "Soft":         {"Index": 4, "Type": 5, "Publish": True},
        "Etat":         {"Index": 6, "Type": 0, "Publish": True},
        "Comp_C":       {"Index": 28, "Type": 1, "Publish": True},
        "Comp_R":       {"Index": 29, "Type": 1, "Publish": True},
        "T_hp":         {"Index": 32, "Type": 2, "Publish": True},
        "T_vmc":        {"Index": 33, "Type": 2, "Publish": True},
        "T_evap":       {"Index": 34, "Type": 2, "Publish": True},
        "T_haut":       {"Index": 36, "Type": 2, "Publish": True},
        "T_bas":        {"Index": 37, "Type": 2, "Publish": True},
        "DP":           {"Index": 38, "Type": 0, "Publish": True},
        "Ventil_flow":  {"Index": 39, "Type": 4, "Publish": True},
        "Ventil_rpm":   {"Index": 40, "Type": 3, "Publish": True},
    }
    # Define the base frame structure
    base_frame = [0xFD, 0xA0, 0x09, 0xA0, 0xFF, 0xFF, 0xFF, 0xFF, 0x9F]
elif UALDES_OPTIONS["device"] == "EASYHOME":
    ITEMS_MAPPING = {
        "Slave":        {"Index": 0, "Type": 0, "Publish": False},
        "Data_Lenght":  {"Index": 2, "Type": 0, "Publish": False},
        "StartPattern": {"Index": 3, "Type": 0, "Publish": False},
        "PwmQAI_1": 	{"LSB_Index": 8, "MSB_Index": 9, "Type": 10, "Publish": True},
        "Mode":         {"Index": 10, "Type": 7, "Publish": True},
        "Temp_Kitchen": {"Index": 14, "Type": 6, "Publish": True},
        "Hum_Kitchen":  {"Index": 15, "Type": 0, "Publish": True},
        "Temp_Bath1":   {"Index": 16, "Type": 6, "Publish": True},
        "Hum_Bath1":    {"Index": 17, "Type": 0, "Publish": True},
        "Temp_Bath2":   {"Index": 18, "Type": 6, "Publish": True},
        "Hum_Bath2":    {"Index": 19, "Type": 0, "Publish": True},
        "CO2": 		    {"LSB_Index": 20, "MSB_Index": 21, "Type": 10, "Publish": True},
        "Hum_Variat":   {"Index": 23, "Type": 0, "Publish": True},
        "PwmQAI_2": 	{"LSB_Index": 24, "MSB_Index": 25, "Type": 10, "Publish": False},
        "EndPattern":   {"Index": 26, "Type": 0, "Publish": False},
    }
    FRAME_INFO = {
            "TX_MASTER_IDENTIFIER" : 0xFD,
            "TX_SLAVE_IDENTIFIER" : 0x87,
            "RX_MASTER_IDENTIFIER" : 0x87,
            "RX_SLAVE_IDENTIFIER" : 0x00
    }
    # Define the base frame structure
    base_frame = [0xFD, 0x87, 0x11, 0x4B, 0x02, 0x02, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x4A]
else:
    print(f"Configuration error: UALDES_OPTIONS[\"device\"] set to ", UALDES_OPTIONS["device"])

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
        if UALDES_OPTIONS["device"] == "T.Flow":
            # Decode the JSON command
            command_data = json.loads(command)

            # Extract the frame type and parameters
            frame_type = command_data.get("type")
            params = command_data.get("params", {})

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
        elif UALDES_OPTIONS["device"] == "EASYHOME":
            frame_type = command
            if frame_type == b'Programming':
                base_frame[8] = 0x10
            elif frame_type == b'Holiday':
                base_frame[8] = 0x21
            elif frame_type == b'Daily':
                base_frame[8] = 0x43
            elif frame_type == b'Boost':
                base_frame[8] = 0x65
            elif frame_type == b'Guest':
                base_frame[8] = 0x87
            else:
                print("Error: unknown command: ", command)

        # Calculate the checksum
        checksum = -sum(base_frame) & 0xFF
        base_frame.append(checksum)
        return base_frame

    except :
        print("Invalid command")
        return None

def decode_temperature_bcd(value):
    """
    Decodes a temperature value encoded with BCD (Binary Coded Decimal) 
    and 0.25°C precision using the 2 least significant bits.
    
    The temperature is encoded as follows:
    - The 2 least significant bits (bits 0-1) represent the decimal part: 
      0b00 = 0.00°C, 0b01 = 0.25°C, 0b10 = 0.50°C, 0b11 = 0.75°C
    - The remaining bits (bits 2-7) are shifted right by 2 and decoded as BCD
      for the integer part of the temperature.
    
    Parameters:
        value (int): The encoded temperature byte (0x00 to 0xFF).
    
    Returns:
        float: The decoded temperature in degrees Celsius.
    
    Example:
        >>> decode_temperature_bcd(0x62)  # Binary: 0110 0010
        18.5
        # Bits 0-1: 0b10 = 2 -> 2 x 0.25 = 0.5°C
        # Bits 2-7: 0x62 >> 2 = 0x18 -> BCD 18 = 18°C
        # Result: 18 + 0.5 = 18.5°C
    """
    
    # Extract the 2 least significant bits for decimal part
    decimal_bits = value & 0b11
    decimal_part = decimal_bits * 0.25
    
    # Shift right by 2 bits to get the BCD encoded integer part
    bcd_value = value >> 2
    
    # Decode BCD: extract tens and units
    tens = (bcd_value >> 4) & 0x0F
    units = bcd_value & 0x0F
    integer_part = tens * 10 + units
    
    # Combine integer and decimal parts
    temperature = integer_part + decimal_part
    
    return temperature

def decode_value(value,type):
    """
    Decodes a numeric value based on the specified type and returns it as a string.

    Parameters:
        value (numeric): The value to be decoded.
        type (int): The decoding type to apply:
            0: Return as is
            1: Divide by 2
            2: Multiply by 0.5 and subtract 20 (temperature conversion)
            3: Multiply by 10
            4: Multiply by 2 and subtract 1
            5: Convert to hexadecimal and return last 2 characters
            other: Return as is
            6: Decode as BCD temperature with 0.25°C precision
            7: Decode as Mode (43 => Daily, 87 => Guest, 65 => Boost, 21 => Holiday, 10 => Programming)


    Returns:
        str: The decoded value as a string.
    """

    if type == 0:
        return str(value)
    elif type == 1:
        return str(value / 2)
    elif type == 2:
        return str(value * 0.5 - 20)
    elif type == 3: 
        return str(value * 10)
    elif type == 4:
        return str(value * 2-1)
    elif type == 5:
        return str(hex(value)[-2:])
    elif type == 6:
        return str(decode_temperature_bcd(value))
    elif type == 7:
        if value == 0x43:
            return "\"Daily\""
        elif value == 0x87:
            return "\"Guest\""
        elif value == 0x65:
            return "\"Boost\""
        elif value == 0x21:
            return "\"Holiday\""
        elif value == 0x10:
            return "\"Programming\""
        else:
            return "\"Unknown\""
    else:
        return str(value)

def decode_value_double(value_MSB,value_LSB, type):
    """
    Decodes a numeric value encoded as a double and returns it as a string.

    Parameters:
        value_MSB (numeric): MSB of the value to be decoded.
        value_LSB (numeric): LSB of the value to be decoded.
        type (int): The decoding type to apply:
            0: Return as is

    Returns:
        str: The decoded value as a string.
    """

    if type == 10:
        return str(value_MSB*256+value_LSB)
    else:
        return str(value_MSB*256+value_LSB)

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
                # Decode the value using the decode_value function
                # Check if it is a double or not
                if properties["Type"] == 10:
                    decoded_value = decode_value_double(data[properties["MSB_Index"]], data[properties["LSB_Index"]], properties["Type"])
                else:
                    decoded_value = decode_value(data[properties["Index"]], properties["Type"])
                # Store the decoded value in the dictionary
                decoded_frame[item] = decoded_value

    else:
        decoded_frame = None
        print("Invalid frame", data)

    return decoded_frame


