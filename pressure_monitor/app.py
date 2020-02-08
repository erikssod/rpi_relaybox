#!/usr/bin/env python3

import time, board, busio, sys
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import pint, yaml, logbook, requests

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

        self.log.level = eval('logbook.'+self.cfg['debug']['loglevel'])

    def interact(self):
        import code
        code.interact(local=locals())
        sys.exit(0)

    def setup(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        
        # Create single-ended input on channel 0
        self.chan0 = AnalogIn(ads, ADS.P0)
    
    def to_V(self,val):
        volts = val * self.ureg.volt
        return volts.to_compact()
    
    def to_Pa(self,V):
        ps = self.cfg['pressure_sensor']
        offset = ps['offset']
        factor = ps['min']/ps['max'] * 10**6
        magnitude = (V - offset) * factor
        pressure = magnitude * self.ureg.pascal
        return pressure.to_compact()
    
    def _dummy(self):
        V = self.chan0.voltage
            
        self.payload = {'timestamp':time.ctime(),
                        'voltage':self.to_V(V),
                        'pressure':self.to_Pa(V),
                        }
        print(self.payload)
    
    def post(self):
        url = self.cfg['slack']['webhookURL']
        r = requests.post(url, json={'text':str(self.payload)})
        self.log.info(f'Slack post: {r.content}')
        self.interact()

if __name__ == '__main__':
    p = PressureMon()
    p.setup()
    p._dummy()
    p.post()

