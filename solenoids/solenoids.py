#!/usr/bin/env python

import yaml, sys, logbook, gpiozero, time, pint

class Actuate:
    def __init__(self):
        logbook.StreamHandler(sys.stdout).push_application()
        self.log = logbook.Logger(self.__class__.__name__)
        logbook.set_datetime_format("local")
        self.log.info('Logbook started')

        try:
            with open('config.yaml', 'r') as stream:
                self.cfg = yaml.load(stream, Loader=yaml.FullLoader)
        except FileNotFoundError:
            self.log.critical('Config file not found')
            sys.exit()

        self.log.level = eval('logbook.'+self.cfg['debug']['loglevel'])
        self.setup()

    def interact(self):
        import code
        code.interact(local=locals())
        sys.exit(0)

    def setup(self):
        self.channel = self.cfg['solenoid']
        for key in self.channel:
            self.channel[key]['switch'] = gpiozero.LED(self.channel[key]['pin'])
        self.time_max = self.to_seconds(self.cfg['default']['max'])

    def to_seconds(self, val):
        ureg = pint.UnitRegistry()
        unit = eval(self.cfg['default']['unit'])
        seconds = unit *val 
        return seconds.to(ureg.second)

    def check(self):
        self.log.debug(self.cfg)
        self.log.debug(self.time_max)
        for key in self.channel:
            state = self.channel[key]['switch'].is_active
            self.log.info(f'{key} is active: {state}')
        self.interact()

if __name__ == '__main__':
    a = Actuate()
    a.check()


