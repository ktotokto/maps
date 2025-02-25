import pygame
import sys
import requests
from io import BytesIO
from PIL import Image

W, H = SIZE = 1200, 600
BLACK = pygame.Color("#000000")


def pilImageToSurface(image):
    mode, size = image.mode, image.size
    data = image.tobytes("raw", mode)
    return pygame.image.fromstring(data, size, mode)


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


def get_map_response(coordinates, delta, apikey):
    toponym_longitude, toponym_latitude = coordinates.split(" ")
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_latitude]),
        "spn": ",".join([delta, delta]),
        "apikey": apikey,
    }
    map_api_server = "https://static-maps.yandex.ru/v1"
    return requests.get(map_api_server, params=map_params)


json_response = get_json_response("Сыктывкар", "2cba1e40-eafb-42e1-8e61-539727bb58a2")
coordinates = get_coordinates(json_response)
map_response = get_map_response(coordinates, "1", "0720951d-bde7-4048-8e6c-f22b5f5c3301")

pygame.init()
pygame.display.set_caption("Карта (не историческая)")
screen = pygame.display.set_mode(SIZE)
im = BytesIO(map_response.content)
opened_image = Image.open(im)
opened_image = opened_image.convert('RGB')
img = pilImageToSurface(opened_image)
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
    screen.fill(BLACK)
    screen.blit(img, img.get_rect(center=(W // 2, H // 2)))
    pygame.display.flip()
