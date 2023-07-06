"""Test migration from older version."""
import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.holidays import const


# @pytest.mark.asyncio
async def test_version1(hass: HomeAssistant) -> None:
    """Migration from version 1."""

    config_entry1: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN, data={"country": "England"}, title="English", version=1
    )
    config_entry1.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry1.entry_id)
    await hass.async_block_till_done()
    assert config_entry1.options == {"country": "GB", "subdiv": "England"}
    assert config_entry1.data == {}
    assert config_entry1.state == config_entries.ConfigEntryState.LOADED

    config_entry2: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        data={"country": "US", "state": "CA"},
        title="US",
        version=1,
    )
    config_entry2.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry2.entry_id)
    await hass.async_block_till_done()
    assert config_entry2.options == {"country": "US", "subdiv": "CA"}
    assert config_entry2.data == {}
    assert config_entry2.state == config_entries.ConfigEntryState.LOADED


# @pytest.mark.asyncio
async def test_version2(hass: HomeAssistant) -> None:
    """Migration from version 2."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN, data={"country": "CZ"}, title="CZ Holidays", version=2
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.options == {"country": "CZ"}
    assert config_entry.data == {}
    assert config_entry.state == config_entries.ConfigEntryState.LOADED
