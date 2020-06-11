import geopy.distance

from django.test import TestCase
from geojson import Point
from . import osrm
from . import helper


class TestWinner(TestCase):

    OSRM_CONF = {}
    origin = Point((14.439855, 50.023226))
    destination = Point((14.489431312606478, 50.121765629793298))
    pointA = Point((14.406775, 50.05801))
    pointB = Point((14.431909, 50.060757))
    pointC = Point((14.538084, 50.078847))

    def setUp(self):
        self.OSRM_CONF['url'] = 'http://router.project-osrm.org/'
        self.OSRM_CONF['service'] = 'route'
        self.OSRM_CONF['profile'] = 'driving'
        self.OSRM_CONF['params'] = {
            'annotations': 'false',
            'overview': 'full',
            'geometries': 'geojson'
        }

    def test_OSRM_route_A_after_120(self):

        data = osrm.get_osrm_route(self.origin, self.pointA, self.destination)
        #Parse route durations
        location, index = helper.get_position_in_time(data['routes'], 120)
        # After 120s on route A I should be at the 43th node
        expected_node = 43
        expected_location = Point((14.421505, 50.025427))
        self.assertTrue(index == expected_node)
        self.assertTrue(location == expected_location)

    def test_OSRM_compare_routes_after_800(self):

        time = 800
        routeA = osrm.get_osrm_route(self.origin, self.pointA, self.destination)
        routeB = osrm.get_osrm_route(self.origin, self.pointB, self.destination)
        routeC = osrm.get_osrm_route(self.origin, self.pointC, self.destination)
        locationA, indexA = helper.get_position_in_time(routeA['routes'], time)
        locationB, indexB = helper.get_position_in_time(routeB['routes'], time)
        locationC, indexC = helper.get_position_in_time(routeC['routes'], time)
        #Calculate distance from the destination
        distanceA = geopy.distance.vincenty(locationA.coordinates, self.destination.coordinates).km
        distanceB = geopy.distance.vincenty(locationB.coordinates, self.destination.coordinates).km
        distanceC = geopy.distance.vincenty(locationC.coordinates, self.destination.coordinates).km

        distances = {
            'A': distanceA,
            'B': distanceB,
            'C': distanceC,
            }

        min_distance = 100000 # km
        winner = 'unknown'
        for key in distances:
            if distances[key] < min_distance:
                min_distance = distances[key]
                winner = key

        self.assertTrue(winner == 'C')
