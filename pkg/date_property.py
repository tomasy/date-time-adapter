"""Properties for DateTime addon for Mozilla IoT Gateway."""

import logging

from gateway_addon import Property

class DateTimeProperty(Property):
    """Date property type."""

    def __init__(self, device, name, description):
        """
        Initialize the object.

        device -- the Device this property belongs to
        name -- name of the property
        description -- description of the property, as a dictionary

        description e.g. {'type': 'boolean'} or more
        'visible'
        'lable'
        'type'
        '@type'
        'unit'
        'description'
        'minimum'
        'maximum'
        'enum'
        'readOnly'
        """
        Property.__init__(self, device, name, description)

# Abstract
    def get_new_value(self):
        logging.error('Missing function property: %s', self)
        return

    def update(self):
        """
        Update the current value, if necessary.
        """
        try:
            new_value = self.get_new_value()

            if new_value != self.get_value():
                logging.info('Device: %s Property: %s = %s (%s)', self.device.name, self.name, new_value, self.get_value())
                self.set_cached_value(new_value)
                self.device.notify_property_changed(self)
        except Exception as ex:
            logging.exception('Update Exception %s', ex)

# name is shown in rules
# label is shown in thing

class DTMinuteIProperty(DateTimeProperty):
    """Minutes integer property"""

    def __init__(self, device, dt):
        # should be 'type': integer'
        DateTimeProperty.__init__(self, device, 'minutesI', {'label': 'Minute I', '@type': 'LevelProperty',
                                                        'type': 'integer', 'unit': 'minute',
                                                        'readOnly': True, 'minimum': 0, 'maximum': 59})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_minute()

class DTMinuteNProperty(DateTimeProperty):
    """Minutes number property type."""

    def __init__(self, device, dt):
        # should be 'type': integer'
        DateTimeProperty.__init__(self, device, 'minutesN', {'label': 'Minute N', '@type': 'LevelProperty',
                                                        'type': 'number', 'unit': 'minute',
                                                        'readOnly': True, 'minimum': 0, 'maximum': 59})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_minute()

class DTMinuteSProperty(DateTimeProperty):
    """Minute string property"""

    def __init__(self, device, dt):
        # should be 'type': integer'
        DateTimeProperty.__init__(self, device, 'minutesS', {'label': 'Minute', '@type': 'LevelProperty',
                                                        'type': 'string', 'unit': 'minute',
                                                        'readOnly': True, 'minimum': 0, 'maximum': 59})
        self.dt = dt

    def get_new_value(self):
        return str(self.dt.get_minute())

class DTHourProperty(DateTimeProperty):
    """Hour property"""

    def __init__(self, device, dt):
        # should be 'type': integer'
        DateTimeProperty.__init__(self, device, 'hour', {'label': 'Hour', '@type': 'LevelProperty',
                                                        'type': 'string', 'unit': 'hour',
                                                        'readOnly': True, 'minimum': 0, 'maximum': 23})
        self.dt = dt

    def get_new_value(self):
        return str(self.dt.get_hour())

class DTFiveMinutesProperty(DateTimeProperty):
    """Five minutes property"""

    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'minutes5', {'label': '5 minutes', '@type': 'LevelProperty',
                                                         'type': 'string', 'unit': 'minute',
                                                         'enum': ['0','5','10','15','20','25','30','35','40','45','50','55'],
                                                         'minimum': 0, 'maximum': 59,
                                                         'readOnly': True})
        self.dt = dt

    def get_new_value(self):
        minute = self.dt.get_minute()
        min5 = int(int(minute / 5) * 5)
        return str(min5)

class DateEvenHourProperty(DateTimeProperty):
    """Even hour boolean property"""

    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'even_hour',
                              {'label': 'Even hour', 'readOnly': True, 'type': 'boolean', '@type': 'BooleanProperty'})
        self.dt = dt

    def get_new_value(self):
        return self.dt.is_even_hour()

class DateEvenMinuteProperty(DateTimeProperty):
    """Even minute boolean property"""

    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'even',
                              {'label': 'Even minute', 'readOnly': True, 'type': 'boolean', '@type': 'BooleanProperty'})
        self.dt = dt

    def get_new_value(self):
        return self.dt.is_even_minute()

class DateWeekendProperty(DateTimeProperty):
    """Weekend boolean property"""

    def __init__(self, device, dt):
        self.dt = dt
        DateTimeProperty.__init__(self, device, 'weekend',
                              {'label': 'Weekend', 'type': 'boolean', '@type': 'BooleanProperty'})

    def get_new_value(self):
        return self.dt.is_sat_sun()

class DateSunriseProperty(DateTimeProperty):
    """Sunrise bolean property"""

    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'sunrise',
                              {'label': 'Sunrise', 'readOnly': True, 'type': 'boolean', '@type': 'BooleanProperty'})
        self.dt = dt

    def get_new_value(self):
        return self.dt.check_time_now(self.dt.sunrise(), 'sunrise')

class DateSunsetProperty(DateTimeProperty):
    """Sunset boolean property"""

    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'sunset',
                              {'label': 'Sunset', 'readOnly': True, 'type': 'boolean', '@type': 'BooleanProperty'})
        self.dt = dt

    def get_new_value(self):
        return self.dt.check_time_now(self.dt.sunset(), 'sunset')

class DTDarkProperty(DateTimeProperty):
    """Dark boolean property"""

    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'dark',
                              {'label': 'Dark', 'type': 'boolean', '@type': 'BooleanProperty'})
        self.dt = dt

    def get_new_value(self):
        return self.dt.sunset() > self.dt.sunrise()
