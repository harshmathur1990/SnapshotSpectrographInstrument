# -*- coding: utf-8 -*-
import serial.tools.list_ports
from utils import get_serial_connection


def main():
    print ('Choose from Available Serial ports:\n')
    print (list(serial.tools.list_ports.comports()))

    all_devices = serial.tools.list_ports.comports()

    for id, device in enumerate(all_devices):
        print ('{}.  {}\n'.format(id, device.device))

    int_id = None

    while (1):
        raw_id = input()
        try:
            int_id = int(raw_id)
            if 0 <= int_id < len(all_devices):
                break
            else:
                print ('Wrong input. Input only choice in integer.\n')
                continue
        except Exception:
            print ('Wrong input. Input only choice in integer.\n')
            continue

    serial_object = get_serial_connection(
        all_devices, int_id
    )


if __name__ == '__main__':
    main()
