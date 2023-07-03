```python
import requests
import json

class Geocentric:
    API_URL = 'https://api.geocentric.com'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_upcoming_events(self):
        return self._get_events('upcoming')

    def get_past_events(self):
        return self._get_events('past')

    def _get_events(self, mode):
        response = requests.get(f'{self.API_URL}/events/{mode}', headers=self._get_headers())
        return response.json()

    def push(self, events, allow_updates=False):
        data = {
            'events': events,
            'allow_updates': allow_updates
        }
        response = requests.post(f'{self.API_URL}/events', headers=self._get_headers(), data=json.dumps(data))
        return response.json()

    def _get_event(self, event_id):
        response = requests.get(f'{self.API_URL}/events/{event_id}', headers=self._get_headers())
        return response.json()

    def _create_event(self, event):
        response = requests.post(f'{self.API_URL}/events', headers=self._get_headers(), data=json.dumps(event))
        return response.json()

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-API-KEY': self.api_key,
            'X-API-SECRET': self.api_secret
        }
```