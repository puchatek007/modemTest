import smbus2
from smbus2 import i2c_msg
import time


def calc_temp(data):
    temp_data = data[0] * 256 + data[1]
    temp = -45 + 175 * temp_data / 65535
    return round(temp, 2)


class Temperature:
    def __init__(self, bus=None):
        if bus is None:
            self.bus = smbus2.SMBus(0)
        else:
            self.bus = bus.bus_return()
        self.device_address = 0x46
        self.data_option = 0xFD
        self.data_serial = 0x89

    def get_temperature(self):
        send_msg = i2c_msg.write(self.device_address, [self.data_option])
        self.bus.i2c_rdwr(send_msg)

        time.sleep(0.01)

        read_msg = i2c_msg.read(self.device_address, 6)
        self.bus.i2c_rdwr(read_msg)

        data = list(read_msg)
        temp = calc_temp(data)

        return int(temp)

    def get_serial(self):
        send_msg = i2c_msg.write(self.device_address, [self.data_serial])
        self.bus.i2c_rdwr(send_msg)

        time.sleep(0.01)

        read_msg = i2c_msg.read(self.device_address, 6)
        self.bus.i2c_rdwr(read_msg)

        data = list(read_msg)

        first_word = data[:2]
        second_word = data[2:4]

        first_number = int.from_bytes(bytearray(first_word), byteorder='big')
        second_number = int.from_bytes(bytearray(second_word), byteorder='big')
        serial_number = (first_number << 16) + second_number

        return serial_number


if __name__ == "__mian__":
    print("start")
    temp = Temperature(1)
    print("pobranie temp")
    print(temp.get_serial())
    print("numer seryjny")
    print(temp.get_temperature())
    print("temperratura")