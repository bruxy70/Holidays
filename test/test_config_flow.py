"""Test the Simple Integration config flow."""
from unittest.mock import patch

from homeassistant import config_entries, data_entry_flow, setup
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.holidays import const
from custom_components.holidays.const import DOMAIN


async def test_config_flow(hass: HomeAssistant) -> None:
    """Test we get the form."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    # Initialise Config Flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert "type" in result and "step_id" in result and "flow_id" in result

    # Check that the config flow shows the user form as the first step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    # If a user were to enter `GB` for country,
    # it would result in this function call
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={"name": "English calendar", "country": "GB"},
    )
    assert (
        "type" in result
        and "step_id" in result
        and "flow_id" in result
        and "errors" in result
    )

    # Should pass to the subdiv step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "subdiv"
    assert result["errors"] == {}

    # ...add England for subdiv
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={"subdiv": "England"},
    )
    assert (
        "type" in result
        and "step_id" in result
        and "flow_id" in result
        and "errors" in result
    )
    # Should pass to the pop step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "pop"
    assert result["errors"] == {}

    # ... wil leave pop enpty
    with patch(
        "custom_components.holidays.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={},
        )
    assert "type" in result and "data" in result
    # Should create entry
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    del result["data"]["unique_id"]
    assert result["data"] == {
        "country": "GB",
        "subdiv": "England",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_options_flow(hass: HomeAssistant) -> None:
    """Test we get the form."""

    # Create MockConfigEntry
    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        data={"country": "GB", "subdiv": "England"},
        title="UK Holidays",
    )
    config_entry.add_to_hass(hass)

    # Initialise Options Flow
    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert "type" in result and "step_id" in result and "flow_id" in result

    # Check that the first options step is user
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "init"

    # Enter data into the form
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"country": "GB"},
    )
    assert (
        "type" in result
        and "step_id" in result
        and "flow_id" in result
        and "errors" in result
    )

    # Should pass to the subdiv step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "subdiv"
    assert result["errors"] == {}

    # ...add England for subdiv
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"subdiv": "England"},
    )
    assert (
        "type" in result
        and "step_id" in result
        and "flow_id" in result
        and "errors" in result
    )
    # Should pass to the pop step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "pop"
    assert result["errors"] == {}

    # ... wil leave pop enpty
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={},
    )
    assert "type" in result and "data" in result
    # Should create entry
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["data"] == {"country": "GB", "subdiv": "England"}
