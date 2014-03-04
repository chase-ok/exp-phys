
from numpy import *
from matplotlib.pyplot import *
from contextlib import contextmanager
from serial import Serial
import time

thermoCalibration = array([[-9.835,-9.797,-9.719,-9.604,-9.455,-9.274,-9.063,-8.824,-8.561,-8.273,-7.963,-7.631,-7.279,-6.907,-6.516,-6.107,-5.680,-5.237,-4.777,-4.301,-3.811,-3.306,-2.787,-2.254,-1.709,-1.151,-0.581,0.000,0.591,1.192,1.801,2.419,3.047,3.683,4.329,4.983,5.646,6.317,6.998,7.685,8.379,9.081,9.789,10.503,11.224,11.951,12.684,13.421,14.164],
                           [-270,-260,-250,-240,-230,-220,-210,-200,-190,-180,-170,-160,-150,-140,-130,-120,-110,-100, -90, -80, -70, -60, -50, -40, -30, -20, -10,   0,  10,  20,  30,  40,  50,  60,  70,  80,  90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]])

def voltageToTemperature(voltage):
    return interp(voltage, thermoCalibration[0,:], thermoCalibration[1,:])

@contextmanager
def open_heater(com_port='COM5'):
    serial = Serial(com_port, 19200)
    time.sleep(0.5) # gotta wait for PicoBlocks

    class Heater(object):
        def turn_on(self): serial.write(bytearray([1]))
        def turn_off(self): serial.write(bytearray([2]))
    yield Heater()

    serial.close()


if __name__ == '__main__':
    with open_heater() as heater:
        heater.turn_on(); print 'heater on'
        time.sleep(5)
        heater.turn_off(); print 'heater off'