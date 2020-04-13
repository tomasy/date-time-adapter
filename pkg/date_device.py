"""Device for DateTime adapter for WebThings Gateway."""

import logging
import threading
import time
from gateway_addon import Device, Event
from .util import DT
from .date_property import DateWeekendProperty, DateEvenHourProperty, DateEvenMinuteProperty, \
                           DTMinuteProperty, \
                           DTFiveMinutesProperty, DTHourProperty, \
                           DTDarkProperty, DTWeekdayProperty

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

    def check(self):
        return

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
                self.check()
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
        self._context = 'https://webthings.io/schemas'
        self._type = ['BinarySensor', 'MultiLevelSensor']
        self.dt = DT(_config.timezone, _config.lat, _config.lng, _config.horizon)
        self.sunrise = self.dt.calc_sunrise()
        self.sunset = self.dt.calc_sunset()
        logging.info('sunset: %s sunrise: %s', self.sunset, self.sunrise)

        self.add_property(DateWeekendProperty(self, self.dt))
        self.add_property(DateEvenHourProperty(self, self.dt))
        self.add_property(DateEvenMinuteProperty(self, self.dt))
        self.add_property(DTDarkProperty(self, self.dt))
        self.add_property(DTHourProperty(self,self.dt))
        self.add_property(DTMinuteProperty(self,self.dt))
        self.add_property(DTFiveMinutesProperty(self, self.dt))
        self.add_property(DTWeekdayProperty(self, self.dt))

        self.add_event('sunset', {
            'title': 'Sunset', 'label': 'Sunset',
            'description': 'An event for new sunset',
            'type': 'string',
        })
        self.add_event('sunrise', {
            'title': 'Sunrise', 'label': 'Sunrise',
            'description': 'An event for new sunrise',
            'type': 'string',
        })
        self.name = 'DateTime'
        self.description = 'DateTime desc'
        self.init()
        logging.debug('DateTimeDevice %s', self.as_dict())

    def check(self):
        self.check_sunrise()
        self.check_sunset()

    def check_sunrise(self):
        if self.dt.now() > self.sunrise:
            self.check_send_event(self.sunrise, 'sunrise')
            self.sunrise = self.dt.calc_sunrise()

    def check_sunset(self):
        if self.dt.now() > self.sunset:
            self.check_send_event(self.sunset, 'sunset')
            self.sunset = self.dt.calc_sunset()

    """ Check if the sunset/sunrise time occured and if so send event """
    def check_send_event(self, next_sunset_sunrise, event_name):
        logging.info('now:%s > next:%s', self.dt.now(), next_sunset_sunrise)
        event = Event(self, event_name, event_name + ': ' + str(next_sunset_sunrise))
        self.event_notify(event)
        logging.info('New event ' + event_name)

class DateTimeTestDevice(DTDevice):
    """Date device type."""
    def __init__(self, adapter, _id, _config):
        """
        adapter -- the Adapter for this device
        _id -- ID of this device
        """
        DTDevice.__init__(self, adapter, _id)
        self._context = 'https://webthings.io/schemas'
        self._type = ['BinarySensor', 'MultiLevelSensor']
        self.dt = DT(_config.timezone, _config.lat, _config.lng, _config.horizon)

        self.add_property(DTMinuteProperty(self,self.dt))

        self.name = 'DateTimeTest'
        self.description = 'DateTimeTest desc'
        self.init()
