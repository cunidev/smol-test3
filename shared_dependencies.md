Shared Dependencies:

1. **Geocentric Class**: The Geocentric class from the geocentric.geocentric library is shared among all the scraper files (EventimSpawner.py, MeetupSpawner.py, BandsintownSpawner.py). It provides methods for getting upcoming and past events, pushing events to the API, and creating events.

2. **Geocode Function**: The geocode function from the geocentric.geo_lookup library is shared among all the scraper files. It is used to get the geographical coordinates of an address.

3. **Spawner Class**: The Spawner class is a template that is shared among all the scraper files. It provides methods for fetching and parsing lists and items, computing updates, and executing the scraping process.

4. **EventSchema**: The EventSchema is shared among all the scraper files. It defines the structure of the event data that is being scraped.

5. **Common Constants**: The LIST_URLS, API_KEY, API_SECRET, and API_WRITE_MODE constants are shared among all the scraper files. They are used for configuring the scraping process.

6. **Common Methods**: The fetch_list, fetch_item, parse_list, parse_item, compute_update, and execute methods are shared among all the scraper files. They are used for fetching, parsing, updating, and executing the scraping process.

7. **Common Libraries**: The requests and bs4 libraries are shared among all the scraper files. They are used for making HTTP requests and parsing HTML respectively.