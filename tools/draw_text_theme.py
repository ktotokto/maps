from pygame import draw
from const import DARK_THEME, WHITE, BLACK, LIGHT_THEME


def draw_text_theme(screen, theme, rect, font):
    if theme == "dark":
        draw.rect(screen, DARK_THEME, rect)
        text = font.render("ТЁМНАЯ ТЕМА", True, WHITE)
        return text, text.get_rect(center=rect.center)
    else:
        draw.rect(screen, LIGHT_THEME, rect)
        text = font.render("СВЕТЛАЯ ТЕМА", True, BLACK)
        return text, text.get_rect(center=rect.center)
