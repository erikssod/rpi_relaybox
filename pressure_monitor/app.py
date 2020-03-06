#!/usr/bin/env python3

import time, board, busio, sys
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import pint, yaml, logbook, requests
import numpy as np

class PressureMon:
    def __init__(self):
        logbook.StreamHandler(sys.stdout).push_application()
        self.log = logbook.Logger(self.__class__.__name__)
        logbook.set_datetime_format("local")
        self.log.info('Logbook started')

        self.ureg = pint.UnitRegistry()

        try:
            with open('config.yaml', 'r') as stream:
                self.cfg = yaml.load(stream, Loader=yaml.FullLoader)
        except FileNotFoundError:
            self.log.critical('Config file not found')
            sys.exit()

        try:
            f = self.cfg['slack']['webhookfile']
            with open(f, 'r') as stream:
                self.slackURL = yaml.load(stream, Loader=yaml.FullLoader)
        except FileNotFoundError:
            self.log.critical('Config file not found')
            sys.exit()

        self.log.level = eval('logbook.'+self.cfg['debug']['loglevel'])

    def interact(self):
        import code
        code.interact(local=locals())
        sys.exit(0)

    def setup(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self._chan0 = AnalogIn(ads, ADS.P0)
        window = self.cfg['monitor']['window']
        self.data = list(np.arange(0,window))
        self.freq = self.cfg['monitor']['frequency']
        self.lo = self.cfg['monitor']['lo']
        self.hi = self.cfg['monitor']['hi']

    def to_V(self,val):
        volts = val * self.ureg.volt
        return volts.to_compact()
    
    def to_Pa(self,V):
        ps = self.cfg['pressure_sensor']
        offset = ps['offset']
        factor = ps['min']/ps['max']
        magnitude = (V - offset) * factor
        pressure = magnitude * self.ureg.pascal
        return pressure

    def to_seconds(self,val):
        ureg = self.ureg
        unit = ureg.parse_expression(self.cfg['monitor']['unit'])
        seconds = unit * val 
        return seconds.to(ureg.second)
    
    def to_interval(self,val):
        ureg = self.ureg
        unit = ureg.parse_expression(self.cfg['monitor']['unit'])
        return  unit * val 
    
    def get_reading(self):
        self.data.pop(0)
        self.datapt = self.to_V(self._chan0.voltage)
        self.data.extend([self.datapt.magnitude])
    
    def monitor(self):
        while True:
            self.get_reading()
            Pa = self.to_Pa(self.datapt.magnitude)
            self.log.info('{0.magnitude:.2f} {0.units:~}'.format(Pa))
            self.norm = self.datapt.magnitude / np.mean(self.data)
            self.log.debug(f'Norm: {self.norm:.2f}')
            if self.norm < self.lo: 
                self.report('dump')
                self.post()
            if self.norm > self.hi:
                self.report('spike')
                self.post()
            time.sleep(self.to_seconds(self.freq).magnitude)

    def report(self, trigger):
        pretty = self.data * self.ureg.pascal
        interv = self.to_interval(self.freq)
        self.payload = {'text':f'Pressure {trigger}!' +\
                '\nMost recent readings: {:.2f~}'.format(pretty) +\
                f'\nTaken every {interv}'}
        self.log.debug(self.payload)
    
    def post(self):
        r = requests.post(self.slackURL,json=self.payload)
        self.log.debug(f'Slack post: {r.content}')

if __name__ == '__main__':
    p = PressureMon()
    p.setup()
    p.monitor()
