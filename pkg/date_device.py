"""Device for DateTime adapter for Mozilla IoT Gateway."""

import logging
import threading
import time
from gateway_addon import Device
from .util import DT
from .date_property import DateWeekendProperty, DateEvenHourProperty, DateEvenMinuteProperty, \
                           DateSunriseProperty, DateSunsetProperty, \
                           DTMinuteIProperty, DTMinuteNProperty, DTMinuteSProperty, \
                           DTFiveMinutesProperty, DTHourProperty, \
                           DTDarkProperty

class DTDevice(Device):
    """Date device type."""
    def __init__(self, adapter, _id):
        """
        adapter -- the Adapter for this device
        _id -- ID of this device
        """
        Device.__init__(self, adapter, _id)

    def init(self):
        try:
            self.poll_interval = 2
            self.active_poll = True
            self.thread = threading.Thread(target=self.poll)
            self.thread.daemon = True
            self.thread.start()
        except Exception as ex:
            logging.exception('Exception %s', ex)
        logging.info('DateTimeDevice started')

    def add_property(self, property):
        self.properties[property.name] = property

    def poll(self):
        """ Poll device for changes."""
        logging.info('poll START for %s', self.name)
        ixx = 60
        while self.active_poll:
            try:
                time.sleep(self.poll_interval)
                ixx += 1
                if (ixx * self.poll_interval) > 60:  # Every 1 minutes
                    ixx = 0
                    # self.dt.sunset_time()
                for prop in self.properties.values():
                    prop.update()
            except Exception as ex:
                logging.error('THREAD ERR Exception %s', ex)
                logging.exception('Exception %s', ex)
                continue
        logging.info('POLL STOPED for device: %s', self.name)


class DateTimeDevice(DTDevice):
    """Date device type."""
    def __init__(self, adapter, _id, _config):
        """
        adapter -- the Adapter for this device
        _id -- ID of this device
        """
        DTDevice.__init__(self, adapter, _id)
        self._context = 'https://iot.mozilla.org/schemas'
        self._type = ['BinarySensor', 'MultiLevelSensor']
        self.dt = DT(_config.timezone, _config.lat, _config.lng, _config.horizon)

        self.add_property(DateWeekendProperty(self, self.dt))
        self.add_property(DateSunriseProperty(self, self.dt))
        self.add_property(DateSunsetProperty(self, self.dt))
        self.add_property(DateEvenHourProperty(self, self.dt))
        self.add_property(DateEvenMinuteProperty(self, self.dt))
        self.add_property(DTDarkProperty(self, self.dt))
        self.add_property(DTMinuteSProperty(self,self.dt))
        self.add_property(DTFiveMinutesProperty(self, self.dt))
        self.add_property(DTHourProperty(self,self.dt))

        self.name = 'DateTime'
        self.description = 'DateTime desc'
        self.init()

class DateTimeTestDevice(DTDevice):
    """Date device type."""
    def __init__(self, adapter, _id, _config):
        """
        adapter -- the Adapter for this device
        _id -- ID of this device
        """
        DTDevice.__init__(self, adapter, _id)
        self._context = 'https://iot.mozilla.org/schemas'
        self._type = ['BinarySensor', 'MultiLevelSensor']
        self.dt = DT(_config.timezone, _config.lat, _config.lng, _config.horizon)

        self.add_property(DTMinuteIProperty(self,self.dt))
        self.add_property(DTMinuteNProperty(self,self.dt))

        self.name = 'DateTimeTest'
        self.description = 'DateTimeTest desc'
        self.init()
