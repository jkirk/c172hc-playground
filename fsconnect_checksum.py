#!/usr/bin/env python3
# -*- coding: utf-8 -*-`

"""This is an awesome python script!"""

import argparse

parser = argparse.ArgumentParser(description='This is an awesome python script!')
# parser.add_argument('argument', help='This is your argument')
args = parser.parse_args()

message_airspeed_demo = bytearray.fromhex('02 20 00 00 1D 80 42 03')

def create_message(gauge_type, gauge_value):
    message = bytearray(8)
    message[0] = 0x02
    message[1] = gauge_type
    message[2:6] = gauge_value.to_bytes(4, 'big')
    message[6] = checksum_xor(message[1:6])
    message[7] = 0x03
    print (message.hex())
    print (message_airspeed_demo.hex())

def checksum_xor(_message):
    _checksum_xor = 0xff
    for char in (_message.removeprefix(b'0x02')):
        _checksum_xor = _checksum_xor ^ char
    return _checksum_xor

def checksum_xor_stx(message):
    print (message_airspeed_demo)


def checksum_8bit(message):
    print (message_airspeed_demo)

def checksum_8bit_stx(message):
    print (message_airspeed_demo)

# checksum_xor(message_airspeed_demo)
# checksum_xor_stx(message_airspeed_demo)
# checksum_8bit(message_airspeed_demo)
# checksum_8bit_stx(message_airspeed_demo)
create_message(0x20, 7552)
