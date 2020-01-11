#!/usr/bin/env python3

import time, board, busio, csv
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan0 = AnalogIn(ads, ADS.P0)

fieldnames = ['timestamp','val']

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open('data.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        payload = {'timestamp':time.ctime(),
                   'val':chan0.value}

        csv_writer.writerow(payload)
        time.sleep(1)
