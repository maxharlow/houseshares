# coding=utf-8

import datetime
import jsonpickle
from flask import Flask
from scrape import ScrapeGumtree

app = Flask(__name__)

@app.route('/houseshares/<location>/<int:to_minutes_ago>')
def houseshares(location, to_minutes_ago):
	to_date = datetime.datetime.now() - datetime.timedelta(minutes=to_minutes_ago)
	gumtree = ScrapeGumtree()
	listings = gumtree.scrape_listings_by_location(location, to_date)
	listings_json = jsonpickle.encode(listings, unpicklable=False)
	return listings_json

