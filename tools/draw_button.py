from pygame import draw
from const import RED, BLACK


def draw_button(screen, rect, font):
    draw.rect(screen, RED, rect)
    text = font.render("СБРОС", True, BLACK)
    return text, text.get_rect(center=rect.center)