import pygame, sys, os
from modules import gametext
from modules import board as b
from modules import player as p
from modules import database as db

class Interface:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((928,793))
        pygame.display.set_caption('Concentration')
        self.clock = pygame.time.Clock()
        # -------- Common variables 
        self.player = p.Player()
        self.menu_is_running = True
        self.game_is_running = False
        self.game_transition_is_running = False
        self.leaderboard_is_running = False
        self.credits_is_running = False
        self.gameover_is_running = False
        self.transition_counter = 0 # Level and Game Over
        # -------- Fonts objects
        self.text_title_font = pygame.font.Font("assets/font/Wars of Asgard Condensed.ttf", 70)
        self.text_minititle_font = pygame.font.Font("assets/font/Wars of Asgard Condensed.ttf", 45)
        self.text_button_font = pygame.font.Font("assets/font/Wars of Asgard Condensed.ttf", 40)
        self.text_transition_font = pygame.font.Font("assets/font/Wars of Asgard Condensed.ttf", 30)
        self.text_subtitle_font = pygame.font.Font("assets/font/Wars of Asgard Condensed.ttf", 25)
        # -------- Background variables
        self.bg_forest_slow = [pygame.image.load(f"assets/background/forestbackground/Layer{i}.png").convert_alpha() for i in range(0,4)]
        self.bg_forest_normal = [pygame.image.load(f"assets/background/forestbackground/Layer{i}.png").convert_alpha() for i in range(4, 8)]
        self.bg_forest_fast = [pygame.image.load(f"assets/background/forestbackground/Layer{i}.png").convert_alpha() for i in range(8, 12)]
        self.bg_forest_anim = [0, 0, 0]
        # -------- Menu variables
        self.menu_title = gametext.Text(self.text_title_font, "Concentration", (464, 100))
        self.menu_start_button = gametext.InteractiveText(self.text_button_font, "Start", (464, 350))
        self.menu_leaderboard_button = gametext.InteractiveText(self.text_button_font, "Leaderboard", (464, 450))
        self.menu_credits_button = gametext.InteractiveText(self.text_button_font, "Credits", (464, 550))
        self.menu_exit_button = gametext.InteractiveText(self.text_button_font, "Exit", (464, 650))
        self.menu_text_buttons = [self.menu_start_button, self.menu_leaderboard_button, self.menu_credits_button, self.menu_exit_button]
        # --------- Game variables
        self.level = 1 # Limit = 7
        self.game_bg_transition = pygame.image.load("assets/background/transitionbackground.png").convert_alpha()
        self.game_text_transition = gametext.Text(self.text_transition_font, f"Level {self.level}", (464, 397))
        self.game_hearts = [pygame.transform.scale(pygame.image.load(f"assets/heart/redheart_512px{i}.png").convert_alpha(), (50,50)) for i in range(1,3)]
        self.game_hearts_anim = 0
        # --------- Gameover variables
        self.gameover_title = gametext.Text(self.text_title_font, "GAME OVER", (464, 100))
        self.gameover_instructions = gametext.Text(self.text_button_font, "ENTER INITIALS", (464, 320))
        self.gameover_input = gametext.Text(self.text_button_font, self.player.initials, (464, 460))
        self.gameover_enter = gametext.InteractiveText(self.text_button_font, "ENTER", (464, 600))
        # --------- Credits variables
        self.credits_title = gametext.Text(self.text_title_font, "Credits", (464, 100))
        self.credits_back = gametext.InteractiveText(self.text_button_font, "Back", (464, 720))
        self.credits_assets = gametext.Text(self.text_minititle_font, "Game Graphics Assets", (464, 250))
        self.credits_dev = gametext.Text(self.text_minititle_font, "Game Developer", (464, 540))
        # --------- Leaderboard variables
        self.leaderboard_title = gametext.Text(self.text_title_font, "Leaderboard", (464, 100))
        self.leaderboard_back = gametext.InteractiveText(self.text_button_font, "Back", (464, 720))


    def start_game(self) -> None:
        """ Organizes the main control flow of the program """
        if self.menu_is_running:
            self.display_backgroundforest()
            self.display_menu()
        if self.game_is_running:
            if self.game_transition_is_running:
                self.display_game_transition()
            else:
                self.display_game()
        if self.gameover_is_running:
            if self.game_transition_is_running:
                self.display_game_transition()
            else:
                self.display_gameover()
        if self.leaderboard_is_running:
            self.display_leaderboard()
        if self.credits_is_running:
            self.display_credits()


    def display_backgroundforest(self) -> None:
        """ Displays the layers of the forest background at different paces """
        for bg in self.bg_forest_slow:
            self.screen.blit(bg, (self.bg_forest_anim[0], 0))
            self.screen.blit(bg, (self.bg_forest_anim[0] + 928, 0))
        for bg in self.bg_forest_normal:
            self.screen.blit(bg, (self.bg_forest_anim[1], 0))
            self.screen.blit(bg, (self.bg_forest_anim[1] + 928, 0))
        for bg in self.bg_forest_fast:
            self.screen.blit(bg, (self.bg_forest_anim[2], 0))
            self.screen.blit(bg, (self.bg_forest_anim[2] + 928, 0))
        self.bg_forest_anim[0] -= 0.5
        self.bg_forest_anim[1] -= 1
        self.bg_forest_anim[2] -= 1.5
        for i in range(3):
            if self.bg_forest_anim[i] <= -928:
                self.bg_forest_anim[i] = 0


    def display_hearts(self) -> None:
        """ Displays the hearts of the player in game """
        self.game_hearts_anim += 0.25
        if self.game_hearts_anim >= 2:
            self.game_hearts_anim = 0
        # Position of heart (x, 720)
        x_pos = 20 # position for heart
        for _ in range(self.player.lives):
            self.screen.blit(self.game_hearts[int(self.game_hearts_anim)], (x_pos, 720))
            x_pos += 60
            

    def display_menu(self) -> None:
        """ Displays the title of the game and the interactive text of the game menu """
        self.screen.blit(self.menu_title.surface, self.menu_title.rect) 
        for button in self.menu_text_buttons:
            self.screen.blit(button.surface, button.rect)
            if button.is_hovering(): 
                button.change_color((255, 255, 0))
            else: 
                button.change_color((255, 255, 255))
            if button.is_activated():
                self.menu_is_running = False
                if self.menu_start_button == button:
                    self.game_transition_is_running = True
                    self.game_is_running = True
                    self.player = p.Player()
                    return
                if self.menu_leaderboard_button == button:
                    self.leaderboard_is_running = True
                    return
                if self.menu_credits_button == button:
                    self.credits_is_running = True
                    return
                if self.menu_exit_button == button:
                    pygame.quit()
                    sys.exit()

    
    def display_leaderboard(self) -> None:
        """ Displays the top ten players of the game based on points from leaderboard.db """
        self.display_backgroundforest()
        title_text = self.leaderboard_title
        back_button = self.leaderboard_back
        self.screen.blit(title_text.surface, title_text.rect)
        self.screen.blit(back_button.surface, back_button.rect)
        if back_button.is_hovering():
            back_button.change_color((255, 255, 0))
        else:
            back_button.change_color((255, 255, 255))
        if back_button.is_activated():
            self.menu_is_running = True
            self.leaderboard_is_running = False
        if "leaderboard.db" not in os.listdir("data"):
                db.create_database()
        y_pos = 0
        for initials, score in db.query_database():
            player_text = gametext.Text(self.text_subtitle_font, f"{initials}\t\t{score}", (464, 230+y_pos))
            self.screen.blit(player_text.surface, player_text.rect)
            y_pos += 45


    def display_credits(self) -> None:
        """ Displays the credits of the game """
        self.display_backgroundforest()
        title = self.credits_title
        back_button = self.credits_back
        game_assets = self.credits_assets
        game_dev = self.credits_dev
        self.screen.blit(title.surface, title.rect)
        self.screen.blit(back_button.surface, back_button.rect)
        if back_button.is_hovering():
            back_button.change_color((255, 255, 0))
        else:
            back_button.change_color((255, 255, 255))
        if back_button.is_activated():
            self.menu_is_running = True
            self.credits_is_running = False
        self.screen.blit(game_assets.surface, game_assets.rect)
        y_pos = 0
        for name in ["TEMOK", "edermunizz", "gilgaphoenizignis"]:
            creator_text = gametext.Text(self.text_subtitle_font, name, (464, 340+y_pos))
            self.screen.blit(creator_text.surface, creator_text.rect)
            y_pos += 50
        self.screen.blit(game_dev.surface, game_dev.rect)
        dev_name = gametext.Text(self.text_subtitle_font, "Andrew Albert A. Yanza", (464, 630))
        self.screen.blit(dev_name.surface, dev_name.rect)


    def display_game_transition(self) -> None: 
        """ Displays a transition between each level of the game"""
        if self.transition_counter >= 70:
            self.game_transition_is_running = False
            self.transition_counter = 0
            self.board = b.Board(self.level)
            return
        self.transition_counter += 1
        if self.game_is_running:
            self.game_text_transition.change_text(f"Level {self.level}")
        else:
            self.game_text_transition.change_text("Game Over")
        self.screen.blit(self.game_bg_transition, (0, 0))
        self.screen.blit(self.game_text_transition.surface, self.game_text_transition.rect)


    def display_gameover(self) -> None:
        """ Displays the gameover message, and gathers input of the initials of the player """
        self.display_backgroundforest()
        self.screen.blit(self.gameover_title.surface, self.gameover_title.rect)
        self.screen.blit(self.gameover_enter.surface, self.gameover_enter.rect)
        self.screen.blit(self.gameover_input.surface, self.gameover_input.rect)
        self.screen.blit(self.gameover_instructions.surface, self.gameover_instructions.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player.initials = self.player.initials[:-1]
                elif len(self.player.initials) == 3:
                    # Limits initials to 3
                    pass
                else:
                    self.player.initials += event.unicode.upper()
                self.gameover_input = gametext.Text(self.text_title_font, self.player.initials, (464, 460))
        if self.gameover_enter.is_hovering(): 
            self.gameover_enter.change_color((255, 255, 0))
        else: 
            self.gameover_enter.change_color((255, 255, 255))
        if self.gameover_enter.is_activated() and len(self.player.initials) == 3:
            # Reset level
            self.level = 1
            # Return to menu
            self.menu_is_running = True
            self.gameover_is_running = False
            if "leaderboard.db" not in os.listdir("data"):
                db.create_database()
            # Inserts data to leaderboard.db
            db.insert_database(self.player.initials, self.player.points)
            

    def display_game(self) -> None:
        """ Displays the game """
        self.display_backgroundforest()
        self.display_hearts()
        for card in self.board.cards:
            self.screen.blit(card.surface, card.rectangle)
            if not card.active and not card.guessed and not card.transitioning:
                if card.clicked():
                    if not self.board.guessing:
                        self.board.guess = card
                        self.board.guessing = True
                    else:
                        self.board.guesser = card
                    card.transitioning = True

            if card.transitioning:
                transition_state = card.transition_state
                transition_to = card.transition_to
                if transition_to == "face":
                    card.transition(True)
                else:
                    card.transition(False)
                if transition_state > 3:
                    card.transitioning = False
                    card.transition_state = 3
                    card.transition_to = "back"
                    card.active = True
                if transition_state < 0:
                    card.transitioning = False
                    card.transition_state = 0
                    card.transition_to = "face"
                    card.active = False

            if card.active and self.board.guessing and self.board.is_guesser(card):
                guess_card = self.board.guess
                if self.board.is_correct_guess() and card != guess_card:
                    self.board.reset_guess()
                    self.board.correct_guess()
                    self.player.add_points()
                    card.guess = True
                    guess_card.guess = True
                    if self.board.is_cleared():
                        self.board.change_scene = True
                else:
                    self.board.reset_guess()
                    self.player.remove_life()
                    if self.player.is_dead():
                        self.board.change_scene = True
                        return
                    card.transitioning = True
                    card.transition_to = "back"
                    guess_card.transitioning = True
                    guess_card.transition_to = "back"
            
            if self.board.change_scene:
                self.board.increment_transition_count()
                transition_count = self.board.transition_count
                if self.player.is_dead():
                    if transition_count == 70:
                        self.board.reset_transition_count()
                        self.game_is_running = False
                        self.gameover_is_running = True
                        self.game_transition_is_running = True
                        return
                if self.board.is_cleared():
                    if transition_count == 70:
                        self.board.reset_transition_count()
                        self.game_transition_is_running = True
                        self.level += 1
                        return
