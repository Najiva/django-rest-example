import geopy.distance

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from geojson import Point
from .helper import Waypoint
from . import osrm
from . import helper


class WinnerView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        return Response("Hello world")

    def post(self, request, format=None):

        # Validation
        # TODO
        # Check that the request has correct structure and data

        # Create native objects/deserialization
        origin = Point((request.data['origin']['lon'], request.data['origin']['lat']))
        dest = Point((request.data['destination']['lon'], request.data['destination']['lat']))
        time = request.data['time']
        waypoints = []
        routes = []
        for waypoint in request.data['waypoints']:
            p = Point((waypoint['lon'], waypoint['lat']))
            name = waypoint['name']
            waypoints.append(Waypoint(name, p))

        # Get routes from OSRM
        for waypoint in waypoints:
            route = osrm.get_osrm_route(origin, waypoint.coord, dest)
            routes.append({
                'name': waypoint.name,
                'data': route
            })

        # Get winner
        min_distance = 100000 # km
        winner = 'unknown'
        for route in routes:
            position, index = helper.get_position_in_time(route['data']['routes'], time)
            route['position'] = position  # Coordinates where I am at the time T
            route['index'] = index  # Index of the node where I am at the time T
            # I need to switch coordinates
            lon = position.coordinates[0]
            lat = position.coordinates[1]
            lon_d = dest.coordinates[0]
            lat_d = dest.coordinates[1]
            distance_from_dest = geopy.distance.vincenty([lat, lon], [lat_d, lon_d]).km
            route['distance'] = distance_from_dest  # How far am I from detination at time T
            if distance_from_dest < min_distance:
                winner = route['name']
                min_distance = distance_from_dest

        response = {
            'winnerName': winner,
            'delays': {
            }
        }

        # Get delays
        for route in routes:
            if route['name'] == winner:
                response['delays'][route['name']] = 0
            else:
                response['delays'][route['name']] = helper.find_delay(
                    route['name'],
                    route['data']['routes'],
                    min_distance,
                    dest,
                    route['index'])
        resp = Response(response)

        return resp
