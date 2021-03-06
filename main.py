# -*- coding: utf-8 -*-
import traceback
import sys
import serial.tools.list_ports
from utils import get_serial_connection, send_to_serial_port
from constants import MIN_WAVELENGTH, MAX_WAVELENGTH


def configure_for_wavelength(serial_object, int_wave):
    ofsetted = off_code(int_wave)
    string_code = make_string(ofsetted)
    to_be_sent = "I4" + string_code + "P1P0"
    send_to_serial_port(serial_object, to_be_sent)
    send_to_serial_port(serial_object, "I0")


def do_initialisation(serial_object):
    send_to_serial_port('!QT')  # Set read ports.
    send_to_serial_port('P0')  # Ensure Buffers Disabled

    # Open X,Y and Z buffers, set ports J,K,L to zero, latch the data.
    send_to_serial_port('I7000P1P0')

    send_to_serial_port('I0')  # Close The Buffers
    send_to_serial_port('O3')  # Balance mode, but front panel has control.


def off_code(number):
    if number < -2048:
        number = -2048
    elif number > 2047:
        number = 2047

    number += 2048

    number = number ^ 0x800

    return number


def make_string(number):
    if number < 0:
        number = 0
    elif number > 4095:
        number = 4095

    num_hex = hex(number)

    num_hex = num_hex[2:]

    if len(num_hex) == 1:
        num_hex = '00' + num_hex
    elif len(num_hex) == 2:
        num_hex = '0' + num_hex

    return num_hex


def main():
    sys.stdout.write('Choose from Available Serial ports:\n')

    all_devices = serial.tools.list_ports.comports()

    for id, device in enumerate(all_devices):
        sys.stdout.write('{}.  {}\n'.format(id, device.device))

    int_id = None

    while (1):
        raw_id = input()
        try:
            int_id = int(raw_id)
            if 0 <= int_id < len(all_devices):
                break
            else:
                sys.stdout.write(
                    'Wrong input. Input only choice in integer.\n'
                )
                continue
        except Exception:
            sys.stdout.write('Wrong input. Input only choice in integer.\n')
            continue

    serial_object = None
    try:
        serial_object = get_serial_connection(
            all_devices, int_id
        )
    except Exception:
        err = traceback.format_exc()
        sys.stdout.write(err)
        sys.exit(1)

    do_initialisation(serial_object)

    while 1:
        sys.stdout.write('Enter e for exit or step from 0 to 2047:\n')
        raw_in = input()
        if raw_in.lower() == 'e' or raw_in.lower() == 'exit':
            sys.stdout.write('You have chosen to exit. Thank you!\n')
            sys.exit(0)
        else:
            int_wave = None
            try:
                int_wave = int(raw_in)
                if not MIN_WAVELENGTH <= int_wave <= MAX_WAVELENGTH:
                    sys.stdout.write(
                        'The Valid Step size are {} to {}.'.format(
                            MIN_WAVELENGTH, MAX_WAVELENGTH
                        )
                    )
                    continue
            except Exception:
                sys.stdout.write('Wrong input.\n')
                continue
            configure_for_wavelength(serial_object, int_wave)
            sys.stdout.write(
                'The FP is configured for {} step'.format(
                    int_wave
                )
            )


if __name__ == '__main__':
    main()
