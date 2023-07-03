```python
from geocentric.geocentric import Geocentric
from geocentric.geo_lookup import geocode
import requests
from bs4 import BeautifulSoup
import datetime

class BandsintownSpawner:
    LIST_URLS      = [ 'https://www.bandsintown.com/' ]
    API_KEY        = 'bandsintown_api_key'
    API_SECRET     = 'bandsintown_api_secret'
    API_WRITE_MODE = 'debug'
    
    api = Geocentric(API_KEY, API_SECRET)
    
    def get_existing_events(self):
        return self.api.get_upcoming_events()
    
    def fetch_list(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('div', class_='event')
    
    def fetch_item(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find('div', class_='event')
    
    def parse_list(self, lst):
        events = []
        for item in lst:
            event = self.parse_item(item)
            if event:
                events.append(event)
        return events
    
    def parse_item(self, item):
        name = item.find('h2', class_='event-name').text
        description = item.find('p', class_='event-description').text
        categories = [cat.text for cat in item.find_all('span', class_='event-category')]
        image = item.find('img', class_='event-image')['src']
        links = [{'name': link.text, 'href': link['href']} for link in item.find_all('a', class_='event-link')]
        start = datetime.datetime.strptime(item.find('span', class_='event-start').text, '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(item.find('span', class_='event-end').text, '%Y-%m-%d %H:%M:%S')
        label = item.find('span', class_='event-label').text
        venue = item.find('span', class_='event-venue').text
        address = item.find('span', class_='event-address').text
        zip = item.find('span', class_='event-zip').text
        country = item.find('span', class_='event-country').text
        coords = geocode(address)
        organizer = item.find('span', class_='event-organizer').text
        email = item.find('span', class_='event-email').text
        phone = item.find('span', class_='event-phone').text
        url = item.find('a', class_='event-url')['href']
        price = float(item.find('span', class_='event-price').text)
        privilege = item.find('span', class_='event-privilege').text
        source = {'name': 'Bandsintown', 'href': self.LIST_URLS[0]}
        created = datetime.datetime.now()
        updated = datetime.datetime.now()
        version = '1.0'
        spawnerID = 'bandsintown_spawner'
        _id = name.lower().replace(' ', '-')
        
        event = {
            'what': {'name': name, 'description': description, 'categories': categories, 'image': image, 'links': links},
            'when': [{'start': start, 'end': end, 'label': label}],
            'where': [{'name': venue, 'coords': coords, 'address': address, 'zip': zip, 'country': country}],
            'who': {'name': organizer, 'email': email, 'phone': phone, 'url': url},
            'how': {'admission': {'price': price, 'privilege': privilege}},
            'meta': {'source': source, 'created': created, 'updated': updated, 'version': version, 'spawnerID': spawnerID},
            '_id': _id
        }
        
        return event
    
    def compute_update(self, old_list, new_list):
        updated_list = old_list
        for new_event in new_list:
            if new_event not in old_list:
                updated_list.append(new_event)
        return updated_list
    
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