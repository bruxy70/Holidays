[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration) [![Holidays](https://img.shields.io/github/v/release/bruxy70/Holidays.svg?1)](https://github.com/bruxy70/Holidays) ![Maintenance](https://img.shields.io/maintenance/yes/2023.svg)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&message=🥨&color=black&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=6f4e37)](https://www.buymeacoffee.com/3nXx0bJDP)

# Holidays

The `holidays` component is a **Home Assistant** helper that creates `calendar` entities with a list of public holidays in a country, based on the Python [Holidays](https://github.com/dr-prodigy/python-holidays) library.
It's primary purpose is to work with [garbage_collection](https://github.com/bruxy70/Garbage-Collection#public-holidays) helper to automatically move entities with `manual_update` automation **blueprints**. But it can also be used independently to show the next public holiday in a given country (or multiple countries).

## Table of Contents

- [Installation](#installation)
  - [Manual Installation](#manual-installation)
  - [Installation via Home Assistant Community Store (HACS)](#installation-via-home-assistant-community-store-hacs)
- [Parameters](#Parameters)
- [State and Attributes](#state-and-attributes)

## Installation

### MANUAL INSTALLATION

1. Download the
   [latest release](https://github.com/bruxy70/Holidays/releases/latest).
2. Unpack the release and copy the `custom_components/holidays` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Add the `Holidays` helper

### INSTALLATION VIA Home Assistant Community Store (HACS)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Search for and install the "Holidays" integration.
3. Restart Home Assistant.
4. Go to `Settings`/`Devices & Services`/`Helpers` hit the `+ CREATE HELPER` button and and add the `Holidays` helper.
5. Configure the parameters
6. If you would like to add more than 1 calendar, click on the `+ CREATE HELPER` button again and add another `Holidays` helper instance.

## Parameters

| Parameter            | Required | Description                                                                                                                                                         |
| :------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Country`            | Yes      | Country holidays - the country code (see [holidays](https://github.com/dr-prodigy/python-holidays) for the list of valid country codes).<br/>_Example:_ `US`        |
| `Observed`           | No       | Observed - when holidays are celebrated on dates that are not the actual event's anniversary date (see [holidays](https://github.com/dr-prodigy/python-holidays) ). |
| `Subdivision`        | No       | State/Province/District... (see [holidays](https://github.com/dr-prodigy/python-holidays) ).                                                                        |
| `Pop named holidays` | No       | Ignore holidays (select from the list of holiday names) _Example:_ `"Columbus Day"`, `"Veterans Day"`                                                               |

## State and Attributes

### `state`

The State contains the number of days to the next country holiday. It is `0` if today is a public holiday.

### Attributes

| Attribute      | Description                                                                                                                                                                                                               |
| :------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `next_date`    | The date of the next holiday                                                                                                                                                                                              |
| `next_holiday` | The name of the next holiday                                                                                                                                                                                              |
| `holidays`     | List of country holidays (last year, this year, and next year). This is used by the `garbage_collection` blueprints to offset collections if they fall on a public holiday (or if the holiday was earlier on in the week) |
