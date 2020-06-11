import json
import requests

from django.conf import settings


def get_osrm_route(origin, point, destination, params=settings.OSRM_CONF['default_params']):
    o = str(origin.coordinates[0]) + ',' + str(origin.coordinates[1]) + ';'
    d = str(destination.coordinates[0]) + ',' + str(destination.coordinates[1])
    w = str(point.coordinates[0]) + ',' + str(point.coordinates[1]) + ';'

    url = settings.OSRM_CONF['url'] + '/' \
        + settings.OSRM_CONF['service'] + '/v1/' \
        + settings.OSRM_CONF['profile'] + '/' \
        + o + w + d + '?'
    first = True
    for key in params:
        if first:
            first = False
            url += key + '=' + params[key]
        else:
            url += '&' + key + '=' + params[key]
    try:
        r = requests.get(url)
        if r:
            data = json.loads(r.text)
            return data
        else:
            print('Could not retrive route from OSRM server.')
            return {}
    except Exception as ex:
            print(f'Error occurred while communicating to OSRM service: {ex}')
            return {}
