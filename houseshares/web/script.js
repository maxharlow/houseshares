function Houseshares() {
	var housesharesApiUri = 'http://localhost:5000/api';
	var markerIcon = 'http://labs.google.com/ridefinder/images/mm_20_red.png';
	var markerIconSelected = 'http://maps.google.com/mapfiles/marker_orange.png';
	var map;
	var mapBox;
	var mapMarkers = [];
	var selectedMarker;

	function init() {
		var mapSettings = {
			navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL},
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		mapBox = document.querySelector("#map");
		map = new google.maps.Map(mapBox, mapSettings);
		centreMap();
		document.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); search(); });
	}

	function search() {
		document.querySelector('form button').disabled = true;
		showLoadingIndicator(true);
		var location = document.querySelector('[name=location]').value;
		var time = document.querySelector('[name=time]').value;
		var findHousesharesUri = housesharesApiUri + '/' + location.replace(' ', '+') + '/' + time;
		var housesharesReq = new XMLHttpRequest();
		housesharesReq.open('GET', findHousesharesUri);
		housesharesReq.onload = function (e) {
			if (this.status == 200) {
				removeHouseshares();
				document.querySelector('aside').appendChild(document.createElement('ul'));
				var houseshares = JSON.parse(this.response);
				for (var i = 0; i < houseshares.length; i++) {
					addHouseshare(houseshares[i]);
				}
				centreMap(location);
			}
			showLoadingIndicator(false);
			document.querySelector('form button').disabled = false;
		}
		housesharesReq.send();
	}

	function addHouseshare(houseshare) {
		houseshareItem = document.createElement('li');
		houseshareItem.id = houseshare.uri.replace('http', '').replace(/\W/g, '');
		houseshareItem.className = houseshare.seller_type.toLowerCase()
				+ ' ' + houseshare.property_type.toLowerCase()
				+ ' ' + houseshare.room_type.toLowerCase()
		houseshareItem.innerHTML += '<h2>' + houseshare.title + '</h2>';
		houseshareItem.innerHTML += '<p>£' + houseshare.price + ' pw</p>';
		houseshareItem.innerHTML += '<p>Available: ' + houseshare.date_available + '</p>';
		houseshareItem.innerHTML += '<p>Posted: ' + houseshare.date_posted + '</p>';
		houseshareItem.innerHTML += '<p><a href="' + houseshare.uri + '">See full advert ></a></p>';
		if (houseshare.location_coordinates) {
			var marker = addMarker(houseshare.location_coordinates[0], houseshare.location_coordinates[1], {id: houseshareItem.id});
		}
		else {
			houseshareItem.innerHTML += '<p>(not on map)</p>';
		}
		if (marker) {
			houseshareItem.addEventListener('click', function () { selectMarker(marker); });
		}
		document.querySelector('aside ul').appendChild(houseshareItem);
	}

	function removeHouseshares() {
		var housesharesList = document.querySelector('aside ul')		
		if (housesharesList) {
			housesharesList.parentNode.removeChild(housesharesList);
		}
		removeMarkers();
	}

	function addMarker(latitude, longitude, data) {
		var position = new google.maps.LatLng(latitude, longitude);
		var marker = new google.maps.Marker({position: position, map: map, icon: markerIcon});
		if (data) {
			for(var i in data) {
				marker[i] = data[i];
			}
		}
		mapMarkers.push(marker);
		google.maps.event.addListener(marker, 'click', function () { selectMarker(marker); });
		return marker;
	}

	function selectMarker(marker) {
		if (selectedMarker) {
			selectedMarker.setIcon(markerIcon);
			var oldAd = document.getElementById(selectedMarker.id);
			oldAd.classList.remove('selected');
		}
		selectedMarker = marker;
		marker.setIcon(markerIconSelected);
		var newAd = document.getElementById(marker.id);
		newAd.classList.add('selected');
		newAd.scrollIntoViewIfNeeded();
	}

	function removeMarkers() {
		for (var i = 0; i < mapMarkers.length; i++) {
			mapMarkers[i].setMap(null);
		}
		mapMarkers = [];
		selectedMarker = undefined;
	}

	function centreMap(location) {
		if (mapMarkers.length > 0) {
			var bounds = new google.maps.LatLngBounds();
			for (var i = 0; i < mapMarkers.length; i++) {
				bounds.extend(mapMarkers[i].position);
			}
			map.fitBounds(bounds);
		}
		else if (location) {
			var geocoder = new google.maps.Geocoder();
			geocoder.geocode({'address': location}, function (results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					var bounds = results[0].geometry.bounds;
					map.fitBounds(bounds);
				}
			});
		}
		else {
			var northEastUK = new google.maps.LatLng(59, 0);
			var southWestUK = new google.maps.LatLng(50, -10);
			var bounds = new google.maps.LatLngBounds(southWestUK, northEastUK);
			map.fitBounds(bounds);
		}
	}

	function showLoadingIndicator(show) {
		var indicator;
		if (!show) {
			indicator = document.body.querySelector('.loading');
			document.body.removeChild(indicator);
		}
		else {
			indicator = document.createElement('div');
			indicator.className = 'loading';
			indicator.innerHTML = '<p>Searching...</p>';
			document.body.appendChild(indicator);
		}
	}

	init();
}

document.addEventListener('DOMContentLoaded', new Houseshares());
