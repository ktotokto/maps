import pygame

from tools.get_json import get_json_response
from const import RED, GREEN

pygame.init()
screen = pygame.display.set_mode((640, 480))


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.Font(None, 32)
        self.color = RED
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.return_text = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.return_text = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_coord(self):
        return get_json_response(self.return_text, "2cba1e40-eafb-42e1-8e61-539727bb58a2") \
            if self.return_text else None
