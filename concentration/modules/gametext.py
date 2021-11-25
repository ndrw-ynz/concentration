import pygame

class Text:
    def __init__(self, font = object, text = str, coordinates=tuple):
        self.font = font
        self.text = text
        self.coordinates = coordinates

        self.surface = font.render(self.text, True, (255, 255, 255))
        self.rect = self.surface.get_rect(center=coordinates)

    def change_text(self, text = str):
        self.text = text
        self.surface = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.surface.get_rect(center=self.coordinates)


class InteractiveText(Text):
    def __init__(self, font = object, text = str, coordinates=tuple):
        super().__init__(font, text, coordinates)

    def change_color(self, RGB = tuple):
        self.surface = self.font.render(self.text, True, RGB)
        self.rect = self.surface.get_rect(center = self.coordinates)

    def is_hovering(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def is_activated(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
    