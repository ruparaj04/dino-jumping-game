import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
FPS = 60
GRAVITY = 1
JUMP_FORCE = 18
OBSTACLE_SPEED = 5
OBSTACLE_FREQUENCY = 1500  # milliseconds
ACCELERATION = 0.0005  # Game acceleration over time

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)
GREY = (200, 200, 200)
BLUE = (135, 206, 250)
DARK_BLUE = (25, 25, 112)
BROWN = (139, 69, 19)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Jump Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for text
font = pygame.font.SysFont('Arial', 24)
large_font = pygame.font.SysFont('Arial', 40)

# Create directory for saving high score if it doesn't exist
save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save")
os.makedirs(save_dir, exist_ok=True)
score_file = os.path.join(save_dir, "highscore.txt")

def load_high_score():
    if os.path.exists(score_file):
        try:
            with open(score_file, 'r') as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_high_score(score):
    with open(score_file, 'w') as f:
        f.write(str(score))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(0, 300)
        self.y = random.randint(30, 150)
        self.width = random.randint(60, 120)
        self.height = 40
        self.speed = random.uniform(0.5, 1.5)
    
    def update(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(0, 100)
            self.y = random.randint(30, 150)
    
    def draw(self, surface):
        # Draw a fluffy cloud with multiple circles
        cloud_color = (245, 245, 245)
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        radius = self.height // 2
        # Draw main cloud body
        pygame.draw.circle(surface, cloud_color, (center_x, center_y), radius)
        pygame.draw.circle(surface, cloud_color, (center_x - radius, center_y), radius * 0.8)
        pygame.draw.circle(surface, cloud_color, (center_x + radius, center_y), radius * 0.8)
        pygame.draw.circle(surface, cloud_color, (center_x - radius // 2, center_y - radius // 2), radius * 0.7)
        pygame.draw.circle(surface, cloud_color, (center_x + radius // 2, center_y - radius // 2), radius * 0.7)

class Dinosaur:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = 100
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.is_jumping = False
        self.jump_velocity = 0
        self.color = GREEN
        self.ducking = False
        self.run_frame = 0
        self.frame_count = 0
        self.run_animation_speed = 5

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = -JUMP_FORCE
            self.ducking = False

    def duck(self):
        if not self.is_jumping:
            self.ducking = True
            # Make the dinosaur shorter when ducking
            self.height = 40
        
    def stand(self):
        self.ducking = False
        self.height = 80

    def update(self):
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += GRAVITY
            
            # Check if landed
            if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
                self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
                self.is_jumping = False
                self.jump_velocity = 0
        
        # Update running animation
        self.frame_count += 1
        if self.frame_count >= self.run_animation_speed:
            self.run_frame = (self.run_frame + 1) % 2
            self.frame_count = 0

    def draw(self, surface):
        # Base position
        body_x = self.x
        body_y = self.y
        
        if self.ducking:
            # Draw ducking dinosaur (lower and longer)
            body_width = 70
            body_height = 40
            
            # Draw the dinosaur body
            pygame.draw.rect(surface, self.color, (body_x, body_y, body_width, body_height))
            
            # Draw the dinosaur head
            head_size = 25
            pygame.draw.rect(surface, self.color, (body_x + body_width - 10, body_y - head_size + 20, head_size, head_size))
            
            # Draw the eye
            pygame.draw.circle(surface, BLACK, (body_x + body_width + 5, body_y - head_size + 30), 4)
            
            # Draw the legs for running animation
            leg_width = 10
            leg_height = 15
            
            # Running animation
            if self.run_frame == 0:
                pygame.draw.rect(surface, self.color, (body_x + 10, body_y + body_height, leg_width, leg_height))
                pygame.draw.rect(surface, self.color, (body_x + 40, body_y + body_height, leg_width, leg_height))
            else:
                pygame.draw.rect(surface, self.color, (body_x + 25, body_y + body_height, leg_width, leg_height))
                pygame.draw.rect(surface, self.color, (body_x + 55, body_y + body_height, leg_width, leg_height))
        else:
            # Draw standing dinosaur
            body_width = 50
            body_height = 80
            
            # Draw the dinosaur body
            pygame.draw.rect(surface, self.color, (body_x, body_y, body_width, body_height))
            
            # Draw the dinosaur head
            head_size = 30
            pygame.draw.rect(surface, self.color, (body_x + body_width - 10, body_y - head_size + 10, head_size, head_size))
            
            # Draw the eye
            pygame.draw.circle(surface, BLACK, (body_x + body_width + 10, body_y - head_size + 20), 5)
            
            # Draw the arm
            arm_width = 20
            arm_height = 8
            pygame.draw.rect(surface, self.color, (body_x + 15, body_y + 30, arm_width, arm_height))
            
            # Draw the legs for running animation
            leg_width = 12
            leg_height = 25
            
            # Running animation
            if self.run_frame == 0:
                pygame.draw.rect(surface, self.color, (body_x + 10, body_y + body_height, leg_width, leg_height))
                pygame.draw.rect(surface, self.color, (body_x + 30, body_y + body_height, leg_width, leg_height))
            else:
                pygame.draw.rect(surface, self.color, (body_x, body_y + body_height, leg_width, leg_height))
                pygame.draw.rect(surface, self.color, (body_x + 40, body_y + body_height, leg_width, leg_height))

    def get_rect(self):
        # Return rectangle for collision detection
        return pygame.Rect(self.x, self.y, 
                          70 if self.ducking else 50,  # Width is larger when ducking
                          self.height)

class Obstacle:
    def __init__(self, speed, obstacle_type=None):
        self.speed = speed
        
        # Randomly choose obstacle type if not specified
        if obstacle_type is None:
            obstacle_type = random.choice(["cactus", "rock", "bird"])
        
        self.obstacle_type = obstacle_type
        
        if obstacle_type == "cactus":
            self.width = 25
            self.height = random.randint(50, 80)
            self.x = SCREEN_WIDTH
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.color = (20, 140, 20)  # Green for cactus
        elif obstacle_type == "rock":
            self.width = 40
            self.height = random.randint(30, 50)
            self.x = SCREEN_WIDTH
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.color = (150, 150, 150)  # Grey for rock
        elif obstacle_type == "bird":
            self.width = 50
            self.height = 30
            self.x = SCREEN_WIDTH
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(40, 120)  # Birds fly at different heights
            self.color = (200, 100, 50)  # Color for bird
            self.wing_frame = 0
            self.frame_count = 0

    def update(self):
        self.x -= self.speed
        
        # Update bird wing animation
        if self.obstacle_type == "bird":
            self.frame_count += 1
            if self.frame_count >= 10:  # Change wing position every 10 frames
                self.wing_frame = (self.wing_frame + 1) % 2
                self.frame_count = 0

    def draw(self, surface):
        if self.obstacle_type == "cactus":
            # Draw main cactus body
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            
            # Draw cactus arms
            arm_width = 15
            arm_height = 10
            
            # Left arm
            arm_y = self.y + self.height // 3
            pygame.draw.rect(surface, self.color, (self.x - arm_width + 5, arm_y, arm_width, arm_height))
            
            # Right arm
            arm_y = self.y + self.height // 2
            pygame.draw.rect(surface, self.color, (self.x + self.width - 5, arm_y, arm_width, arm_height))
            
        elif self.obstacle_type == "rock":
            # Draw rock as a polygon
            rock_points = [
                (self.x, self.y + self.height),
                (self.x, self.y + self.height // 2),
                (self.x + self.width // 3, self.y),
                (self.x + 2 * self.width // 3, self.y + self.height // 3),
                (self.x + self.width, self.y + 2 * self.height // 3),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(surface, self.color, rock_points)
            
        elif self.obstacle_type == "bird":
            # Draw bird body
            pygame.draw.ellipse(surface, self.color, (self.x, self.y, self.width, self.height))
            
            # Draw bird head
            head_size = 15
            pygame.draw.circle(surface, self.color, (self.x + self.width - 5, self.y + self.height // 2 - 5), head_size // 2)
            
            # Draw beak
            beak_points = [
                (self.x + self.width + 5, self.y + self.height // 2 - 5),
                (self.x + self.width + 15, self.y + self.height // 2),
                (self.x + self.width + 5, self.y + self.height // 2 + 5)
            ]
            pygame.draw.polygon(surface, (255, 200, 0), beak_points)
            
            # Draw wings with animation
            if self.wing_frame == 0:
                # Wings up
                wing_points = [
                    (self.x + 10, self.y + 5),
                    (self.x + self.width // 2, self.y - 15),
                    (self.x + self.width - 10, self.y + 5)
                ]
            else:
                # Wings down
                wing_points = [
                    (self.x + 10, self.y + self.height - 5),
                    (self.x + self.width // 2, self.y + self.height + 15),
                    (self.x + self.width - 10, self.y + self.height - 5)
                ]
            pygame.draw.polygon(surface, self.color, wing_points)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.x < -self.width

class Game:
    def __init__(self):
        self.dinosaur = Dinosaur()
        self.obstacles = []
        self.clouds = [Cloud() for _ in range(3)]
        self.score = 0
        self.high_score = load_high_score()
        self.game_over = False
        self.pause = False
        self.obstacle_timer = 0
        self.last_obstacle_time = 0
        self.current_speed = OBSTACLE_SPEED
        self.day_cycle = 0  # 0-100, 0=day, 100=night
        self.day_cycle_direction = 1  # 1=getting darker, -1=getting lighter
        self.day_cycle_speed = 0.05
        self.ground_pattern = [random.randint(0, 1) for _ in range(100)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()  # Reset the game
                    elif not self.pause:
                        self.dinosaur.jump()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.dinosaur.duck()
                if event.key == pygame.K_ESCAPE:
                    if not self.game_over:
                        self.pause = not self.pause
                    else:
                        pygame.quit()
                        sys.exit()
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.dinosaur.ducking:
                    self.dinosaur.stand()

    def update(self):
        if not self.game_over and not self.pause:
            # Update dinosaur
            self.dinosaur.update()
            
            # Increase score
            self.score += 1
            
            # Gradually increase speed
            self.current_speed += ACCELERATION
            
            # Update day/night cycle
            self.day_cycle += self.day_cycle_direction * self.day_cycle_speed
            if self.day_cycle >= 100:
                self.day_cycle = 100
                self.day_cycle_direction = -1
            elif self.day_cycle <= 0:
                self.day_cycle = 0
                self.day_cycle_direction = 1
            
            # Update clouds
            for cloud in self.clouds:
                cloud.update()
            
            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
            
            # Check for collisions
            for obstacle in self.obstacles:
                if self.dinosaur.get_rect().colliderect(obstacle.get_rect()):
                    self.game_over = True
                    if self.score // 10 > self.high_score:
                        self.high_score = self.score // 10
                        save_high_score(self.high_score)
            
            # Add new obstacles
            current_time = pygame.time.get_ticks()
            # Gradually decrease obstacle frequency as speed increases
            current_frequency = max(OBSTACLE_FREQUENCY - (self.current_speed - OBSTACLE_SPEED) * 50, 800)
            if current_time - self.last_obstacle_time > current_frequency:
                # Every once in a while, add a specific type of obstacle
                if random.random() < 0.2:  # 20% chance for a bird
                    self.obstacles.append(Obstacle(self.current_speed, "bird"))
                else:  # 80% chance for cactus or rock
                    obstacle_type = random.choice(["cactus", "rock"])
                    self.obstacles.append(Obstacle(self.current_speed, obstacle_type))
                
                self.last_obstacle_time = current_time

    def draw_ground(self, surface):
        # Draw main ground
        ground_color = GREY
        pygame.draw.rect(surface, ground_color, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        
        # Draw ground details
        detail_color = BROWN
        for i in range(100):
            if self.ground_pattern[i] == 1:
                x_pos = (i * 20 - (int(self.score / 5) % 20)) % (SCREEN_WIDTH + 20) - 10
                pygame.draw.rect(surface, detail_color, (x_pos, SCREEN_HEIGHT - GROUND_HEIGHT + 10, 3, 3))
        
        # Draw ground line
        pygame.draw.line(surface, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT), 
                         (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT), 2)

    def draw(self):
        # Calculate sky color based on day/night cycle
        day_r, day_g, day_b = 135, 206, 250  # Light blue for day
        night_r, night_g, night_b = 25, 25, 112  # Dark blue for night
        
        # Interpolate between day and night colors
        cycle_ratio = self.day_cycle / 100.0
        sky_r = int(day_r * (1 - cycle_ratio) + night_r * cycle_ratio)
        sky_g = int(day_g * (1 - cycle_ratio) + night_g * cycle_ratio)
        sky_b = int(day_b * (1 - cycle_ratio) + night_b * cycle_ratio)
        
        sky_color = (sky_r, sky_g, sky_b)
        
        # Clear screen with sky color
        screen.fill(sky_color)
        
        # Draw moon/sun based on cycle
        if self.day_cycle < 50:  # Day time
            # Draw sun
            sun_radius = 40
            sun_x = 100
            sun_y = 80
            pygame.draw.circle(screen, (255, 255, 0), (sun_x, sun_y), sun_radius)
        else:  # Night time
            # Draw moon
            moon_radius = 30
            moon_x = 100
            moon_y = 80
            pygame.draw.circle(screen, (220, 220, 220), (moon_x, moon_y), moon_radius)
            
            # Draw some stars at night
            for i in range(20):
                star_x = (i * 37 + int(self.score / 10)) % SCREEN_WIDTH
                star_y = (i * 23 % 150) + 10
                star_size = random.randint(1, 3)
                brightness = 150 + int(100 * (self.day_cycle - 50) / 50)  # Brighter as night gets darker
                pygame.draw.circle(screen, (brightness, brightness, brightness), (star_x, star_y), star_size)
        
        # Draw clouds
        for cloud in self.clouds:
            cloud.draw(screen)
        
        # Draw ground
        self.draw_ground(screen)
        
        # Draw dinosaur
        self.dinosaur.draw(screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {self.score // 10}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        # Draw high score
        high_score_text = font.render(f"High Score: {self.high_score}", True, BLACK)
        screen.blit(high_score_text, (SCREEN_WIDTH - 200, 20))
        
        # Draw game over message
        if self.game_over:
            game_over_text = large_font.render("Game Over!", True, BLACK)
            restart_text = font.render("Press SPACE to restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
        
        # Draw pause message
        elif self.pause:
            pause_text = large_font.render("PAUSED", True, BLACK)
            continue_text = font.render("Press ESC to continue", True, BLACK)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
            screen.blit(continue_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))

    def run(self):
        # Main game loop
        while True:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()