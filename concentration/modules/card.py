import json, os, pygame

with open(os.path.join(os.path.dirname(__file__), "config.json")) as file:
    config = json.load(file)

class Card:
    """
    Attributes: 
        id (int) - Represents the unique id that the card has
        content (obj) - Represents the character that the card contains
        img (obj) - Represents the image name of the image in the assets folder
        anim_state (int) - Represents the animation state of the card
    """
    def __init__(self, card_key):
        json_card = config[card_key]
        self.content = json_card["content"]
        self.transition_state = json_card["transition_state"]
        img_name = json_card["img_name"]
        self.card_animations = {
            0:pygame.image.load(f"assets/card/animations/card1.png").convert_alpha(),
            1:pygame.image.load(f"assets/card/animations/card2.png").convert_alpha(),
            2:pygame.image.load(f"assets/card/animations/card3.png").convert_alpha(),
            3:pygame.image.load(f"assets/card/face/{img_name}").convert_alpha()
        }
        self.surface = None
        self.rectangle = None
        self.size = None
        self.position = None
        self.surface = None
        self.rectangle = None
        self.active = False
        self.guessed = False
        self.transitioning = False
        self.transition_to = "face"

    def clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rectangle.collidepoint(pygame.mouse.get_pos())

    def default_state(self):
        self.surface = pygame.transform.scale(self.card_animations[0], self.size)
        self.rectangle = self.surface.get_rect(topleft=self.position)

    def transition(self, transition_to_face = bool):
        increment = 1.2
        phase = 3
        if not transition_to_face:
            increment *= -1
            phase = 0
        self.transition_state += increment
        self.surface = pygame.transform.scale(self.card_animations.get(int(self.transition_state), self.card_animations[phase]), self.size)
        self.rectangle = self.surface.get_rect(topleft=self.position)
