[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) [![Holidays](https://img.shields.io/github/v/release/bruxy70/Holidays.svg?1)](https://github.com/bruxy70/Holidays) ![Maintenance](https://img.shields.io/maintenance/yes/2021.svg)

[![Buy me a coffee](https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&message=🥨&color=black&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=6f4e37)](https://www.buymeacoffee.com/3nXx0bJDP)

# Holidays

The `holidays` componnent is a Home Assistant integration that a custom sensor with a list of public holidays in a countrt, based on the Python (Holidays)[https://github.com/dr-prodigy/python-holidays] library. It's primary purpose is to automatically move `garbage_collection` integration entities with `manual_update` automation blueprints, but can also be used independently to show next public holiday in given country.

## Table of Contents
* [Installation](#installation)
  + [Manual Installation](#manual-installation)
  + [Installation via Home Assistant Community Store (HACS)](#installation-via-home-assistant-community-store-hacs)

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
5. Add the `Holidays` integration

