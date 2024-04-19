import pygame
import random

class Spooky:
    def __init__(self):
        pygame.init()

        self.height = 480
        self.width = 640
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Spooky")
        self.game_font = pygame.font.SysFont("Arial", 24)

        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False

        self.new_game()

        self.clock = pygame.time.Clock()
        self.main_loop()

    def new_game(self):
        self.robot = Item(self.width, self.height, "robot", self.game_font.get_height())
        
        self.result = ""
        self.score = 0
        self.coins = []
        for i in range(5):
            i = Item(self.width, self.height, "coin", self.game_font.get_height())
            self.coins.append(i)

        self.create_ghoul()

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

    def check_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                   self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_UP:
                    self.to_up = True
                if event.key == pygame.K_DOWN:
                    self.to_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_UP:
                    self.to_up = False
                if event.key == pygame.K_DOWN:
                    self.to_down = False

            if event.type == pygame.QUIT:
                exit()

    def move(self):
        if self.game_solved() or self.game_over():
            return

        if self.to_right and self.robot.x < self.width-self.robot.get_width():
            self.robot.x += 3
        if self.to_left and self.robot.x > 0:
            self.robot.x -= 3
        if self.to_up and self.robot.y > 0:
            self.robot.y -= 3
        if self.to_down and self.robot.y < self.height-self.robot.get_height()-self.game_font.get_height():
            self.robot.y += 3   

    def check_contact(self):
        def check(item1, item2):
            item1_middle_x = item1.x+item1.get_width()/2
            item1_middle_y = item1.y+item1.get_height()/2
            item2_middle_x = item2.x+item2.get_width()/2
            item2_middle_y = item2.y+item2.get_height()/2
            if abs(item1_middle_y-item2_middle_y) < (item1.get_height()+item2.get_height())/2:
                if abs(item1_middle_x-item2_middle_x) < (item1.get_width()+item2.get_width())/2:
                    return True
            return False

        if check(self.robot, self.ghoul):
            self.result = "fail"
            self.game_over()

        for coin in self.coins:
            if check(self.robot, coin):
                self.coins.remove(coin)
                self.score += 1
                if self.score == 5:
                    self.result = "success"
                    self.game_solved()

    def create_ghoul(self):
        self.ghoul = Item(self.width, self.height, "monster", self.game_font.get_height())

    def it_follows(self, speed):
        if self.game_solved() or self.game_over():
            return

        target_x = self.robot.x
        target_y = self.robot.y

        if self.ghoul.x > target_x:
            self.ghoul.x -= speed
        if self.ghoul.x < target_x:
            self.ghoul.x += speed
        if self.ghoul.y > target_y:
            self.ghoul.y -= speed
        if self.ghoul.y < target_y:
            self.ghoul.y += speed

    def game_solved(self):
        self.result_text = "Victory!"
        if self.result == "success":
            return True
        return False
    
    def game_over(self):
        self.result_text = "Game over!"
        if self.result == "fail":
            return True
        return False
        
    def draw_window(self):
        self.window.fill((48,48,48))

        game_text = self.game_font.render("Score: " + str(self.score), True, (255, 0, 0))
        self.window.blit(game_text, (25, self.height - game_text.get_height()))
        game_text = self.game_font.render("F2 = new game", True, (255, 0, 0))
        self.window.blit(game_text, (200, self.height - game_text.get_height()))
        game_text = self.game_font.render("Esc = exit game", True, (255, 0, 0))
        self.window.blit(game_text, (400, self.height - game_text.get_height()))

        for coin in self.coins:
            self.window.blit(coin.item, (coin.x, coin.y))

        self.move()
        self.window.blit(self.robot.item, (self.robot.x, self.robot.y))

        if self.score > 0:
            if self.score < 3:
                self.it_follows(1)
            else:
                self.it_follows(2)
            self.window.blit(self.ghoul.item, (self.ghoul.x, self.ghoul.y))
        
        self.check_contact()

        if self.game_over() or self.game_solved():
            game_text = self.game_font.render(self.result_text, True, (255, 0, 255))
            game_text_x = self.width / 2 - game_text.get_width() / 2
            game_text_y = self.height / 2 - game_text.get_height() / 2
            pygame.draw.rect(self.window, (12, 12, 12), (game_text_x-game_text.get_width()/2, game_text_y-game_text.get_height()/2, game_text.get_width()*2, game_text.get_height()*2))
            self.window.blit(game_text, (game_text_x, game_text_y))

        pygame.display.flip()
        self.clock.tick(60)

# Item class for robot, ghoul and coins
class Item:
    def __init__(self, x, y, kind, font_height):
        self.item = pygame.image.load(kind + ".png")

        if kind == "robot":
            self.x = x/2-self.item.get_width()
            self.y = y-self.item.get_height()-font_height
        elif kind == "coin":
            # A better random location selection process could be implemented.
            # With these settings, sometimes it creates coins that are too close (even on top of each other)
            self.x = random.randint(50,x-50)
            self.y = random.randint(0,y-200)
        elif kind == "monster":
            self.x = random.choice([0, x-self.item.get_width()])
            self.y = random.choice([0, y-self.item.get_height()-font_height])

    def get_width(self):
        return self.item.get_width()

    def get_height(self):
        return self.item.get_height()

if __name__ == "__main__":
    Spooky()