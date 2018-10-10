import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange' 
    else:
        return 'red'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Mapbox Bright")

# Marker allows you to put marker into map with popup description
map.add_child(folium.Marker(location=[38.58, -99.09], popup="I am Marker", icon=folium.Icon(color='green')))

# other way how to add Markers
# helps with organisation and with adding functionality 
fgv = folium.FeatureGroup(name="Vulcanoes")
fgp = folium.FeatureGroup(name='Population')

# zip fuction is needed when iterating through multiple lists at same time
for lt, ln, el, name in zip(lat, lon, elev, name):
# iframe creates box 200 x 100 and uses name, name and el to html hypertext
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=10, popup=folium.Popup(iframe), fill=True, color=color_producer(el)))
# lambda sets color if population is over 1 000 000 population is value of POP2005 key of properties key
fgp.add_child(folium.GeoJson(data=(open('world.json', 'r', encoding='utf-8-sig').read()), style_function=lambda x: {'fillColor':'green' 
if x['properties']['POP2005'] < 1000000 else 'orange' if 1000000 <= x['properties']['POP2005'] < 10000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
#swith layers off or on
map.add_child(folium.LayerControl())
map.save("Map1.html")