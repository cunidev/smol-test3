```python
'''
Eventim Spawner for Geocentric spawners
'''
from geocentric.geocentric import Geocentric
from geocentric.geo_lookup import geocode
import requests
from bs4 import BeautifulSoup

class EventimSpawner:
    LIST_URLS      = [ 'https://www.eventim.de/events.html' ]
    API_KEY        = 'eventim_api_key'
    API_SECRET     = 'eventim_api_secret'
    API_WRITE_MODE = 'debug'
    
    api = Geocentric(API_KEY, API_SECRET)
    
    def get_existing_events(self):
        return self.api.get_upcoming_events()
    
    def fetch_list(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('div', class_='eventItem')
    
    def fetch_item(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')
    
    def parse_list(self, lst):
        events = []
        for item in lst:
            event_url = item.find('a')['href']
            event_page = self.fetch_item(event_url)
            events.append(self.parse_item(event_page))
        return events
    
    def parse_item(self, item):
        event = {}
        event['what'] = {
            'name': item.find('h1').text,
            'description': item.find('div', class_='eventInfo').text,
            'categories': [cat.text for cat in item.find_all('a', class_='category')],
            'image': item.find('img')['src'],
            'links': [{'name': link.text, 'href': link['href']} for link in item.find_all('a')]
        }
        event['when'] = [{'start': item.find('div', class_='eventDate').text}]
        event['where'] = [{'name': item.find('div', class_='venue').text, 'coords': geocode(item.find('div', class_='venue').text)}]
        event['who'] = {'name': item.find('div', class_='organizer').text}
        event['how'] = {'admission': {'price': item.find('div', class_='price').text}}
        event['meta'] = {'source': {'name': 'Eventim', 'href': item.find('link')['href']}}
        return event
    
    def compute_update(self, old_list, new_list):
        return [event for event in new_list if event not in old_list]
    
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