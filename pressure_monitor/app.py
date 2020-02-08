#!/usr/bin/env python3

import time, board, busio, csv
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import pint

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)

fieldnames = ['timestamp', 'voltage', 'pressure']

ureg = pint.UnitRegistry()

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

def to_V(val):
    volts = val * ureg.volt
    return volts.to_compact()

def to_Pa(V):
    offset = 0.504140385
    factor = 1.6/4.5 * 10**6
    magnitude = (V - offset) * factor
    pressure = magnitude * ureg.pascal
    return pressure.to_compact()

while True:
    with open('data.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        V = chan0.voltage
        
        payload = {'timestamp':time.ctime(),
                   'voltage':to_V(V),
                   'pressure':to_Pa(V),
                   }

        csv_writer.writerow(payload)
        print(payload)
        time.sleep(1)


