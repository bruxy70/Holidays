"""Sensor platform for holidays."""
import asyncio
import logging
from datetime import date, datetime, time, timedelta
from typing import Any, List, Optional, Union

import holidays
import homeassistant.util.dt as dt_util
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from homeassistant.const import ATTR_HIDDEN, CONF_ENTITIES, CONF_NAME
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.restore_state import RestoreEntity

from .calendar import EntitiesCalendarData
from .const import (
    ATTR_DAYS,
    ATTR_HOLIDAYS,
    ATTR_LAST_UPDATED,
    ATTR_NEXT_DATE,
    CALENDAR_NAME,
    CALENDAR_PLATFORM,
    CONF_HOLIDAY_POP_NAMED,
    CONF_ICON_NORMAL,
    CONF_ICON_TODAY,
    CONF_ICON_TOMORROW,
    CONF_COUNTRY,
    CONF_OBSERVED,
    CONF_PROV,
    CONF_STATE,
    DEVICE_CLASS,
    DOMAIN,
    SENSOR_PLATFORM,
    STATE_TODAY,
    STATE_TOMORROW,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=10)
THROTTLE_INTERVAL = timedelta(seconds=60)


async def async_setup_platform(hass, _, async_add_entities, discovery_info=None):
    """Create garbage collection entities defined in YAML and add them to HA."""
    async_add_entities([Holidays(hass, discovery_info)], True)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Create garbage collection entities defined in config_flow and add them to HA."""
    async_add_devices([Holidays(hass, config_entry.data, config_entry.title)], True)


class Holidays(RestoreEntity):
    """Holidays Sensor class."""

    def __init__(self, hass, config, title=None):
        """Read configuration and initialise class variables."""
        self.config = config
        self._name = title if title is not None else config.get(CONF_NAME)
        self._hidden = config.get(ATTR_HIDDEN, False)
        self._country = config.get(CONF_COUNTRY)
        self._holiday_pop_named = config.get(CONF_HOLIDAY_POP_NAMED)
        self._holiday_prov = config.get(CONF_PROV)
        self._holiday_state = config.get(CONF_STATE)
        self._holiday_observed = config.get(CONF_OBSERVED, True)
        self._holidays = []
        self._holidays_log = ""
        self._next_date = None
        self._last_updated = None
        self._days = None
        self._entities = config.get(CONF_ENTITIES)
        self._state = 2
        self._icon_normal = config.get(CONF_ICON_NORMAL)
        self._icon_today = config.get(CONF_ICON_TODAY)
        self._icon_tomorrow = config.get(CONF_ICON_TOMORROW)
        self._icon = self._icon_normal

    async def _async_load_holidays(self) -> None:
        """Load the holidays from from a date."""
        self._holidays_log = ""
        log = ""
        self._holidays.clear()
        if self._country_holidays is not None and self._country_holidays != "":
            this_year = dt_util.now().date().year
            years = [this_year - 1, this_year, this_year + 1]
            _LOGGER.debug(
                "(%s) Country Holidays with parameters: "
                "country: %s, prov: %s, state: %s, observed: %s",
                self._name,
                self._country_holidays,
                self._holiday_prov,
                self._holiday_state,
                self._holiday_observed,
            )
            kwargs = {"years": years}
            if self._holiday_state is not None and self._holiday_state != "":
                kwargs["state"] = self._holiday_state
            if self._holiday_prov is not None and self._holiday_prov != "":
                kwargs["prov"] = self._holiday_prov
            if (
                self._holiday_observed is not None
                and isinstance(self._holiday_observed, bool)
                and not self._holiday_observed
            ):
                kwargs["observed"] = self._holiday_observed  # type: ignore
            hol = holidays.CountryHoliday(self._country_holidays, **kwargs)
            if self._holiday_pop_named is not None:
                for pop in self._holiday_pop_named:
                    try:
                        hol.pop_named(pop)
                    except Exception as err:
                        _LOGGER.error("(%s) Holiday not removed (%s)", self._name, err)
            try:
                for holiday_date, holiday_name in hol.items():
                    self._holidays.append(holiday_date)
                    log += f"\n  {holiday_date}: {holiday_name}"
                    self._holidays_log += f"\n  {holiday_date}: {holiday_name}"
            except KeyError:
                _LOGGER.error(
                    "(%s) Invalid country code (%s)",
                    self._name,
                    self._country_holidays,
                )
            _LOGGER.debug("(%s) Found these holidays: %s", self._name, log)

    async def async_added_to_hass(self):
        """When sensor is added to hassio, add it to calendar."""
        await super().async_added_to_hass()
        if DOMAIN not in self.hass.data:
            self.hass.data[DOMAIN] = {}
        if SENSOR_PLATFORM not in self.hass.data[DOMAIN]:
            self.hass.data[DOMAIN][SENSOR_PLATFORM] = {}
        self.hass.data[DOMAIN][SENSOR_PLATFORM][self.entity_id] = self

        state = await self.async_get_last_state()
        if not self.hidden:
            if CALENDAR_PLATFORM not in self.hass.data[DOMAIN]:
                self.hass.data[DOMAIN][CALENDAR_PLATFORM] = EntitiesCalendarData(
                    self.hass
                )
                _LOGGER.debug("Creating holidays calendar")
                self.hass.async_create_task(
                    async_load_platform(
                        self.hass,
                        CALENDAR_PLATFORM,
                        DOMAIN,
                        {"name": CALENDAR_NAME},
                        {"name": CALENDAR_NAME},
                    )
                )
            self.hass.data[DOMAIN][CALENDAR_PLATFORM].add_entity(self.entity_id)

    async def async_will_remove_from_hass(self):
        """When sensor is added to hassio, remove it."""
        await super().async_will_remove_from_hass()
        del self.hass.data[DOMAIN][SENSOR_PLATFORM][self.entity_id]
        self.hass.data[DOMAIN][CALENDAR_PLATFORM].remove_entity(self.entity_id)

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return self.config.get("unique_id", None)

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self.config.get("unique_id", None))},
            "name": self.config.get("name"),
            "manufacturer": "bruxy70",
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def hidden(self):
        """Return the hidden attribute."""
        return self._hidden

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the entity icon."""
        return self._icon

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        res = {}
        if self._next_date is None:
            res[ATTR_NEXT_DATE] = None
        else:
            res[ATTR_NEXT_DATE] = datetime(
                self._next_date.year, self._next_date.month, self._next_date.day
            ).astimezone()
        res[ATTR_DAYS] = self._days
        res[ATTR_LAST_UPDATED] = self._last_updated
        res[ATTR_HOLIDAYS] = self._holidays_log
        return res

    @property
    def device_class(self):
        """Return the class of the sensor."""
        return DEVICE_CLASS

    def __repr__(self):
        """Return main sensor parameters."""
        return (
            f"Holidays[ name: {self._name}, "
            f"entity_id: {self.entity_id}, "
            f"state: {self.state}\n"
            f"config: {self.config}]"
        )

    async def _async_ready_for_update(self) -> bool:
        """Check if the entity is ready for the update.

        Skip the update if the sensor was updated today
        """
        now = dt_util.now()
        today = now.date()
        try:
            ready_for_update = bool(self._last_updated.date() != today)
        except AttributeError:
            ready_for_update = True
        return ready_for_update

    async def async_next_date(self, first_date: date) -> Optional[date]:
        """Get next date from self._holidays."""
        for d in self._holidays:
            if d < first_date:
                continue
            return d
        return None

    async def async_update(self) -> None:
        """Get the latest data and updates the states."""
        if not await self._async_ready_for_update() or not self.hass.is_running:
            return
        _LOGGER.debug("(%s) Calling update", self._name)
        await self._async_load_holidays()
        await self.async_update_state()

    async def async_update_state(self) -> None:
        """Pick the first event from holiday dates, update attributes."""
        _LOGGER.debug("(%s) Looking for next collection", self._name)
        now = dt_util.now()
        today = now.date()
        self._next_date = await self.async_next_date(today)
        self._last_updated = now
        if self._next_date is not None:
            _LOGGER.debug(
                "(%s) next_date (%s), today (%s)", self._name, self._next_date, today
            )
            self._days = (self._next_date - today).days
            next_date_txt = self._next_date.strftime(self._date_format)
            _LOGGER.debug(
                "(%s) Found next collection date: %s, that is in %d days",
                self._name,
                next_date_txt,
                self._days,
            )
            if self._days > 1:
                self._state = 3
                self._icon = self._icon_normal
            else:
                if self._days == 0:
                    self._state = STATE_TODAY
                    self._icon = self._icon_today
                elif self._days == 1:
                    self._state = STATE_TOMORROW
                    self._icon = self._icon_tomorrow
        else:
            self._days = None
