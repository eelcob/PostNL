#!/usr/bin/env python3
"""
Sensor component for PostNL
Author: Eelco Bode

Todo: fix file location to variable
"""
import json
import logging

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCES
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

_LOGGER.warning("start Loading PostNL")


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
            print (id)
        
            type = package['shipmentType']
            print (type)

            state = package['status']
            print (state)

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
            print (sender)
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
