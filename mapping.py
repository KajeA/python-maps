import folium
import pandas

#### Starting position ####

map = folium.Map(location=[41.12, -103.38], zoom_start=5.5, tiles="Stamen Terrain")



#### Data for volcanoes ####

data = pandas.read_csv("volcanos.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])


#### Popup styles for volcanoes ####

html = """<h4>Volcano information:</h4>
Name: %s
<br>
Height: %d m
"""

#### Colours for markers ####

def color_marker(elevation):
    if elevation < 1500.0:
      return 'lightgreen'
    elif elevation >= 1500.0 and elevation < 2000.0:
        return 'darkgreen'
    elif elevation >= 2000.0 and elevation < 2500.0:  #learned different p3 syntax but can't mix con + var + con
        return 'orange'
    else:
        return 'red'
    
#### CREATE THE VOLCANO MAP ####

fgv = folium.FeatureGroup(name="Volcanos")

for lt, ln, el, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (str(nm), el), width=200, height=100)
    fgv.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=color_marker(el),icon="fa-area-chart", prefix='fa')))
    

    
#### ADD COUNTRY LINES AND SHADING BASED ON POPULATION ####

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r').read(), 
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'yellow' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'blue' if 20000000 <= x['properties']['POP2005'] < 50000000 else 'red'}))





#### GENERATE MAP ####

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map_html_popup_simple.html")
