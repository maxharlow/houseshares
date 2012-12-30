# coding=utf-8

import datetime

class Advert(object):

	def __init__(self, uri):
		self.uri = uri
		self.title = None
		self.price = None
		self.location = None
		self.location_coordinates = None
		self.room_type = None
		self.date_available = None
		self.property_type = None
		self.seller_type = None
		self.phone_number = None
		self.date_posted = None
		self.description = None
		self.photos = []

	def __str__(self):
		text = ('----------------------------------------------------------------------------------------------------'
			'\n{title}'
			'\n£{price} pw'
			'\n'
			'\nLocation:		{location} {location_coordinates}'
			'\nRoom type:		{room_type}'
			'\nDate available:		{date_available}'
			'\nProperty type:		{property_type}'
			'\nSeller type:		{seller_type}'
			'\nPhone number:		{phone_number}'
			'\nDate posted:		{date_posted}'
			'\n'
			'\n{description}'
			'\n'
			'\n{photos}'
			'\n'
			'\n{uri}'
			'\n----------------------------------------------------------------------------------------------------')
		values = {
			'title': str(self.title),
			'price': str(self.price),
			'location': str(self.location),
			'location_coordinates': str(self.location_coordinates) if self.location_coordinates is not None else '',
			'room_type': str(self.room_type),
			'date_available': str(self.date_available),
			'property_type': str(self.property_type),
			'seller_type': str(self.seller_type),
			'phone_number': str(self.phone_number) if self.phone_number is not None else '',
			'date_posted': str(self.date_posted),
			'description': str(self.description),
			'photos': str([str(p) for p in self.photos]),
			'uri': str(self.uri)}
		return text.format(**values)

