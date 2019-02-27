import serial


def get_serial_connection(all_devices, id):

    ser = serial.Serial(
        all_devices[id].device,
        9600,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )

    return ser


def send_to_serial_port(serial_object, message):
    pass


def read_from_serial_port(serial_object):
    pass
