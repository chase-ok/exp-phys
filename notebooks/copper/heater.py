
from numpy import *
from matplotlib.pyplot import *
from contextlib import contextmanager
from serial import Serial
import time
import visa

@contextmanager
def open_heater(com_port='COM5'):
    serial = Serial(com_port, 19200)
    try:
        time.sleep(0.5) # gotta wait for PicoBlocks

        class Heater(object):
            def turn_on(self): serial.write(bytearray([1]))
            def turn_off(self): serial.write(bytearray([2]))
        yield Heater()
    finally:
        serial.close()

@contextmanager
def open_power_meter(ammeter_id='9', voltmeter_id='7'):
    ammeter = visa.instrument("GPIB::{0}".format(ammeter_id))
    voltmeter = visa.instrument("GPIB::{0}".format(voltmeter_id))

    try:
        for instr in [ammeter, voltmeter]:
            instr.write('G1')
            instr.write('X')

        class PowerMeter(object):
            def read_power(self):
                voltage = float(voltmeter.read())
                current = float(ammeter.read())
                return abs(voltage*current)
        yield PowerMeter()
    finally:
        for instr in [ammeter, voltmeter]:
            try: instr.close()
            except Exception as e: print e

if __name__ == '__main__':
    #with open_heater() as heater:
    #    heater.turn_on(); print 'heater on'
    #    time.sleep(5)
    #    heater.turn_off(); print 'heater off'
    with open_power_meter() as power_meter, open_heater() as heater:
        heater.turn_on(); print 'heater on'
        for _ in range(10):
            print power_meter.read_power(), 'W'
            #time.sleep(0.1)
        heater.turn_off(); print 'heater off'
        for _ in range(10):
            print power_meter.read_power(), 'W'
            #time.sleep(0.1)