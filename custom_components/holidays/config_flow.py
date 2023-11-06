"""Adds config flow for GarbageCollection."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Dict, cast

import holidays
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
localised_countries: dict = holidays.list_localized_countries()
sorted_countries: list = sorted([holiday for holiday in supported_countries])
country_codes = [selector.SelectOptionDict(value=c, label=c) for c in sorted_countries]


@callback
async def choose_second_step(options: Dict[str, Any]) -> str:
    """Return next step_id for options flow."""
    country = options.get(const.CONF_COUNTRY)
    subdivs = supported_countries[country]
    languages = localised_countries.get(country, "")
    if subdivs or languages:
        # If country was changed, remove subdivs for the wrong country
        if const.CONF_SUBDIV in options and (
            not subdivs or options[const.CONF_SUBDIV] not in subdivs
        ):
            del options[const.CONF_SUBDIV]
        if const.CONF_LANGUAGES in options and (
            not languages or options[const.CONF_LANGUAGES] not in languages
        ):
            del options[const.CONF_LANGUAGES]
        return "subdiv"
    if const.CONF_SUBDIV in options:
        del options[const.CONF_SUBDIV]
    if const.CONF_LANGUAGES in options:
        del options[const.CONF_LANGUAGES]
    return await choose_third_step(options)


@callback
async def choose_third_step(options: Dict[str, Any]) -> str:
    """Return next step_id for options flow."""
    if const.CONF_HOLIDAY_POP_NAMED in options:
        # Remove holidays that do not exist
        this_year = dt_util.now().date().year
        years = [this_year - 1, this_year, this_year + 1]
        hol = create_holidays(
            years,
            options.get(const.CONF_COUNTRY, ""),
            options.get(const.CONF_SUBDIV, ""),
            options.get(const.CONF_LANGUAGES, ""),
            False,
        )
        holiday_names = list(dict.fromkeys(hol.values()))
        for pop in options[const.CONF_HOLIDAY_POP_NAMED]:
            if pop not in holiday_names:
                options[const.CONF_HOLIDAY_POP_NAMED].remove(pop)
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


async def general_options_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Generate options schema."""
    return vol.Schema(
        {
            optional(
                const.CONF_ICON_NORMAL, handler.options, const.DEFAULT_ICON_NORMAL
            ): selector.IconSelector(),
            optional(
                const.CONF_ICON_TODAY, handler.options, const.DEFAULT_ICON_TODAY
            ): selector.IconSelector(),
            optional(
                const.CONF_ICON_TOMORROW, handler.options, const.DEFAULT_ICON_TOMORROW
            ): selector.IconSelector(),
            optional(const.CONF_COUNTRY, handler.options): selector.SelectSelector(
                selector.SelectSelectorConfig(options=country_codes)
            ),
            optional(const.CONF_OBSERVED, handler.options, True): bool,
        }
    )


async def general_config_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Generate config schema."""
    return vol.Schema(
        {
            optional(CONF_NAME, handler.options): selector.TextSelector(),
            optional(
                const.CONF_ICON_NORMAL, handler.options, const.DEFAULT_ICON_NORMAL
            ): selector.IconSelector(),
            optional(
                const.CONF_ICON_TODAY, handler.options, const.DEFAULT_ICON_TODAY
            ): selector.IconSelector(),
            optional(
                const.CONF_ICON_TOMORROW, handler.options, const.DEFAULT_ICON_TOMORROW
            ): selector.IconSelector(),
            optional(const.CONF_COUNTRY, handler.options): selector.SelectSelector(
                selector.SelectSelectorConfig(options=country_codes)
            ),
            optional(const.CONF_OBSERVED, handler.options, True): bool,
        }
    )


async def subdiv_config_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Second step."""
    country = handler.options.get(const.CONF_COUNTRY)
    options = {}
    if country in supported_countries:
        subdivs = [
            selector.SelectOptionDict(value=s, label=s)
            for s in supported_countries[handler.options.get(const.CONF_COUNTRY)]
        ]
        options[optional(const.CONF_SUBDIV, handler.options)] = selector.SelectSelector(
            selector.SelectSelectorConfig(options=subdivs)
        )
    if country in localised_countries:
        languages = [
            selector.SelectOptionDict(value=s, label=s)
            for s in localised_countries[handler.options.get(const.CONF_COUNTRY)]
        ]
        options[
            optional(const.CONF_LANGUAGES, handler.options)
        ] = selector.SelectSelector(selector.SelectSelectorConfig(options=languages))
    return vol.Schema(options)


async def pop_config_schema(
    handler: SchemaConfigFlowHandler | SchemaOptionsFlowHandler,
) -> vol.Schema:
    """Last step."""
    this_year = dt_util.now().date().year
    years = [this_year - 1, this_year, this_year + 1]
    hol = create_holidays(
        years,
        handler.options.get(const.CONF_COUNTRY, ""),
        handler.options.get(const.CONF_SUBDIV, ""),
        handler.options.get(const.CONF_LANGUAGES, ""),
        False,
    )
    holiday_names = sorted(list(dict.fromkeys(hol.values())))
    list_holidays = [selector.SelectOptionDict(value=h, label=h) for h in holiday_names]
    return vol.Schema(
        {
            optional(
                const.CONF_HOLIDAY_POP_NAMED, handler.options
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list_holidays,
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            )
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
