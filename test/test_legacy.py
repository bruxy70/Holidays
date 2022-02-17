"""Test listing holidays for England using Country GB, Subdiv England."""
from pprint import pprint
from typing import Any, Dict

import holidays  # pylint: disable=import-self

kwargs: Dict[str, Any] = {"years": [2022], "prov": "BC"}

# pylint: disable=maybe-no-member
pprint(holidays.CountryHoliday("CA", **kwargs))

