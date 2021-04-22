#!/usr/bin/env python3
"""
Sensor component for PostNL
Author: Eelco Bode

import json

#data = {}
#number = 0
#with open ('POSTNL-Inbox.json') as json_file:
#    data = json.load(json_file)
#    for package in data ['receiver']:
#        print(number)
#        print('Type: '+ package['shipmentType'])
#        print('State: '+ package['delivery']['status'])
#        if package['sender']:
#            if package['sender']['firstName']:
#                if package['sender']['lastName']:
#                    sender = package['sender']['firstName'] + " " + package['sender']['lastName']
#                else:
#                    sender = package['sender']['firstName']
#            elif package['sender']['lastName']:
#                sender = package['sender']['lastName']
#            elif package['sender']['companyName']:
#                    sender = package['sender']['companyName']
#            else:
#                sender = "uknown"
#        else:
#            sender = "Unknown"
#        print('Sender: '+ sender)
#        print('\n')
#        number = number + 1


from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug("Setup PostNL sensor")

    entities = []

    data = {}
    packagenumber = 0
    with open ('POSTNL-Inbox.json') as json_file:
    data = json.load(json_file)
    for package in data ['receiver']:
        sensor_type = resource.lower()

        id = packagenumber
        
        #print('Type: '+ package['shipmentType'])
        type = package['shipmentType']

        print('State: '+ package['delivery']['status'])
        state = package['status']

        if package['sender']:
            if package['sender']['firstName']:
                if package['sender']['lastName']:
                    sender = package['sender']['firstName'] + " " + package['sender']['lastName']
                else:
                    sender = package['sender']['firstName']
            elif package['sender']['lastName']:
                sender = package['sender']['lastName']
            elif package['sender']['companyName']:
                    sender = package['sender']['companyName']
            else:
                sender = "uknown"
        else:
            sender = "Unknown"
        #print('Sender: '+ sender)
        package = PostNLSensor(id, sender, type, state)

        packagenumber = packagenumber + 1
        entities.append(package)

    add_entities(entities)


class PostNLSenor(Entity):
    def __init__(self, data, sensor_type, date_format, timespan_in_days, locale, id_name):
        self.data = data
        self.type = sensor_type
        self.date_format = date_format
        self.timespan_in_days = timespan_in_days
        self.locale = locale
        self._name = SENSOR_PREFIX + (id_name + " " if len(id_name) > 0  else "") + SENSOR_TYPES[sensor_type][0]
        self._icon = SENSOR_TYPES[sensor_type][1]
        self._hidden = False
        self._state = None
        self._last_update = None
        self._days_until_collection_date = None
        self._is_collection_date_today = False
        self._year_month_day_date = None

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return {ATTR_YEAR_MONTH_DAY_DATE: self._year_month_day_date, ATTR_LAST_UPDATE: self._last_update, ATTR_HIDDEN: self._hidden, ATTR_DAYS_UNTIL_COLLECTION_DATE: self._days_until_collection_date, ATTR_IS_COLLECTION_DATE_TODAY: self._is_collection_date_today}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self.data.update()
        waste_data = self.data.data

        try:
            if waste_data:
                if self.type in waste_data:
                    collection_date = datetime.strptime(
                        waste_data[self.type], "%Y-%m-%d"
                    ).date()

                    # Date in date format "%Y-%m-%d"
                    self._year_month_day_date = str(collection_date)

                    if collection_date:
                        # Set the values of the sensor
                        self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")

                        # Is the collection date today?
                        self._is_collection_date_today = date.today() == collection_date

                        # Days until collection date
                        delta = collection_date - date.today()
                        self._days_until_collection_date = delta.days

                        # Only show the value if the date is lesser than or equal to (today + timespan_in_days)
                        if collection_date <= date.today() + relativedelta(days=int(self.timespan_in_days)):
                            #if the date does not contain a named day or month, return the date as normal
                            if (self.date_format.find('a') == -1 and self.date_format.find('A') == -1
                            and self.date_format.find('b') == -1 and self.date_format.find('B') == -1):
                                self._state = collection_date.strftime(self.date_format)
                            #else convert the named values to the locale names
                            else:
                                edited_date_format = self.date_format.replace('%a', 'EEE')
                                edited_date_format = edited_date_format.replace('%A', 'EEEE')
                                edited_date_format = edited_date_format.replace('%b', 'MMM')
                                edited_date_format = edited_date_format.replace('%B', 'MMMM')

                                #half babel, half date string... something like EEEE 04-MMMM-2020
                                half_babel_half_date = collection_date.strftime(edited_date_format)

                                #replace the digits with qquoted digits 01 --> '01'
                                half_babel_half_date = re.sub(r"(\d+)", r"'\1'", half_babel_half_date)
                                #transform the EEE, EEEE etc... to a real locale date, with babel
                                locale_date = format_date(collection_date, half_babel_half_date, locale=self.locale)

                                self._state = locale_date
                        else:
                            self._hidden = True
                    else:
                        raise ValueError()
                else:
                    raise ValueError()
            else:
                raise ValueError()
        except ValueError:
            self._state = None
            self._hidden = True
            self._days_until_collection_date = None
            self._year_month_day_date = None
            self._is_collection_date_today = False
            self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
