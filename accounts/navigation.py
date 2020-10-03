import openrouteservice


def get_routes(coords):
    client = openrouteservice.Client(
        key='5b3ce3597851110001cf6248601cc4adb79846c89cab0a82974ac095')  # API KEY GOES HERE
    routes = client.directions(coords)

    return routes
