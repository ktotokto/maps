import pygame
from io import BytesIO
from PIL import Image

from tools.get_json import get_map_response
from tools.pil_image import pil_image_to_surface


class MapParams:
    def __init__(self, coordinates, z_index, apikey, coefficient):
        self.coordinates, self.z_index, self.apikey = coordinates.split(), z_index, apikey
        self.coefficient, self.theme = coefficient, "light"
        self.key_list = [pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        self.get_map()

    def key_event(self, key):
        if key in self.key_list:
            if key == self.key_list[0]:
                new_z_index = (int(self.z_index) - 1)
                if new_z_index >= 1:
                    self.coefficient, self.z_index = self.coefficient * 2, str(new_z_index)
            elif key == self.key_list[1]:
                new_z_index = (int(self.z_index) + 1)
                if new_z_index <= 21:
                    self.coefficient, self.z_index = self.coefficient / 2, str(new_z_index)
            elif key == self.key_list[2]:
                self.coordinates[1] = str(float(self.coordinates[1]) + self.coefficient)
            elif key == self.key_list[3]:
                self.coordinates[1] = str(float(self.coordinates[1]) - self.coefficient)
            elif key == self.key_list[4]:
                self.coordinates[0] = str(float(self.coordinates[0]) - self.coefficient * 2)
            elif key == self.key_list[5]:
                self.coordinates[0] = str(float(self.coordinates[0]) + self.coefficient * 2)
            coord_0, coord_1 = float(self.coordinates[0]), float(self.coordinates[1])
            self.coordinates[0] = str(-(coord_0 / abs(coord_0)) * (360.0 - abs(coord_0))) if abs(coord_0) > 180.0 else \
                self.coordinates[0]
            self.coordinates[1] = str((coord_1 / abs(coord_1)) * 85.0) if abs(coord_1) > 85.0 else self.coordinates[1]
            self.get_map()
            print(self.z_index, self.coefficient)

    def get_map(self):
        map_response = get_map_response(self.coordinates, self.z_index, self.apikey, self.theme)
        im = BytesIO(map_response.content)
        opened_image = Image.open(im)
        opened_image = opened_image.convert('RGB')
        self.map = pil_image_to_surface(opened_image)
