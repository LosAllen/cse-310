import arcade
import random
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Asteroids Clone"
BULLET_SPEED = 5
PLAYER_SPEED = 2
ROTATION_SPEED = 4
ASTEROID_SPEED = 1.5
ASTEROID_SIZES = [40, 30, 20]  # Large, Medium, Small
ASTEROID_POINTS = {40: 10, 30: 20, 20: 50}  # Score points per size
MAX_LIVES = 3

class Bullet:
    """ Bullet fired by the player """
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        self.radius = 3  # Small bullet size

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.RED)

class Asteroid:
    """ Asteroids that move across the screen """
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.dx = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)
        self.dy = random.uniform(-ASTEROID_SPEED, ASTEROID_SPEED)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        # Wrap around screen edges
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

    def draw(self):
        arcade.draw_circle_outline(self.x, self.y, self.size, arcade.color.WHITE, 2)

class Player:
    """ Player-controlled spaceship """
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.angle = 0
        self.speed = 0

    def update(self, keys_held):
        """ Update movement and rotation based on keys held """
        if keys_held["left"]:
            self.angle += ROTATION_SPEED
        if keys_held["right"]:
            self.angle -= ROTATION_SPEED
        if keys_held["up"]:
            self.speed = PLAYER_SPEED
        else:
            self.speed = 0  # Stop moving if not holding UP

        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        # Wrap around screen edges
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

    def draw(self):
        # Draw a simple triangle as the spaceship
        tip_x = self.x + math.cos(math.radians(self.angle)) * 15
        tip_y = self.y + math.sin(math.radians(self.angle)) * 15
        left_x = self.x + math.cos(math.radians(self.angle + 140)) * 10
        left_y = self.y + math.sin(math.radians(self.angle + 140)) * 10
        right_x = self.x + math.cos(math.radians(self.angle - 140)) * 10
        right_y = self.y + math.sin(math.radians(self.angle - 140)) * 10

        arcade.draw_triangle_filled(tip_x, tip_y, left_x, left_y, right_x, right_y, arcade.color.BLUE)

class AsteroidsGame(arcade.Window):
    """ Main game class """
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player = None
        self.bullets = []
        self.asteroids = []
        self.lives = MAX_LIVES
        self.score = 0
        self.keys_held = {"left": False, "right": False, "up": False}

        # Random asteroid spawn timer
        self.time_since_last_spawn = 0
        self.next_spawn_time = random.uniform(1, 5)

    def setup(self):
        self.player = Player()
        self.bullets = []
        self.asteroids = []

        # Spawn initial asteroids
        for _ in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            asteroid = Asteroid(x, y, 40)
            self.asteroids.append(asteroid)

    def on_draw(self):
        self.clear()
        self.player.draw()
        for bullet in self.bullets:
            bullet.draw()
        for asteroid in self.asteroids:
            asteroid.draw()

        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)
        arcade.draw_text(f"Lives: {self.lives}", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)

    def on_update(self, delta_time):
        """ Update the game state """
        self.player.update(self.keys_held)

        for bullet in self.bullets:
            bullet.update()
        for asteroid in self.asteroids:
            asteroid.update()

        # Check for bullet collisions with asteroids
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if (bullet.x - asteroid.x) ** 2 + (bullet.y - asteroid.y) ** 2 < (asteroid.size ** 2):
                    self.score += ASTEROID_POINTS[asteroid.size]
                    if asteroid.size > 20:  # If not the smallest, split it
                        for _ in range(2):
                            new_asteroid = Asteroid(asteroid.x, asteroid.y, asteroid.size - 10)
                            self.asteroids.append(new_asteroid)
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    break

        # Check for player collisions with asteroids
        for asteroid in self.asteroids:
            if (self.player.x - asteroid.x) ** 2 + (self.player.y - asteroid.y) ** 2 < (asteroid.size ** 2):
                self.lives -= 1
                self.reset_player()
                if self.lives <= 0:
                    arcade.close_window()

        # **Asteroid Spawning Logic**
        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= self.next_spawn_time:
            self.spawn_asteroid()
            self.time_since_last_spawn = 0
            self.next_spawn_time = random.uniform(1, 5)  # Reset to another random time

    def spawn_asteroid(self):
        """ Spawns a new asteroid at a random edge of the screen with a random trajectory """
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
        elif edge == "bottom":
            x, y = random.randint(0, SCREEN_WIDTH), 0
        elif edge == "left":
            x, y = 0, random.randint(0, SCREEN_HEIGHT)
        else:  # Right
            x, y = SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)

        new_asteroid = Asteroid(x, y, 40)
        self.asteroids.append(new_asteroid)
        
    def reset_player(self):
        """ Reset player position after losing a life """
        self.player.x = SCREEN_WIDTH // 2
        self.player.y = SCREEN_HEIGHT // 2
        self.player.speed = 0


    def on_key_press(self, key, modifiers):
        """ Handle key presses """
        if key == arcade.key.LEFT:
            self.keys_held["left"] = True
        elif key == arcade.key.RIGHT:
            self.keys_held["right"] = True
        elif key == arcade.key.UP:
            self.keys_held["up"] = True
        elif key == arcade.key.SPACE:
            bullet = Bullet(self.player.x, self.player.y, self.player.angle)
            self.bullets.append(bullet)
            
    def on_key_release(self, key, modifiers):
        """ Handle key releases """
        if key == arcade.key.LEFT:
            self.keys_held["left"] = False
        elif key == arcade.key.RIGHT:
            self.keys_held["right"] = False
        elif key == arcade.key.UP:
            self.keys_held["up"] = False

# Run the game
if __name__ == "__main__":
    game = AsteroidsGame()
    game.setup()
    arcade.run()
