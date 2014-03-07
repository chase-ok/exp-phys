

from numpy import *
from matplotlib.pyplot import *

SAMPLE_MOLES = 0.2223

def plot_readings(readings):
    _, temp_axis = subplots()
    temp_axis.plot(readings['time'], readings['temperature'], 'k')
    temp_axis.set_xlabel('Time [s]')
    temp_axis.set_ylabel('Temperature [K]', color='k')
    for tick in temp_axis.get_yticklabels(): tick.set_color('k')
    
    power_axis = temp_axis.twinx()
    power_axis.plot(readings['time'], readings['power'], 'r')
    power_axis.set_ylabel('Power [W]', color='r')
    for tick in power_axis.get_yticklabels(): tick.set_color('r')
    show()

def calc_energy_delivered(readings):
    return trapz(readings['power'], readings['time'])

def calc_start_temperature(pulse, readings):
    base_line = readings['temperature'][readings['time'] < pulse.delay*0.9]
    return base_line.mean()

def calc_peak_temperature(pulse, readings):
    after_pulse = readings['temperature'][readings['time'] > pulse.delay]
    sorted_temps = sort(after_pulse)
    return sorted_temps[-3:].mean()

def calc_heat_capacity(pulse, readings):
    energy = calc_energy_delivered(readings)
    print 'Energy', energy, 'J'

    start_temp = calc_start_temperature(pulse, readings)
    print 'Starting Temperature', start_temp, 'K'

    peak_temp = calc_peak_temperature(pulse, readings)
    print 'Peak Temperature', peak_temp, 'K'

    return energy/(peak_temp-start_temp)/SAMPLE_MOLES