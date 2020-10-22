import googlemaps
from googlemaps.maps import StaticMapPath


class Navigation:

    def __init__(self):
        self.client = googlemaps.Client(
            key='AIzaSyD0Isa9kbHBJ_Q2txdAsLsycNzKnUoXafA')

    def get_directions(self, source, destination):
        directions_result = self.client.directions(source, destination)

        return directions_result

    def render_route(self, origin, destination):
        # m = folium.Map(location=[0, 0], tiles="cartodbpositron", zoom_start=13)
        # folium.PolyLine(
        #     locations=[
        #         list(reversed(coord))
        #         for coord in routes["features"][0]["geometry"]["coordinates"]
        #     ]
        # ).add_to(m)

        path = StaticMapPath(points=[origin, destination])

        response = self.client.static_map(
            maptype="hybrid",
            format="png",
            scale=2,
            path=path
        )

        with open("./assets/maps/test.png", "wb") as fp:
            for chunks in response:
                fp.write(chunks)

        # with open("./takeout/test.png", 'w') as f:
        #     response.save(f)

        # with open('./takeout/test.png', 'wb') as f:
        #     f.write(response)

        return response
