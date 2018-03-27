var map = L.map('map').setView([39.7318566,-75.4168745], 6);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZHVkYXJldiIsImEiOiJCeUx0Y0kwIn0.Yjsz4P3dQn3fMxCDQRH2rg', {
    maxZoom: 10,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
		'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="http://mapbox.com">Mapbox</a>',
    id: 'mapbox.light'
}).addTo(map);

// control that shows state info on hover
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info');
    this.update();
    return this._div;
};

info.update = function (props) {
    this._div.innerHTML = '<h4>Total spending per capita</h4>' +  (props ?
		'<b>' + props.name + '</b><br />' + props.spending_per_capita
		: 'Hover over a location<br/>&nbsp;');
};

info.addTo(map);

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

		var div = L.DomUtil.create('div', 'info legend'),
				grades = [20000, 15000, 10000, 5000, 0],
				labels = [];

		// loop through our density intervals and generate a label with a colored square for each interval
		for (var i = 1; i < grades.length; i++) {
				div.innerHTML +=
						'<i style="background:' + getColor(grades[i]) + '"></i> ' +
						'$' + grades[i] + ' - $' + grades[i-1] + '  <br/>';
		}

		return div;
};

legend.addTo(map);

var geojsonLayer = new L.GeoJSON.AJAX("/locations.geojson", {style: style, onEachFeature: onEachFeature});       
geojsonLayer.addTo(map);

function getColor(value) {
    return value >= 15000 ? '#a63603' :
           value >= 10000 ? '#e6550d' :
           value >= 5000 ? '#fd8d3c' :
           value >= 0    ? '#fdbe85' :
                           '#feedde';
    }

    function style(feature) {
		    return {
				    fillColor: getColor(feature.properties.spending_per_capita),
				    weight: 2,
				    opacity: 1,
				    color: 'white',
				    fillOpacity: 0.7
		    };
    }

    function onEachFeature(feature, layer) {
layer.on({
  'mouseover': highlightFeature,
  'mouseout': resetHighlight,
  'click': function() {
				    window.location.href = '/l/' + feature.properties.slug;
		    }
});
    }

function highlightFeature(e) {
var layer = e.target;
info.update(layer.feature.properties);
}

function resetHighlight(e) {
  info.update();
}
