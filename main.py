import pygame
import sys
from classes.input_box import InputBox
from classes.map import MapParams
from const import BLACK, SIZE, W, H, RED
from tools.create_pt import create_pt
from tools.draw_text_theme import draw_text_theme
from tools.get_json import get_json_response, get_coordinates

json_response = get_json_response("Сыктывкар", "2cba1e40-eafb-42e1-8e61-539727bb58a2")
map_params = MapParams(get_coordinates(json_response), "1", "0720951d-bde7-4048-8e6c-f22b5f5c3301", 40)

pygame.init()
pygame.display.set_caption("Карта (не историческая)")
font = pygame.font.SysFont(None, 32)
switch_rect = pygame.Rect(W - 300, H - 80, 300, 80)
switch_state = False
input_box = InputBox(0, H - 48, 200, 48)
screen = pygame.display.set_mode(SIZE)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input_box.handle_event(event)
                coord = input_box.get_coord()
                if coord and coord["response"]["GeoObjectCollection"]["featureMember"]:
                    map_params.coordinates = get_coordinates(coord).split()
                    coordinates_pt = create_pt((get_coordinates(coord)), "pm2rdm")
                    map_params.z_index, map_params.coefficient = 7, 0.625
                    map_params.get_map(coordinates_pt)
            map_params.key_event(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            switch_state = not switch_state if switch_rect.collidepoint(pygame.mouse.get_pos()) else switch_state
            map_params.theme = "dark" if switch_state else "light"
        input_box.handle_event(event)
    input_box.update()
    screen.fill(BLACK)
    input_box.draw(screen)
    img = map_params.map
    screen.blit(img, img.get_rect(center=(W // 2, H // 2)))
    screen.blit(*draw_text_theme(screen, map_params.theme, switch_rect, font))
    pygame.display.flip()
