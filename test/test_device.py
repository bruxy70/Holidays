"""Test all frequencies (except blank)."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.holidays import const


async def test_device(hass: HomeAssistant) -> None:
    """Test device registry."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={"country": "CZ"},
        title="CZ Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    device_registry = dr.async_get(hass)
    device = device_registry.async_get_device(
        identifiers={(const.DOMAIN, config_entry.entry_id)}
    )
    assert device is not None
    assert device.manufacturer == "bruxy70"
    assert device.name == "CZ Holidays"


async def test_device_info(hass: HomeAssistant) -> None:
    """Test device info."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={"country": "CZ"},
        title="CZ Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    sensor = hass.data["holidays"]["calendar"]["calendar.cz_holidays"]
    assert sensor.device_info == {
        "identifiers": {("holidays", sensor.unique_id)},
        "name": "CZ Holidays",
        "manufacturer": "bruxy70",
    }


async def test_entity(hass: HomeAssistant) -> None:
    """Test entity registry."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={"country": "CZ"},
        title="CZ Holidays",
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    entity_registry = er.async_get(hass)
    entity = entity_registry.async_get_entity_id(
        platform=const.DOMAIN, domain="calendar", unique_id=config_entry.entry_id
    )
    assert entity == "calendar.cz_holidays"
