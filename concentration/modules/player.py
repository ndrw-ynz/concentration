class Player:

    def __init__(self):
        self.lives = 5
        self.points = 0
        self.initials = ""

    def is_dead(self):
        return self.lives == 0

    def remove_life(self):
        self.lives -= 1

    def add_points(self):
        self.points += 50
