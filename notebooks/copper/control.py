
from copper.heater import open_heater, open_power_meter
from copper.thermocouple import open_thermocouple
from numpy import *
from matplotlib.pyplot import *
import time
from collections import namedtuple

Pulse = namedtuple('Pulse', 'delay duration')
Reading = namedtuple('Reading', 'time temperature power')

def readings_to_array(readings):
    dtype = [(field, float) for field in Reading._fields]
    return array(readings, dtype)

def record_pulse(pulse, total_duration):
    with open_heater() as heater, open_power_meter() as power_meter, \
            open_thermocouple() as thermo:
        heater.turn_off()

        start = time.time()
        def get_time(): return time.time() - start

        readings = []
        def do_reading():
            readings.append(Reading(time=get_time(),
                                    temperature=thermo.read_temperature(),
                                    power=power_meter.read_power()))

        print 'Starting'
        while get_time() < pulse.delay: do_reading()

        print 'Turning heater on'
        heater.turn_on()
        while get_time() < pulse.delay+pulse.duration: do_reading()

        print 'Turning heater off'
        heater.turn_off()
        while get_time() < total_duration: do_reading()

        return readings_to_array(readings)


if __name__ == '__main__':
    pulse = Pulse(delay=10, duration=10)
    readings = record_pulse(pulse, 60)

    from copper import analysis
    print 'Heat Cap', analysis.calc_heat_capacity(pulse, readings)
    analysis.plot_readings(readings)