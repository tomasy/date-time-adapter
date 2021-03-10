"""Properties for DateTime addon for Mozilla IoT Gateway."""

import logging

from gateway_addon import Event, Property

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
        'title', before 'label'
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

    """Will be called when a value is changed for a property. Normally
       the property do not need to know if it has been hanged but if it
       want to take som actions this can be overridden
    """
    def new_value(self, old_value, new_value):
        return

    def update(self):
        """
        Update the current value, if necessary.
        """
        try:
            new_value = self.get_new_value()

            if new_value != self.get_value():
                self.new_value(self.get_value(), new_value)
                #logging.debug('Device: %s Property: %s = %s (%s)', self.device.name, self.name, new_value, self.get_value())
                self.set_cached_value(new_value)
                self.device.notify_property_changed(self)
        except Exception as ex:
            logging.exception('Update Exception %s', ex)

# name is shown in rules
# label is shown in thing

class DTMinuteProperty(DateTimeProperty):
    """Minutes integer property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'minute', {'title': 'Minute', 'label': 'Minute', '@type': 'LevelProperty',
                                                           'type': 'integer', 'unit': 'minute',
                                                           'readOnly': True, 'minimum': 0, 'maximum': 59})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_minute()

class DTHourProperty(DateTimeProperty):
    """Hour integer property type."""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'hour', {'title': 'Hour', 'label': 'Hour', '@type': 'LevelProperty',
                                                         'type': 'integer', 'unit': 'hour',
                                                         'readOnly': True, 'minimum': 0, 'maximum': 23})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_hour()

class DTDayProperty(DateTimeProperty):
    """Day integer property type."""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'day', {'title': 'Day', 'label': 'Day', '@type': 'LevelProperty',
                                                         'type': 'integer', 'unit': 'day',
                                                         'readOnly': True, 'minimum': 1, 'maximum': 31})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_day()

class DTMonthProperty(DateTimeProperty):
    """Month integer property type."""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'month', {'title': 'Month', 'label': 'Month', '@type': 'LevelProperty',
                                                         'type': 'integer', 'unit': 'month',
                                                         'readOnly': True, 'minimum': 1, 'maximum': 12})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_month()

class DTYearProperty(DateTimeProperty):
    """Year integer property type."""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'year', {'title': 'Year', 'label': 'Year', '@type': 'LevelProperty',
                                                         'type': 'integer', 'unit': 'year',
                                                         'readOnly': True, 'minimum': 2000, 'maximum': 3000})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_year()

class DTFiveMinutesProperty(DateTimeProperty):
    """Five minutes property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'minutes5', {'title': '5 minutes', 'label': '5 minutes',
                                                             'type': 'string', 'unit': 'minute',
                                                             'enum': ['0', '5', '10', '15', '20', '25', '30',
                                                                      '35', '40', '45', '50','55'],
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
                                  {'title': 'Even hour', 'label': 'Even hour', 'readOnly': True, 'type': 'boolean', '@type': 'BooleanProperty'})
        self.dt = dt

    def get_new_value(self):
        return self.dt.is_even_hour()

class DateEvenMinuteProperty(DateTimeProperty):
    """Even minute boolean property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'even',
                              {'title': 'Even minute', 'label': 'Even minute', 'readOnly': True, 'type': 'boolean', '@type': 'BooleanProperty'})
        self.dt = dt

    def get_new_value(self):
        return self.dt.is_even_minute()

class DateWeekendProperty(DateTimeProperty):
    """Weekend boolean property"""
    def __init__(self, device, dt):
        self.dt = dt
        DateTimeProperty.__init__(self, device, 'weekend',
                              {'title': 'Weekend', 'label': 'Weekend', 'type': 'boolean', '@type': 'BooleanProperty'})

    def get_new_value(self):
        return self.dt.is_sat_sun()

class DTDarkProperty(DateTimeProperty):
    """Dark boolean property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'dark',
                              {'title': 'Dark', 'label': 'Dark', 'type': 'boolean', '@type': 'BooleanProperty'})
        self.dt = dt

    def get_new_value(self):
        return self.dt.sunset() > self.dt.sunrise()

class DTWeekdayProperty(DateTimeProperty):
    """Weekday property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'weekday', {'title': 'Weekday', 'label': 'Weekday',
                                                             'type': 'string',
                                                             'enum': ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                                                      'Friday', 'Saturday', 'Sunday'],
                                                             'readOnly': False})
        self.dt = dt

    def get_new_value(self):
        weekday = self.dt.get_weekday()
        day = self.description['enum'][weekday]
        return day

class DTAzimuthProperty(DateTimeProperty):
    """Azimunth integer property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'azimuth', {'title': 'Azimuth', 'label': 'Azimuth', '@type': 'LevelProperty',
                                                           'type': 'integer', 'unit': 'degree',
                                                           'readOnly': True, 'minimum': -180, 'maximum': 180})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_azimuth()

class DTElevationProperty(DateTimeProperty):
    """Elevation integer property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'elevation', {'title': 'Elevation', 'label': 'Elevation', '@type': 'LevelProperty',
                                                           'type': 'integer', 'unit': 'degree',
                                                           'readOnly': True, 'minimum': 0, 'maximum': 90})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_elevation()

class DTNextEventProperty(DateTimeProperty):
    """Next event integer property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'next_event', {'title': 'Next event', 'label': 'Next event', '@type': 'LevelProperty',
                                                           'type': 'integer', 'unit': 'minute',
                                                           'readOnly': True, 'minimum': 0, 'maximum': 1440})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_nexttime()

class DTLastEventProperty(DateTimeProperty):
    """Last event integer property"""
    def __init__(self, device, dt):
        DateTimeProperty.__init__(self, device, 'last_event', {'title': 'Last event', 'label': 'Last event', '@type': 'LevelProperty',
                                                           'type': 'integer', 'unit': 'minute',
                                                           'readOnly': True, 'minimum': 0, 'maximum': 1440})
        self.dt = dt

    def get_new_value(self):
        return self.dt.get_lasttime()
