"""Define constants used in garbage_collection."""

from datetime import datetime
from typing import Any, List

import voluptuous as vol

# Constants for holidays.
# Base component constants
DOMAIN = "holidays"
CALENDAR_PLATFORM = "calendar"
ATTRIBUTION = "Data from this is provided by holidays."

VERSION = 2

ATTR_NEXT_DATE = "next_date"
ATTR_NEXT_HOLIDAY = "next_holiday"
ATTR_LAST_UPDATED = "last_updated"
ATTR_HOLIDAYS = "holidays"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"
DEVICE_CLASS = "holidays__schedule"

# Configuration
CONF_CALENDAR = "calendar"
CONF_ICON_NORMAL = "icon_normal"
CONF_ICON_TODAY = "icon_today"
CONF_ICON_TOMORROW = "icon_tomorrow"
CONF_COUNTRY = "country"
CONF_HOLIDAY_POP_NAMED = "holiday_pop_named"
CONF_PROV = "prov"  # obsolete
CONF_STATE = "state"  # obsolete
CONF_SUBDIV = "subdiv"  # Subdivision - replaces state and prov
CONF_OBSERVED = "observed"
CONF_CALENDARS = "calendars"

# Defaults
DEFAULT_NAME = DOMAIN

# Icons
DEFAULT_ICON_NORMAL = "mdi:calendar-blank"
DEFAULT_ICON_TODAY = "mdi:calendar-arrow-right"
DEFAULT_ICON_TOMORROW = "mdi:calendar-check"
ICON = DEFAULT_ICON_NORMAL


def date_text(value: Any) -> str:
    """Have to store date as text - datetime is not JSON serialisable."""
    if value is None or value == "":
        return ""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().strftime("%Y-%m-%d")
    except ValueError as error:
        raise vol.Invalid(f"Invalid date: {value}") from error


def time_text(value: Any) -> str:
    """Have to store time as text - datetime is not JSON serialisable."""
    if value is None or value == "":
        return ""
    try:
        return datetime.strptime(value, "%H:%M").time().strftime("%H:%M")
    except ValueError as error:
        raise vol.Invalid(f"Invalid date: {value}") from error


def month_day_text(value: Any) -> str:
    """Validate format month/day."""
    if value is None or value == "":
        return ""
    try:
        return datetime.strptime(value, "%m/%d").date().strftime("%m/%d")
    except ValueError as error:
        raise vol.Invalid(f"Invalid date: {value}") from error


def string_to_list(string) -> List:
    """Convert comma separated text to list."""
    if string is None or string == "":
        return []
    return list(map(lambda x: x.strip("'\" "), string.split(",")))
