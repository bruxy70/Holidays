"""Test listing holidays for England using Country GB, Subdiv England."""
from pprint import pprint
from typing import Any, Dict

import holidays  # pylint: disable=import-self

kwargs: Dict[str, Any] = {"years": [2022]}
COUNTRY1 = "England"
# pylint: disable=maybe-no-member
print("Using Country")
pprint(holidays.CountryHoliday(COUNTRY1, **kwargs))

COUNTRY2 = "GB"
kwargs["subdiv"] = "England"
# pylint: disable=maybe-no-member
print("Using Country")
pprint(holidays.CountryHoliday(COUNTRY2, **kwargs))
