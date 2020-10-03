import openrouteservice
import folium



def get_routes(coords):
<<<<<<< HEAD
    client = openrouteservice.Client(
        key='5b3ce3597851110001cf6248601cc4adb79846c89cab0a82974ac095')  # API KEY GOES HERE
=======
    client = openrouteservice.Client(key="")  # API KEY GOES HERE
>>>>>>> dc952c55e4714e8fc25f218c97f4684e9d1e7a79
    routes = client.directions(coords)

    return routes


def render_route(routes):
    m = folium.Map(location=[0, 0], tiles="cartodbpositron", zoom_start=13)
    folium.PolyLine(
        locations=[
            list(reversed(coord))
            for coord in routes["features"][0]["geometry"]["coordinates"]
        ]
    ).add_to(m)
