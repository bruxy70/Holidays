"""Test listing holidays for England using Country GB, Subdiv England."""
from pprint import pprint
from typing import Any, Dict

import holidays  # pylint: disable=import-self

#print("List supported countries")
#pprint(holidays.list_supported_countries())

kwargs: Dict[str, Any] = {"years": [2022]}
COUNTRY2 = "GB"
obj_holidays = getattr(holidays,COUNTRY2)(**kwargs)
if hasattr(obj_holidays,"subdiv"):
    print(COUNTRY2 ,"has SUBDIV")
    kwargs["subdiv"] = "England"
    obj_holidays = getattr(holidays,COUNTRY2)(**kwargs)
else:
    print("%S does not have SUBDIV",COUNTRY2)
pprint(obj_holidays)


