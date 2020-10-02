import openrouteservice

def get_routes(coords):
    client = openrouteservice.Client(key='') #API KEY GOES HERE
    routes = client.directions(coords)
    return routes
