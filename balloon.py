import pygame # version 23.0.1
import random
import os

pygame.init()

# configure game window
WIN_WIDTH, WIN_HEIGHT = 900, 500
FPS = 60
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
bullets_fired_font = pygame.font.SysFont('calibri', 40)
bullets_missed_font = pygame.font.SysFont('calibri', 60)
pygame.display.set_caption("Balloon shooting challenge")

# other definitions
SPEED = 2
BULLET_SPEED = SPEED * 10
BALLOON_WIDTH, BALLOON_HEIGHT = 50, 50  
CANNON_WIDTH, CANNON_HEIGHT = 90, 50
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALLOON_HIT = pygame.USEREVENT + 1

# load assets and relative file path
root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__)))
balloon_img = pygame.transform.scale(pygame.image.load(os.path.join(root_dir, 'Assets', 'balloon.png')), (BALLOON_WIDTH, BALLOON_HEIGHT))
cannon_img = pygame.transform.scale(pygame.image.load(os.path.join(root_dir, 'Assets', 'cannon.png')), (CANNON_WIDTH, CANNON_HEIGHT))
hit_sound = pygame.mixer.Sound(os.path.join(root_dir, 'Assets', 'Grenade.mp3'))
fire_sound = pygame.mixer.Sound(os.path.join(root_dir, 'Assets', 'Silencer.mp3'))

# function to render graphics
def draw_window(cannon, balloon, bullets, bullets_fired):   
    
    # static rendering
    window.fill(WHITE)
    window.blit(cannon_img, (cannon.x, cannon.y))
    window.blit(balloon_img, (balloon.x, balloon.y))
    bullets_fired_text = bullets_fired_font.render("Bullets fired: " + str(bullets_fired), 1, BLACK)
    window.blit(bullets_fired_text, (WIN_WIDTH//2 - bullets_fired_text.get_width()//2, 10))

    # dynamic rendering
    for bullet in bullets:
        pygame.draw.rect(window, BLACK, bullet)

    pygame.display.update()

# function to control cannon/player movement
def cannon_movement(key_pressed, cannon):
    if key_pressed[pygame.K_UP] and cannon.y - SPEED > 0:
        cannon.y -= SPEED
    if key_pressed[pygame.K_DOWN] and cannon.y + SPEED + cannon.height < WIN_HEIGHT:
        cannon.y += SPEED

# function to control bullet motion
def bullet_movement(balloon, bullets, missed_shots):
    for bullet in bullets:
        bullet.x -= BULLET_SPEED
        if balloon.colliderect(bullet): # collision setting
            pygame.event.post(pygame.event.Event(BALLOON_HIT))
            bullets.remove(bullet)
        elif bullet.x < 0: # redundant bullets
            bullets.remove(bullet)
            missed_shots.append(bullet)

# function to control balloon motion
def balloon_movement(balloon, balloon_direction):
    if balloon.y - BALLOON_HEIGHT < 0 or balloon.y + BALLOON_HEIGHT > WIN_HEIGHT:
        balloon_direction *= -1
    balloon.y += balloon_direction

# function to play during end of game
def end_game(missed_shots):
    end_text = bullets_missed_font.render("Missed shots: " + str(missed_shots), 1, BLACK)
    window.blit(end_text, (WIN_WIDTH//2 - end_text.get_width()//2, WIN_HEIGHT//2 - end_text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(3*1000)
    pygame.quit()

# main loop
def main():

    balloon = pygame.Rect(100, WIN_HEIGHT//2, BALLOON_WIDTH, BALLOON_HEIGHT)
    cannon = pygame.Rect(WIN_WIDTH - 100, WIN_HEIGHT-100, CANNON_WIDTH, CANNON_HEIGHT)
    bullets = []
    missed_shots = []
    bullets_fired, dir_counter = 0, 0

    clock = pygame.time.Clock()

    run = True
    while run:

        # determine balloon's new direction
        if dir_counter % 20 == 0: 
            balloon_direction = random.randint(-SPEED, SPEED)

        clock.tick(FPS) # limit frames for accuracy

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(cannon.x, cannon.y + CANNON_HEIGHT//2 - 8, BULLET_WIDTH, BULLET_HEIGHT) # bullet to cannon's centre
                    bullets.append(bullet)
                    fire_sound.play()
                    bullets_fired += 1
            
            if event.type == BALLOON_HIT:
                hit_sound.play()
                run = False
                end_game(len(missed_shots))

        key_pressed = pygame.key.get_pressed()
        cannon_movement(key_pressed, cannon)
        balloon_movement(balloon, balloon_direction)
        bullet_movement(balloon, bullets, missed_shots)
        draw_window(cannon, balloon, bullets, bullets_fired)

        dir_counter += 1

if __name__ == "__main__":
    main()