"""Test calendar for simple integration."""
from datetime import date

from custom_components.holidays import const
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry


async def test_setup(hass: HomeAssistant):  # pylint: disable=unused-argument
    """Check config_entry is created."""
    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        data={"country": "US", "subdiv": "CZ"},
        title="US Holidays",
    )
    assert config_entry.entry_id != None


async def test_uk(hass: HomeAssistant):
    """Test UK Holidays."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        data={"country": "GB", "subdiv": "England"},
        title="UK Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    uk_holidays = hass.states.get("calendar.uk_holidays")
    state = uk_holidays.state
    next_date = uk_holidays.attributes["next_date"]
    next_holiday = uk_holidays.attributes["next_holiday"]
    holidays = uk_holidays.attributes["holidays"]
    len_holidays = len(holidays.strip().split("\n"))
    assert state == "9", f"Next holiday should be in 9 days, not {state}"
    assert (
        next_holiday == "Good Friday"
    ), f"Next holiday should be Good Friday, not {next_holiday}"
    assert next_date.date() == date(
        2020, 4, 10
    ), f"Next holiday should be on April 10, not {next_date.date()}"
    assert len_holidays == 27, f"Holidays should have 27 items, not {len_holidays}"


async def test_cz(hass: HomeAssistant):
    """Test CZ Holidays."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        data={"country": "CZ"},
        title="CZ Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    cz_holidays = hass.states.get("calendar.cz_holidays")
    state = cz_holidays.state
    next_date = cz_holidays.attributes["next_date"]
    next_holiday = cz_holidays.attributes["next_holiday"]
    holidays = cz_holidays.attributes["holidays"]
    len_holidays = len(holidays.strip().split("\n"))
    assert state == "9", f"Next holiday should be in 9 days, not {state}"
    assert (
        next_holiday == "Velký pátek"
    ), f"Next holiday should be Velký pátek, not {next_holiday}"
    assert next_date.date() == date(
        2020, 4, 10
    ), f"Next holiday should be on April 10, not {next_date.date()}"
    assert len_holidays == 39, f"Holidays should have 39 items, not {len_holidays}"
