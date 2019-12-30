#!/usr/bin/env python

import yaml, sys, logbook, gpiozero

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

    def check(self):
        self.log.debug(self.cfg)

    def setup(self):
        self.pair1 = gpiozero.LED(self.cfg['relay_ctl_pin']['beds1n2'])
        self.pair2 = gpiozero.LED(self.cfg['relay_ctl_pin']['beds3n4'])
        self.spikes = gpiozero.LED(self.cfg['relay_ctl_pin']['spikes'])

if __name__ == '__main__':
    a = Actuate()
    a.check()


