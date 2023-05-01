#!/usr/bin/env python3
# -*- coding: utf-8 -*-`

"""This is an awesome python script!"""

import argparse

parser = argparse.ArgumentParser(description="This is an awesome python script!")
# parser.add_argument('argument', help='This is your argument')
args = parser.parse_args()

message_airspeed_demo = bytearray.fromhex("02 20 00 00 1D 80 42 03")


def create_message(gauge_type, gauge_value, checksum_type=0):
    """Create a c172hc message.

    Keyword arguments:
    gauge_type -- Gauge type
    gauge_value -- Gauge value
    checksum_type -- Checksum type

    The c172hc message looks like this: 0x02, gauge_type, gauge_value, checksum, 0x03

    The way the checksum is calculated can be controlled with "checksum_type".

    The following checksum types are supported:
    - 0 -> checksum w/o STX: 0xFF XOR gauge_type XOR gauge_value
    - 1 -> checksum w/ STX:  0xFF XOR 0x02 XOR gauge_type XOR gauge_value
    - 2 -> checksum w/o STX: 0xFF - (0xFF + gauge_type + gauge_value) + 1
    - 3 -> checksum w/ STX:  0xFF - (0xFF + 0x02 + gauge_type + gauge_value) + 1
    """
    message = bytearray(8)
    message[0] = 0x02
    message[1] = gauge_type
    message[2:6] = gauge_value.to_bytes(4, "big")

    if checksum_type == 0:
        message[6] = checksum_xor(message[1:6])
    elif checksum_type == 1:
        message[6] = checksum_xor(message[0:6])
    elif checksum_type == 2:
        message[6] = checksum_8bit(message[1:6])
    elif checksum_type == 3:
        message[6] = checksum_8bit(message[0:6])

    message[7] = 0x03
    return message.hex()


def checksum_xor(_message):
    """Calculate checksum for given message (XOR).

    Keyword argument:
    _message -- Message (bytearray) for which the checksum should be calculated

    The checksum is calculated by XOR each byte, starting with 0xFF
    """
    _checksum_xor = 0xFF
    for char in _message:
        _checksum_xor = _checksum_xor ^ char
    return _checksum_xor


def checksum_8bit(_message):
    """Calculate checksum for given message (8bit sum).

    Keyword argument:
    _message -- Message (bytearray) for which the checksum should be calculated

    The checksum is calculated by summing up each byte, starting with 0xFF.
    The sum is then 'trimmed' to 8bit and a two's complement is calculated.
    """
    _sum = 0xFF
    for char in _message:
        _sum += char
    _sum = _sum & 0xFF  # only use the lowest 8 Bit
    _sum = checksum_xor(_sum.to_bytes(1, "big")) + 1  # -sum is a two's complement
    return _sum


def print_all_checksums(value):
    """Print message with different checksum types."""
    print(
        "Value: "
        + str(value)
        + " / XOR-Checksum w/o  STX: "
        + create_message(0x20, value, 0)
    )
    # print("Value: "
    #    + str(value) + " / XOR-Checksum w.  STX: " + create_message(0x20, value, 1))
    print(
        "Value: "
        + str(value)
        + " / 8bit-Checksum w/o STX: "
        + create_message(0x20, value, 2)
    )
    print(
        "Value: "
        + str(value)
        + " / 8bit-Checksum w.  STX: "
        + create_message(0x20, value, 3)
    )


# checksum_xor(message_airspeed_demo)
# checksum_xor_stx(message_airspeed_demo)
# checksum_8bit(message_airspeed_demo)
# checksum_8bit_stx(message_airspeed_demo)
print("Airspeed Demo:        " + message_airspeed_demo.hex())

print_all_checksums(0)
print_all_checksums(102)
print_all_checksums(7552)
