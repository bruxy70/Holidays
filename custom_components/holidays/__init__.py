"""Component to integrate with holidays."""

import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous as vol
from dateutil.relativedelta import relativedelta
from homeassistant import config_entries
from homeassistant.const import CONF_ENTITY_ID, CONF_NAME
from homeassistant.helpers import discovery

from .const import (
    CONF_DATE,
    CONF_SENSORS,
    DOMAIN,
    SENSOR_PLATFORM,
    configuration,
)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)

config_definition = configuration()

SENSOR_SCHEMA = vol.Schema(config_definition.compile_schema())

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {vol.Optional(CONF_SENSORS): vol.All(cv.ensure_list, [SENSOR_SCHEMA])}
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up this component using YAML."""

    if config.get(DOMAIN) is None:
        # We get here if the integration is set up using config flow
        return True

    return False

async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""
    if config_entry.source == config_entries.SOURCE_IMPORT:
        # We get here if the integration is set up using YAML
        return False
    _LOGGER.debug(
        "Setting %s from ConfigFlow",
        config_entry.title,
    )
    # # Backward compatibility - clean-up (can be removed later?)
    config_entry.options = {}
    config_entry.add_update_listener(update_listener)
    # Add sensor
    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(config_entry, SENSOR_PLATFORM)
    )
    return True


async def async_remove_entry(hass, config_entry):
    """Handle removal of an entry."""
    try:
        await hass.config_entries.async_forward_entry_unload(
            config_entry, SENSOR_PLATFORM
        )
        _LOGGER.info(
            "Successfully removed sensor from the holidays integration"
        )
    except ValueError:
        pass


async def update_listener(hass, entry):
    """Update listener."""
    # The OptionsFlow saves data to options.
    # Move them back to data and clean options (dirty, but not sure how else to do that)
    if len(entry.options) > 0:
        entry.data = entry.options
        entry.options = {}
    await hass.config_entries.async_forward_entry_unload(entry, SENSOR_PLATFORM)
    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(entry, SENSOR_PLATFORM)
    )
