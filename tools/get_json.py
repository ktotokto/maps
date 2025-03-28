import requests


def get_json_response(toponym_to_find, apikey):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": apikey,
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    return response.json()


def get_coordinates(json_response):
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym["Point"]["pos"]


def get_map_response(coordinates, z_index, apikey, theme="dark", pt_list=()):
    toponym_longitude, toponym_latitude = coordinates
    pt_list = ["".join(f"{",".join(pt.split())},{pt_list[-1]}".split()) for pt in pt_list[:-1]]
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_latitude]),
        "z": z_index,
        "apikey": apikey,
        "theme": theme,
        "pt": "~".join(pt_list)
    }
    map_api_server = "https://static-maps.yandex.ru/v1"
    return requests.get(map_api_server, params=map_params)
