Houseshares
===========

Scrape and parse housemate-wanted advertisments from Gumtree, and output Json. A Javascript frontend uses this to produce a nice map-based interface.


Running
-------

Start everything:

    python houseshares

or use Foreman: `foreman start`.

The default port is 5000, though if the environment specifies one it'll use that instead.

The frontend is at:

    /web/index.html

Which calls the API:

    /api/LOCATION/MINUTES

eg `localhost:5000/api/london/5` for adverts in London listed in the last five minutes.
