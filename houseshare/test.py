# coding=utf-8

import datetime
from scrape import ScrapeGumtree

print('Scraping...')
gumtree = ScrapeGumtree()
location = u'london'
to_date = datetime.datetime.now() - datetime.timedelta(minutes=5)
listings = gumtree.scrape_listings_by_location(location, to_date)

print('\nFound adverts:')
for advert in listings:
	print(str(advert))

