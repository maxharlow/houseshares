Houseshares
===========

Scrape and parse housemate-wanted advertisments from Gumtree, and output Json. A Javascript web app then overlays a nice Google Maps interface.


Running
-------

Using Python:
    python housemates

Or use Foreman:
    foreman start
Which is used if you deploy to Heroku.

The default port is 5000, though if the environment specifies one, it'll use that instead.

The web interface is at:
    /web/index.html

The API:
    /api/_LOCATION_/_MINUTES AGO_
eg `localhost:5000/api/london/5` for adverts in London listed in the last five minutes.
