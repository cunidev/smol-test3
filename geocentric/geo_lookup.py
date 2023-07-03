```python
# Geographic Lookup Helper Library

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="test-geocentric")

def geocode(addr, default=None): # returns coord tuple
    try:
        location = geolocator.geocode(addr)
        if location is not None:
            return (location.latitude, location.longitude)
        else:
            return default
    except GeocoderTimedOut:
        return geocode(addr, default)
```