import openrouteservice
import folium

def get_routes(coords):
    client = openrouteservice.Client(key='') #API KEY GOES HERE
    routes = client.directions(coords)
    return routes

def render_route(routes)
    m = folium.Map(location=[0,0], tiles='cartodbpositron', zoom_start=13):
    folium.PolyLine(locations=[list(reversed(coord))
                               for coord in
                               route['features'][0]['geometry']['coordinates']]).add_to(m)
