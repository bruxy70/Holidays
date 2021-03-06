"""Adds config flow for GarbageCollection."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Dict, cast

import holidays
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
    SchemaFlowMenuStep,
    SchemaOptionsFlowHandler,
)

from . import const, create_holidays

supported_countries: dict = holidays.list_supported_countries()
country_codes: list = sorted([holiday for holiday in supported_countries])


@callback
def choose_second_step(options: Dict[str, Any]) -> str:
    """Return next step_id for options flow."""
    subdivs = supported_countries[options.get(const.CONF_COUNTRY)]
    if subdivs:
        # If country was changed, remove subdivs for the wrong country
        if const.CONF_SUBDIV in options and options[const.CONF_SUBDIV] not in subdivs:
            del options[const.CONF_SUBDIV]
        return "subdiv"
    if const.CONF_SUBDIV in options:
        del options[const.CONF_SUBDIV]
    return choose_third_step(options)


@callback
def choose_third_step(options: Dict[str, Any]) -> str:
    """Return next step_id for options flow."""
    if const.CONF_HOLIDAY_POP_NAMED in options:
        # Remove holidays that do not exist
        hol = create_holidays(
            [dt_util.now().date().year],
            options.get(const.CONF_COUNTRY, ""),
            options.get(const.CONF_SUBDIV, ""),
            options.get(const.CONF_OBSERVED, True),
        )
        for pop in options[const.CONF_HOLIDAY_POP_NAMED]:
            if pop not in hol or "(Observed)" in pop:
                del options[pop]
    return "pop"


def required(
    key: str, options: Dict[str, Any], default: Any | None = None
) -> vol.Required:
    """Return vol.Required."""
    if isinstance(options, dict) and key in options:
        suggested_value = options[key]
    elif default is not None:
        suggested_value = default
    else:
        return vol.Required(key)
    return vol.Required(key, description={"suggested_value": suggested_value})


def optional(
    key: str, options: Dict[str, Any], default: Any | None = None
) -> vol.Optional:
    """Return vol.Optional."""
    if isinstance(options, dict) and key in options:
        suggested_value = options[key]
    elif default is not None:
        suggested_value = default
    else:
        return vol.Optional(key)
    return vol.Optional(key, description={"suggested_value": suggested_value})


def general_options_schema(
    _,
    options: Dict[str, Any],
) -> vol.Schema:
    """Generate options schema."""
    return vol.Schema(
        {
            optional(
                const.CONF_ICON_NORMAL, options, const.DEFAULT_ICON_NORMAL
            ): selector.IconSelector(),
            optional(
                const.CONF_ICON_TODAY, options, const.DEFAULT_ICON_TODAY
            ): selector.IconSelector(),
            optional(
                const.CONF_ICON_TOMORROW, options, const.DEFAULT_ICON_TOMORROW
            ): selector.IconSelector(),
            optional(const.CONF_COUNTRY, options): vol.In(country_codes),
            optional(const.CONF_OBSERVED, options, True): bool,
        }
    )


def general_config_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
    options: Dict[str, Any],
) -> vol.Schema:
    """Generate config schema."""
    return vol.Schema(
        {
            optional(CONF_NAME, options): selector.TextSelector(),
        }
    ).extend(general_options_schema(handler, options).schema)


def subdiv_config_schema(
    _,
    options: Dict[str, Any],
) -> vol.Schema:
    """Second step."""
    subdivs = supported_countries[options.get(const.CONF_COUNTRY)]
    return vol.Schema(
        {
            optional(const.CONF_SUBDIV, options): vol.In(subdivs),
        }
    )


def pop_config_schema(
    _,
    options: Dict[str, Any],
) -> vol.Schema:
    """Last step."""
    hol = create_holidays(
        [dt_util.now().date().year],
        options.get(const.CONF_COUNTRY, ""),
        options.get(const.CONF_SUBDIV, ""),
        options.get(const.CONF_OBSERVED, True),
    )
    list_holidays = {h: h for h in sorted(hol.values()) if "(Observed)" not in h}
    return vol.Schema(
        {
            optional(const.CONF_HOLIDAY_POP_NAMED, options): cv.multi_select(
                list_holidays
            ),
        }
    )


CONFIG_FLOW: Dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "user": SchemaFlowFormStep(general_config_schema, next_step=choose_second_step),
    "subdiv": SchemaFlowFormStep(subdiv_config_schema, next_step=choose_third_step),
    "pop": SchemaFlowFormStep(pop_config_schema),
}
OPTIONS_FLOW: Dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "init": SchemaFlowFormStep(general_options_schema, next_step=choose_second_step),
    "subdiv": SchemaFlowFormStep(subdiv_config_schema, next_step=choose_third_step),
    "pop": SchemaFlowFormStep(pop_config_schema),
}


# mypy: ignore-errors
class HolidaysConfigFlowHandler(SchemaConfigFlowHandler, domain=const.DOMAIN):
    """Handle a config or options flow for Holdays."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW
    VERSION = const.CONFIG_VERSION

    @callback
    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title.

        The options parameter contains config entry options, which is the union of user
        input from the config flow steps.
        """
        return cast(str, options["name"]) if "name" in options else ""
