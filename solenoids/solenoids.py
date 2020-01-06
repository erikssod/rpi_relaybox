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


    def setup(self):
        self.pair1 = gpiozero.LED(self.cfg['relay_ctl_pin']['beds1n2'])
        self.pair2 = gpiozero.LED(self.cfg['relay_ctl_pin']['beds3n4'])
        self.spikes = gpiozero.LED(self.cfg['relay_ctl_pin']['spikes'])

    def time_open(self):
        ureg = pint.UnitRegistry()
        t = self.cfg['default']['time']
        u = eval(self.cfg['default']['unit'])
        tmp = t * u
        self.TimeOpen = tmp.to(ureg.second)

    def check(self):
        self.log.debug(self.cfg)
        self.log.debug(self.TimeOpen)

    def test(self):
        self.pair1.on()
        self.pair2.on()
        self.spikes.on()
        self.log.info(self.pair1.is_active)
        self.log.info(self.pair2.is_active)
        self.log.info(self.spikes.is_active)
        time.sleep(15)
        self.pair1.off()
        self.pair2.off()
        self.spikes.off()
        self.log.info(self.pair1.is_active)
        self.log.info(self.pair2.is_active)
        self.log.info(self.spikes.is_active)

    def all_off(self):
        self.pair1.off()
        self.pair2.off()
        self.spikes.off()
        self.log.info(self.pair1.is_active)
        self.log.info(self.pair2.is_active)
        self.log.info(self.spikes.is_active)


if __name__ == '__main__':
    a = Actuate()
    a.time_open()
    a.check()
#   a.test()
    a.all_off()


