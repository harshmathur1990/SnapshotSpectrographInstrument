# -*- coding: utf-8 -*-
import traceback
import sys
import serial.tools.list_ports
from utils import get_serial_connection
from constants import MIN_WAVELENGTH, MAX_WAVELENGTH


def configure_for_wavelength(int_wave):
    pass


def do_initialisation(serial_object):
    pass


def do_alignment(serial_object):
    pass


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

    do_alignment(serial_object)

    while 1:
        sys.stdout.write('Enter e for exit or wavelength in nm to tune:\n')
        raw_in = input()
        if raw_in.lower() == 'n':
            sys.stdout.write('You have chosen to exit. Thank you!\n')
            sys.exit(0)
        else:
            int_wave = None
            try:
                int_wave = int(raw_in)
                if not MIN_WAVELENGTH <= int_wave <= MAX_WAVELENGTH:
                    sys.stdout.write(
                        'The Valid Wavelength range are {} nm to {} nm'.format(
                            MIN_WAVELENGTH, MAX_WAVELENGTH
                        )
                    )
                    continue
            except Exception:
                sys.stdout.write('Wrong input.\n')
                continue
            configure_for_wavelength(int_wave)
            sys.stdout.write(
                'The FP is configured for {} nm Wavelength'.format(
                    int_wave
                )
            )


if __name__ == '__main__':
    main()
