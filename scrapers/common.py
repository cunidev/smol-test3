```python
import requests
from bs4 import BeautifulSoup
from geocentric.geocentric import Geocentric
from geocentric.geo_lookup import geocode

class Spawner:
    LIST_URLS      = [ 'https://ex.am.ple/feed.php' ]
    API_KEY        = 'often_same_as_source'
    API_SECRET     = 'kittenskittenskittens'
    API_WRITE_MODE = 'debug'
    
    api = Geocentric(API_KEY, API_SECRET)
    
    def get_existing_events(self):
        return self.api.get_upcoming_events()
    
    def fetch_list(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    
    def fetch_item(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    
    def parse_list(self, lst):
        pass
    
    def parse_item(self, item):
        pass
        
    def compute_update(self, old_list, new_list):
        pass
        
    def execute(self):
        new_events = []
        for url in self.LIST_URLS:
            current_events = self.fetch_list(url)
            parsed_current_events = self.parse_list(current_events)
            new_events.extend(parsed_current_events)
        
        old_events = self.get_existing_events()
        updated_list = self.compute_update(old_events, new_events)
        
        self.api.push(updated_list, allow_updates=True)
```