import geopy.distance

from geojson import Point


class Waypoint:
    name: str
    coord: Point

    def __init__(self, name: str, coord: Point) -> None:
        self.name = name
        self.coord = coord


def get_position_in_time(routes, time):
    legs = routes[0]['legs']
    durations = []
    for leg in legs:
        durations += leg['annotation']['duration']
    index = 0
    elapsed = 0
    for d in durations:
        elapsed += d
        index += 1
        if elapsed >= time:
            print("Index of the node after " + str(time) + " s: " + str(index) + ' elapsed: ' + str(elapsed))
            break
    location = Point(routes[0]['geometry']['coordinates'][index])
    return location, index


def get_time_from_points(routes, start_index, dest_index):
    legs = routes[0]['legs']
    durations = []
    for leg in legs:
        durations += leg['annotation']['duration']
    elapsed = 0
    for i in range(start_index, dest_index):
        elapsed += durations[i]

    return elapsed


def find_winner_distance_node(name, routes, target_distance, destination):
    nodes = routes[0]['geometry']['coordinates']
    index = 0
    for node in nodes:
        index += 1
        lon = node[0]
        lat = node[1]
        lon_d = destination.coordinates[0]
        lat_d = destination.coordinates[1]
        distance_from_dest = geopy.distance.vincenty([lat, lon], [lat_d, lon_d]).km
        if distance_from_dest <= target_distance:
            break
    print("Winner " + name + " distance node: " + str(routes[0]['geometry']['coordinates'][index]) + " distance: " + str(distance_from_dest))
    return index


def find_delay(name, routes, target_distance, destination, start_index):
    node_winner_distance_index = find_winner_distance_node(name, routes, target_distance, destination)
    delay = get_time_from_points(routes, start_index, node_winner_distance_index)
    return delay
