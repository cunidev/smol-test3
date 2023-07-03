```python
'''
A tiny SDK and interface for Geocentric spawners
'''
from geocentric import Geocentric
from geocentric import geo_lookup
import requests
from bs4 import BeautifulSoup

class MeetupSpawner:
    LIST_URLS      = [ 'https://www.meetup.com/find/events/' ]
    API_KEY        = 'meetup_api_key'
    API_SECRET     = 'meetup_api_secret'
    API_WRITE_MODE = 'debug'
    
    api = Geocentric(API_KEY, API_SECRET)
    
    def get_existing_events(self):
        return self.api.get_upcoming_events()
    
    '''
    Scrape list of events, or single event, from a source URL
    '''
    def fetch_list(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('div', class_='eventCard')
    
    def fetch_item(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')
    
    '''
    Supporting functions: Turn a raw item into a Geocentric item list 
    '''
    def parse_list(self, lst):
        events = []
        for item in lst:
            event_url = item.find('a', class_='eventCardHead--title').get('href')
            event = self.fetch_item(event_url)
            events.append(self.parse_item(event))
        return events
    
    def parse_item(self, item):
        event = {}
        event['what'] = {
            'name': item.find('h1', class_='pageHead-headline').text.strip(),
            'description': item.find('div', class_='event-description runningText').text.strip(),
            'categories': [cat.text for cat in item.find_all('a', class_='topicLink')],
            'image': item.find('img', class_='photo-item_photo').get('src'),
            'links': [{'name': 'Meetup', 'href': item.find('link', rel='canonical').get('href')}]
        }
        event['when'] = [{
            'start': item.find('time', itemprop='startDate').get('datetime'),
            'end': item.find('time', itemprop='endDate').get('datetime'),
            'label': 'Meetup Event'
        }]
        event['where'] = [{
            'name': item.find('span', class_='venueDisplay-name').text.strip(),
            'coords': geo_lookup.geocode(item.find('p', class_='venueDisplay-venue-address').text.strip()),
            'address': item.find('p', class_='venueDisplay-venue-address').text.strip(),
            'zip': '',
            'country': ''
        }]
        event['who'] = {
            'name': item.find('span', class_='orgInfo-name').text.strip(),
            'email': '',
            'phone': '',
            'url': item.find('a', class_='orgInfo-name').get('href')
        }
        event['how'] = {
            'admission': {
                'price': 0,
                'privilege': 'Free'
            }
        }
        event['meta'] = {
            'source': {
                'name': 'Meetup',
                'href': 'https://www.meetup.com/'
            },
            'created': '',
            'updated': '',
            'version': '',
            'spawnerID': 'MeetupSpawner'
        }
        event['_id'] = ''
        return event
        
    '''
    Integrate existing with old (already published) events 
    e.g. compute updates
    '''
    def compute_update(self, old_list, new_list):
        return list(set(new_list) - set(old_list))
        
        
    '''
    More-or-less standard execution procedure (adapt if needed)
    '''
    def execute(self):
        new_events = []
        for url in self.LIST_URLS:
            current_events = self.fetch_list(url)
            parsed_current_events = self.parse_list(current_events)
            new_events.extend(parsed_current_events)
        
        print(new_events)
        
        old_events = self.get_existing_events()
        updated_list = self.compute_update(old_events, new_events)
        
        # Commit the new list of events
        self.api.push(updated_list, allow_updates=True)
```