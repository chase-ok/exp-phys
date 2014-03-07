
from numpy import *
from matplotlib.pyplot import *
from contextlib import contextmanager
import time
import visa

thermoCalibration = array([[-9.835,-9.797,-9.719,-9.604,-9.455,-9.274,-9.063,-8.824,-8.561,-8.273,-7.963,-7.631,-7.279,-6.907,-6.516,-6.107,-5.680,-5.237,-4.777,-4.301,-3.811,-3.306,-2.787,-2.254,-1.709,-1.151,-0.581,0.000,0.591,1.192,1.801,2.419,3.047,3.683,4.329,4.983,5.646,6.317,6.998,7.685,8.379,9.081,9.789,10.503,11.224,11.951,12.684,13.421,14.164],
                           [-270,-260,-250,-240,-230,-220,-210,-200,-190,-180,-170,-160,-150,-140,-130,-120,-110,-100, -90, -80, -70, -60, -50, -40, -30, -20, -10,   0,  10,  20,  30,  40,  50,  60,  70,  80,  90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210]])

def voltageToTemperature(voltage):
    milli = voltage*1000
    deg_c = interp(milli, thermoCalibration[0,:], thermoCalibration[1,:])
    return deg_c + 273.

@contextmanager
def open_thermocouple(gpib_id='6'):
    instr = visa.instrument("GPIB::{0}".format(gpib_id))
    try:
        instr.write('G1')
        instr.write('X')

        class Thermocouple(object):
            def read_temperature(self):
                voltage = float(instr.read())
                return voltageToTemperature(voltage)
        yield Thermocouple()
    finally:
        instr.close()

if __name__ == '__main__':
    with open_thermocouple() as thermo:
        for _ in range(10):
            print thermo.read_temperature(), 'K'
            time.sleep(0.1)