"""Test calendar for simple integration."""
from datetime import date

import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.holidays import const

ERROR_STATE = "Next holiday should be in {} days, not {}."
ERROR_NAME = "Next holiday should be {}, not {}."
ERROR_DATE = "Next holiday should be on {}, not {}."
ERROR_LENGTH = "Holidays should have {} items, not {}."


@pytest.mark.asyncio
async def test_uk(hass: HomeAssistant) -> None:
    """Test UK Holidays."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={"country": "GB", "subdiv": "England"},
        title="UK Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state == config_entries.ConfigEntryState.LOADED

    uk_holidays = hass.states.get("calendar.uk_holidays")
    state = uk_holidays.state
    next_date = uk_holidays.attributes["next_date"]
    next_holiday = uk_holidays.attributes["next_holiday"]
    holidays = uk_holidays.attributes["holidays"]
    len_holidays = len(holidays)
    assert state == "40", ERROR_STATE.format(9, state)
    assert next_holiday == "Good Friday", ERROR_NAME.format("Good Friday", next_holiday)
    assert next_date.date() == date(2020, 4, 10), ERROR_DATE.format(
        "April 10", next_date.date()
    )
    assert len_holidays == 27, ERROR_LENGTH.format(27, len_holidays)


@pytest.mark.asyncio
async def test_cz(hass: HomeAssistant) -> None:
    """Test CZ Holidays."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={"country": "CZ"},
        title="CZ Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state == config_entries.ConfigEntryState.LOADED
    cz_holidays = hass.states.get("calendar.cz_holidays")
    state = cz_holidays.state
    next_date = cz_holidays.attributes["next_date"]
    next_holiday = cz_holidays.attributes["next_holiday"]
    holidays = cz_holidays.attributes["holidays"]
    len_holidays = len(holidays)
    assert state == "40", ERROR_STATE.format(9, state)
    assert next_holiday == "Velký pátek", ERROR_NAME.format("Velký pátek", next_holiday)
    assert next_date.date() == date(2020, 4, 10), ERROR_DATE.format(
        "April 10", next_date.date()
    )
    assert len_holidays == 39, ERROR_LENGTH.format(39, len_holidays)


@pytest.mark.asyncio
async def test_se(hass: HomeAssistant) -> None:
    """Test SE Holidays."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={"country": "SE"},
        title="SE Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state == config_entries.ConfigEntryState.LOADED
    se_holidays = hass.states.get("calendar.se_holidays")
    state = se_holidays.state
    next_date = se_holidays.attributes["next_date"]
    next_holiday = se_holidays.attributes["next_holiday"]
    holidays = se_holidays.attributes["holidays"]
    len_holidays = len(holidays)
    assert state == "40", ERROR_STATE.format(9, state)
    assert next_holiday == "Good Friday", ERROR_NAME.format("Good Friday", next_holiday)
    assert next_date.date() == date(2020, 4, 10), ERROR_DATE.format(
        "April 10", next_date.date()
    )
    assert len_holidays == 48, ERROR_LENGTH.format(48, len_holidays)


@pytest.mark.asyncio
async def test_pop_uk(hass: HomeAssistant) -> None:
    """Test Pop Holidays."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={
            "country": "GB",
            "subdiv": "UK",
            "observed": True,
            "holiday_pop_named": [
                "St. Patrick's Day [Northern Ireland]",
            ],
        },
        title="UK Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state == config_entries.ConfigEntryState.LOADED
    uk_holidays = hass.states.get("calendar.uk_holidays")
    state = uk_holidays.state
    next_date = uk_holidays.attributes["next_date"]
    next_holiday = uk_holidays.attributes["next_holiday"]
    holidays = uk_holidays.attributes["holidays"]
    len_holidays = len(holidays)
    assert state == "40", ERROR_STATE.format(40, state)
    assert next_holiday == "Good Friday", ERROR_NAME.format("Good Friday", next_holiday)
    assert next_date.date() == date(2020, 4, 10), ERROR_DATE.format(
        "April 10", next_date.date()
    )
    assert len_holidays == 40, ERROR_LENGTH.format(40, len_holidays)


@pytest.mark.asyncio
async def test_pop_texas(hass: HomeAssistant) -> None:
    """Test Pop Holidays."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={
            "country": "US",
            "subdiv": "TX",
            "observed": True,
            "holiday_pop_named": [
                "Emancipation Day In Texas; Juneteenth National Independence Day",
            ],
        },
        title="US Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state == config_entries.ConfigEntryState.LOADED
    us_holidays = hass.states.get("calendar.us_holidays")
    state = us_holidays.state
    next_date = us_holidays.attributes["next_date"]
    next_holiday = us_holidays.attributes["next_holiday"]
    holidays = us_holidays.attributes["holidays"]
    len_holidays = len(holidays)
    assert state == "1", ERROR_STATE.format(1, state)
    assert next_holiday == "Texas Independence Day", ERROR_NAME.format(
        "Texas Independence Day", next_holiday
    )
    assert next_date.date() == date(2020, 3, 2), ERROR_DATE.format(
        "April 10", next_date.date()
    )
    assert len_holidays == 65, ERROR_LENGTH.format(65, len_holidays)
