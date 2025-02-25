import pygame
import sys
import requests
from io import BytesIO
from PIL import Image

W, H = SIZE = 1200, 600
BLACK = pygame.Color("#000000")


class MapParams:
    def __init__(self, coordinates, z_index, apikey):
        self.coordinates, self.z_index, self.apikey = coordinates.split(), z_index, apikey
        self.get_map()

    def key_event(self, key):
        if key == pygame.K_PAGEUP:
            new_z_index = (int(self.z_index) - 1)
            self.z_index = str(new_z_index) if new_z_index >= 1 else "1"
        elif key == pygame.K_PAGEDOWN:
            new_z_index = (int(self.z_index) + 1)
            self.z_index = str(new_z_index) if new_z_index <= 21 else "21"
        elif key == pygame.K_UP:
            pass
            # self.coordinates[1] = str(float(self.coordinates[1]) + 10 / (int(self.z_index) * 2))
        elif key == pygame.K_DOWN:
            pass
            # self.coordinates[1] = str(float(self.coordinates[1]) - 10 / (int(self.z_index) * 2))
        elif key == pygame.K_LEFT:
            pass
        elif key == pygame.K_RIGHT:
            pass

    def get_map(self):
        map_response = get_map_response(self.coordinates, self.z_index, self.apikey)
        im = BytesIO(map_response.content)
        opened_image = Image.open(im)
        opened_image = opened_image.convert('RGB')
        self.map = pil_image_to_surface(opened_image)


def pil_image_to_surface(image):
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


def get_map_response(coordinates, z_index, apikey):
    toponym_longitude, toponym_latitude = coordinates
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_latitude]),
        "z": z_index,
        "apikey": apikey,
    }
    map_api_server = "https://static-maps.yandex.ru/v1"
    return requests.get(map_api_server, params=map_params)


json_response = get_json_response("Сыктывкар", "2cba1e40-eafb-42e1-8e61-539727bb58a2")
map_params = MapParams(get_coordinates(json_response), "12", "0720951d-bde7-4048-8e6c-f22b5f5c3301")

pygame.init()
pygame.display.set_caption("Карта (не историческая)")
screen = pygame.display.set_mode(SIZE)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            map_params.key_event(event.key)
    screen.fill(BLACK)
    img = map_params.get_map()
    screen.blit(img, img.get_rect(center=(W // 2, H // 2)))
    pygame.display.flip()
