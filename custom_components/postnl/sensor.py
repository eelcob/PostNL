#!/usr/bin/env python3
"""
Sensor component for PostNL
Author: Eelco Bode

Todo: fix file location to variable
"""
import json
import logging
import asyncio
import voluptuous as vol

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME

_LOGGER = logging.getLogger(__name__)

_LOGGER.warning("start Loading PostNL")

CONF_POST_FILE = "postfile"

ICON = "mdi:email"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_POST_FILE): cv.string,
    }
)

@asyncio.coroutine
def async_setup_platform(hass, config, add_entities, discovery_info=None):
            _LOGGER.debug("Setup PostNL sensor")

            #entities = []

            data = {}
            packagenumber = 0
            packagefile = config.get(CONF_POST_FILE).strip()
            with open (packagefile) as json_file:
                data = json.load(json_file)
                for package in data ['receiver']:

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
    def __init__(self, data, id, sender, type, state):
        self.data = data
        self.id = id
        self.sender = sender
        self.type = type
        self.state = state
        self._name = SENSOR_PREFIX + (id_name + " " if len(id_name) > 0  else "") + SENSOR_TYPES[sensor_type][0]
        self._icon = SENSOR_TYPES[sensor_type][1]
        self._hidden = False
        self._state = None
        self._last_update = None

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state
