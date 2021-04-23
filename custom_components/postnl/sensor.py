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

#@asyncio.coroutine
#def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
#    async_add_devices(
#        [
#            PostNLSensor(
#                feed=config[CONF_POST_FILE],
#                name=config[CONF_NAME],
#            )
#        ],
#        True,
#    )
#
#class PostNLSensor(SensorEntity):
#    def __init__(
#        self,
#        feed: str,
#        name: str,
#    ):
#        self._feed = feed
#        self._name = name
#        self._state = None
#        self._entries = []
#
#
#
#
#
#   @property
#    def name(self):
#        return self._name
#
#    @property
#    def state(self):
#        return self._state
#
#    @property
#    def icon(self):
#        return ICON
#
#    @property
#    def device_state_attributes(self):
#        return {"entries": self._entries}

#@asyncio.coroutine
#def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
#    async_add_devices(
#        [
#            PostNLSensor(
#                feed=config[CONF_POST_FILE],
#                name=config[CONF_NAME],
#            )
#        ],
#        True,

@asyncio.coroutine
def async_setup_platform(hass, config, add_entities, discovery_info=None):
    async_add_devices(
        [
            _LOGGER.debug("Setup PostNL sensor")

            #entities = []

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
        ],
        True,
    )


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
