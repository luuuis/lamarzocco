"""Sensor platform for La Marzocco espresso machines."""

import logging

import voluptuous as vol
from homeassistant.helpers import entity_platform
from lmdirect.msgs import (
    CONTINUOUS,
    DRINKS_K1,
    DRINKS_K2,
    DRINKS_K3,
    DRINKS_K4,
    TOTAL_FLUSHING,
)

from .const import (
    ATTR_MAP_COFFEE_TEMP,
    ATTR_MAP_DRINK_STATS_GS3_AV,
    ATTR_MAP_DRINK_STATS_GS3_MP_LM,
    ATTR_MAP_STEAM_TEMP,
    DOMAIN,
    ENTITY_CLASS,
    ENTITY_ICON,
    ENTITY_MAP,
    ENTITY_NAME,
    ENTITY_TAG,
    ENTITY_TYPE,
    ENTITY_UNITS,
    MODEL_GS3_AV,
    MODEL_GS3_MP,
    MODEL_LM,
    MODELS_SUPPORTED,
    SCHEMA,
    SERVICE_SET_TEMP,
    TEMP_COFFEE,
    TEMP_STEAM,
    TYPE_COFFEE_TEMP,
    TYPE_DRINK_STATS,
    TYPE_STEAM_TEMP,
)
from .entity_base import EntityBase
from .services import call_service

_LOGGER = logging.getLogger(__name__)

ENTITIES = {
    "coffee_temp": {
        ENTITY_TAG: [TEMP_COFFEE],
        ENTITY_NAME: "Coffee Temp",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_COFFEE_TEMP,
            MODEL_GS3_MP: ATTR_MAP_COFFEE_TEMP,
            MODEL_LM: ATTR_MAP_COFFEE_TEMP,
        },
        ENTITY_TYPE: TYPE_COFFEE_TEMP,
        ENTITY_ICON: "mdi:water-boiler",
        ENTITY_CLASS: "temperature",
        ENTITY_UNITS: "°C",
    },
    "steam_temp": {
        ENTITY_TAG: [TEMP_STEAM],
        ENTITY_NAME: "Steam Temp",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_STEAM_TEMP,
            MODEL_GS3_MP: ATTR_MAP_STEAM_TEMP,
        },
        ENTITY_TYPE: TYPE_STEAM_TEMP,
        ENTITY_ICON: "mdi:water-boiler",
        ENTITY_CLASS: "temperature",
        ENTITY_UNITS: "°C",
    },
    "drink_stats": {
        ENTITY_TAG: [
            DRINKS_K1,
            DRINKS_K2,
            DRINKS_K3,
            DRINKS_K4,
            CONTINUOUS,
            TOTAL_FLUSHING,
        ],
        ENTITY_NAME: "Total Drinks",
        ENTITY_MAP: {
            MODEL_GS3_AV: ATTR_MAP_DRINK_STATS_GS3_AV,
            MODEL_GS3_MP: ATTR_MAP_DRINK_STATS_GS3_MP_LM,
            MODEL_LM: ATTR_MAP_DRINK_STATS_GS3_MP_LM,
        },
        ENTITY_TYPE: TYPE_DRINK_STATS,
        ENTITY_ICON: "mdi:coffee",
        ENTITY_CLASS: None,
        ENTITY_UNITS: "drinks",
    },
}

ENTITY_SERVICES = {
    SERVICE_SET_TEMP: {
        SCHEMA: {vol.Required("temperature"): vol.Coerce(float)},
        MODELS_SUPPORTED: [MODEL_GS3_AV, MODEL_GS3_MP, MODEL_LM],
    }
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensor entities."""
    lm = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        LaMarzoccoSensor(lm, sensor_type, hass.config.units.is_metric, config_entry)
        for sensor_type in ENTITIES
        if lm.model_name in ENTITIES[sensor_type][ENTITY_MAP]
    )

    platform = entity_platform.current_platform.get()

    [
        platform.async_register_entity_service(
            service, ENTITY_SERVICES[service][SCHEMA], service
        )
        for service in ENTITY_SERVICES
        if lm.model_name in ENTITY_SERVICES[service][MODELS_SUPPORTED]
    ]


class LaMarzoccoSensor(EntityBase):
    """Sensor representing espresso machine temperature data."""

    def __init__(self, lm, sensor_type, is_metric, config_entry):
        """Initialize sensors"""
        self._object_id = sensor_type
        self._lm = lm
        self._entities = ENTITIES
        self._is_metric = is_metric
        self._entity_type = self._entities[self._object_id][ENTITY_TYPE]

        self._lm.register_callback(self.update_callback)

    @property
    def available(self):
        """Return if sensor is available."""
        return all(
            self._lm.current_status.get(x) is not None
            for x in self._entities[self._object_id][ENTITY_TAG]
        )

    @property
    def state(self):
        """State of the sensor."""
        entities = self._entities[self._object_id][ENTITY_TAG]
        return sum([self._lm.current_status.get(x, 0) for x in entities])

    @property
    def unit_of_measurement(self):
        """Unit of measurement."""
        return self._entities[self._object_id][ENTITY_UNITS]

    @property
    def device_class(self):
        """Device class for sensor"""
        return self._entities[self._object_id][ENTITY_CLASS]

    async def set_temp(self, temperature=None):
        """Service call to set the temp of either the coffee or steam boilers."""

        if self._entity_type not in [TYPE_COFFEE_TEMP, TYPE_STEAM_TEMP]:
            _LOGGER.error(
                f"set_temp service used on a non-boiler entity: {self.entity_id}"
            )
            return False

        """Machine expects Celcius, so convert if needed."""
        if not self._is_metric:
            temperature = round((temperature - 32) / 9 * 5, 1)

        func = getattr(self._lm, "set_" + self._object_id)

        _LOGGER.debug(f"Setting {self._object_id} to {temperature}")

        await call_service(func, temp=temperature)
        return True
