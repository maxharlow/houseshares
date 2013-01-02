# coding=utf-8

import re
import time
import datetime
import urllib
import urllib2
from bs4 import BeautifulSoup
from model import Advert

class ScrapeGumtree(object):

	def scrape_listings_by_location(self, location, to_listed_date):
		uri = u'http://www.gumtree.com/search?q=&category=double-room-flatshare&search_location=' + urllib.quote(location)
		return self.scrape_listings(uri, to_listed_date)

	def scrape_listings(self, uri, to_listed_date):
		print('Scraping Gumtree listing: ' + uri)
		page = urllib2.urlopen(uri)
		listing_html = BeautifulSoup(page)
		listing_adverts_html = listing_html.find_all('ul', class_='ad-listings')
		if not listing_adverts_html:
			return [] # there are no listings on this page -- invalid uri?
		listing_adverts_html = listing_adverts_html[0] if len(listing_adverts_html) == 1 else listing_adverts_html[1]  # skip featured listings
		listing_adverts_html = listing_adverts_html.find_all('li', class_='hlisting')
		adverts = []
		for listing_advert_html in listing_adverts_html:
			advert_uri = listing_advert_html.find('a', class_='description')['href']
			advert = Advert(advert_uri)
			advert.date_posted = self._extract_date_posted(listing_advert_html)
			if advert.date_posted < to_listed_date:
				return adverts
			time.sleep(1) # please don't ban me
			self.scrape_advert(advert_uri, advert)
			adverts.append(advert)
		next_uri = listing_html.find('li', class_='pag-next').contents[0]['href']
		return adverts + self.scrape_listing(next_uri, to_listed_date)

	def scrape_advert(self, uri, advert=None):
		print('Scraping Gumtree advert: ' + uri)
		page = urllib2.urlopen(uri)
		advert_html = BeautifulSoup(page)
		advert = Advert(uri) if advert is None else advert
		advert.title = self._extract_title(advert_html)
		advert.price = self._extract_price(advert_html)
		advert.location = self._extract_location(advert_html)
		advert.location_coordinates = self._extract_location_coordinates(advert_html)
		advert.room_type = self._extract_room_type(advert_html)
		advert.date_available = self._extract_date_available(advert_html)
		advert.property_type = self._extract_property_type(advert_html)
		advert.seller_type = self._extract_seller_type(advert_html)
		advert.phone_number = self._extract_phone_number(advert_html)
		advert.description = self._extract_description(advert_html)
		advert.photos = self._extract_photos(advert_html)
		return advert

	def _extract_date_posted(self, listing_advert_html):
		location = listing_advert_html.find('span', class_='dtlisted')
		value = location.attrs['title']
		value = datetime.datetime.strptime(value, '%Y%m%dT%H%M%S+0000') # Gumtree doesn't appear to use time zones here
		return value

	def _extract_title(self, advert_html):
		location = advert_html.find('h1')
		value = unicode(location.contents[0])
		value = value.encode('utf-8')
		return value

	def _extract_price(self, advert_html):
		location = advert_html.find('span', class_='ad-price')
		value = location.get_text()
		value = value.replace(u'£', u'')
		value = value.replace(u',', u'')
		if 'pm' in value:
			value = value.replace(u'pm', u'')
			value = round((int(value) * 12) / 52.2) # convert to weekly
		else: # presume weekly
			value = value.replace(u'pw', u'')
		return int(value)

	def _extract_location(self, advert_html):
		location = advert_html.find('span', class_='ad-location')
		value = location.get_text()
		return value

	def _extract_location_coordinates(self, advert_html):
		location = advert_html.find('a', class_='open_map')
		if location is not None:
			value = location.get('data-target')
			value = value.split('center=')[1]
			value = value.split('&')[0]
			value = value.split(',')
			value = (float(value[0]), float(value[1]))
		else:
			value = None
		return value

	def _extract_room_type(self, advert_html):
		location = advert_html.find('h3', text='Room type').find_next()
		value = location.get_text()
		value = value.encode('utf-8')
		return value

	def _extract_date_available(self, advert_html):
		location = advert_html.find('h3', text='Date available').find_next()
		value = location.contents[0]
		try:
			value = datetime.datetime.strptime(value, '%d/%m/%y').date()
		except ValueError: # some people manage to enter invalid dates...
			value = datetime.date.min
		return value

	def _extract_property_type(self, advert_html):
		location = advert_html.find('h3', text='Property type').find_next()
		value = location.get_text()
		value = value.encode('utf-8')
		return value

	def _extract_seller_type(self, advert_html):
		location = advert_html.find('h3', text='Seller type').find_next()
		value = location.get_text()
		value = value.encode('utf-8')
		return value

	def _extract_phone_number(self, advert_html):
		location = advert_html.find('span', class_='phone')
		if location is not None:
			value = location.get_text()
			value = value.encode('utf-8')
		else:
			value = None
		return value

	def _extract_description(self, advert_html):
		location = advert_html.find('div', id='vip-description-text')
		value = location.get_text().strip()
		value = value.encode('utf-8')
		return value

	def _extract_photos(self, advert_html):
		location = advert_html.find('ul', class_='gallery-main')
		values = re.findall(r'data-target="(.+?)"', unicode(location))
		values = [uri for uri in values if u'maps' not in uri]
		return values

