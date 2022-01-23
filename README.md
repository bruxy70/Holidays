[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) [![Holidays](https://img.shields.io/github/v/release/bruxy70/Holidays.svg?1)](https://github.com/bruxy70/Holidays) ![Maintenance](https://img.shields.io/maintenance/yes/2021.svg)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&message=🥨&color=black&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=6f4e37)](https://www.buymeacoffee.com/3nXx0bJDP)

# Holidays

The `holidays` componnent is a **Home Assistant** integration that creates `calendar` entities with a list of public holidays in a country, based on the Python [Holidays](https://github.com/dr-prodigy/python-holidays) library.
It's primary purpose is to work with [garbage_collection](https://github.com/bruxy70/Garbage-Collection#public-holidays) integration to automatically move entities with `manual_update` automation **blueprints**. But it can also be used independently to show next public holiday in given country (or multiple countries).

## Table of Contents
* [Installation](#installation)
  + [Manual Installation](#manual-installation)
  + [Installation via Home Assistant Community Store (HACS)](#installation-via-home-assistant-community-store-hacs)
* [Parameters](#Parameters)
* [State and Attributes](#state-and-attributes)

## Installation

### MANUAL INSTALLATION
1. Download the
   [latest release](https://github.com/bruxy70/Holidays/releases/latest).
2. Unpack the release and copy the `custom_components/holidays` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Add the `Holidays` integration

### INSTALLATION VIA Home Assistant Community Store (HACS)
1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Search for and install the "Holidays" integration.
4. Restart Home Assistant.
5. Go to `Configuration`/`Devices & Services` hit the `+ ADD INTEGRATION` button and and add the `Holidays` integration. <br />If you would like to add more than 1 calendar, click on the `+ ADD INTEGRATION` button again and add another `Holidays` integration instance.
6. Configure the parameters

## Parameters
|Parameter |Required|Description
|:----------|----------|------------
| `country` | Yes | Country holidays - the country code (see [holidays](https://github.com/dr-prodigy/python-holidays) for the list of valid country codes).<br/>*Example:* `US` 
| `holiday_pop_named` | No | Ignore holidays (list of holiday names) *Example:* `"Columbus Day"`, `"Veterans Day"`
| `prov` | No | Province (see [holidays](https://github.com/dr-prodigy/python-holidays) ).
| `state` | No | State (see [holidays](https://github.com/dr-prodigy/python-holidays) ).
| `observed` | No | Observed (see [holidays](https://github.com/dr-prodigy/python-holidays) ).

## State and Attributes
### `state`
The State contains the number of days to the next country holiday. It is `0` if today is a public holiday.

### Attributes
| Attribute | Description
|:----------|------------
| `next_date` | The date of holiday
| `holidays` | List of used country (last year, this year and next year). This is used by the `garbage_collection` blueprints to offset collections if they fall on a public holiday (or if holiday was earlier on in the week)
