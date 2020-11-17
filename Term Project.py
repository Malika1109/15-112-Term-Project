import pygame
import sys
import random

#Project code which creates the Flappy Bird Game and allows the user to play the game with 3 lives.
#After the 3 lives are over, a Game Over screen is diaplayed.

#Function which takes 2 images of the floor base and joins them together
def create_floor():
    screen.blit(floor_surface,(floor_position,900))
    screen.blit(floor_surface,(floor_position + 576,900))
    
#function to create and return 2 randomly generated pipes
def generate_pipe():
    
    pipe_position = random.choice(pipe_height) 
    
    bottom_pipe = pipe_surface.get_rect(midtop = (700,pipe_position))
    
    top_pipe = pipe_surface.get_rect(midbottom = (700,pipe_position - 500)) 
    
    return bottom_pipe,top_pipe
    
#Function to draw the created pipes. This function will draw a vertically and horizontally flipped image of the top pipe
def draw_pipes(pipes):
    
    for pipe in pipes:
        
        if pipe.bottom >= 1024:
            
            screen.blit(pipe_surface, pipe)
            
        else:
            
            #Syntax for transform.flip() obtained from https://www.pygame.org/docs/ref/transform.html
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            
            screen.blit(flip_pipe, pipe)

#function to move the pipes backwards on the screen    
def move_pipes(pipes):
    
    for pipe in pipes:
        
        pipe.centerx -= 5
        
    return pipes


            
#Function which checks collisions and returns the state of the game            
def pipe_collision(pipes):
    
    for pipe in pipes:
        
        if bird_rect.colliderect(pipe):
            
            return False
            
    if bird_rect.top<= -90 or bird_rect.bottom >= 1000:
        
        return False
        
    return True
            
            
def rotate_bird(bird):
    
    #Syntax and working of transform.rotozoom() obtained from https://www.pygame.org/docs/ref/transform.html
    rotated_bird = pygame.transform.rotozoom(bird,-bird_pos*3,1)
    return rotated_bird
    
#Function to continuosly return new bird rectangles from a list of bird images to rotate the wings of the bird
def bird_animate():
    
    new_bird = bird_frames[bird_index]
    
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    
    return new_bird, new_bird_rect


#Function which diaplays the user's score on the screen
def score_display():
    
    score_surface = game_font.render(str(int(score)),True,(255,255,255))
    
    score_rect = score_surface.get_rect(center = (288,100))
    
    screen.blit(score_surface,score_rect)


pygame.init()

screen = pygame.display.set_mode((576,1024))

clock = pygame.time.Clock()

game_font = pygame.font.Font(pygame.font.get_default_font(),40)  

gravity = 0.25

bird_pos = 0

game_state = True

score = 0


#Picture obtained from github at https://github.com/ian13456/flapp5/blob/master/assets/sprites/background-day.png 
bg_surface = pygame.image.load('background-day.png').convert() 

bg_surface = pygame.transform.scale2x(bg_surface)

#Floor Base picture obtained from github at https://github.com/ian13456/flapp5/blob/master/assets/sprites/base.png
floor_surface = pygame.image.load('base.png').convert()

floor_surface = pygame.transform.scale2x(floor_surface)

floor_position = 0

#Bird down flap image obtained at https://github.com/ian13456/flapp5/blob/master/assets/sprites/bluebird-downflap.png
bird_downflap = pygame.transform.scale2x(pygame.image.load('bluebird-downflap.png').convert_alpha())

#Bird mid flap image obtained at https://github.com/ian13456/flapp5/blob/master/assets/sprites/bluebird-midflap.png
bird_midflap = pygame.transform.scale2x(pygame.image.load('bluebird-midflap.png').convert_alpha())

#Bird up flap image obtained at https://github.com/ian13456/flapp5/blob/master/assets/sprites/bluebird-upflap.png
bird_upflap = pygame.transform.scale2x(pygame.image.load('bluebird-upflap.png').convert_alpha())

bird_frames = [bird_downflap,bird_midflap,bird_upflap]

bird_index = 0

bird_surface = bird_frames[bird_index]

bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,1000)



bird_surface = pygame.image.load('bluebird-midflap.png').convert_alpha()

bird_surface = pygame.transform.scale2x(bird_surface)

bird_rect = bird_surface.get_rect(center = (100,512))

pipe_surface = pygame.image.load('pipe-green.png').convert()

pipe_surface = pygame.transform.scale2x(pipe_surface)


pipe_list = []

GETPIPE = pygame.USEREVENT
pygame.time.set_timer(GETPIPE,1000)

pipe_height = [400,600,800] 

#Game over image obtained at https://github.com/ian13456/flapp5/blob/master/assets/sprites/message.png
game_over_surface = pygame.image.load('message.png').convert_alpha()

game_over_surface = pygame.transform.scale2x(game_over_surface)

game_over_rect = game_over_surface.get_rect(center = (288,512))

lives = 3


while True:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            pygame.quit()
            
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state:
                bird_pos = 0
                bird_pos -= 8
                
                
            
            if event.key == pygame.K_SPACE and game_state == False:
                
                game_state = True
                
                pipe_list.clear()
                
                bird_rect.center = (100, 512) 
                
                bird_pos = 0
                
                score = 0
                
                lives -= 1
                
                
        if event.type == GETPIPE:
            pipe_list.extend(generate_pipe())
            
            
        if event.type == BIRDFLAP:
            
            if bird_index<2:
                
                bird_index += 1
            
            else:
                
                bird_index = 0
                
            bird_surface, bird_rect = bird_animate()
            
            
            
    screen.blit(bg_surface,(0,0))
    
    if game_state:
    
        #Bird
        bird_pos += gravity
        
        
        rotated_bird = rotate_bird(bird_surface)
        
        bird_rect.centery += bird_pos
        
        screen.blit(rotated_bird,bird_rect)
        
        game_state = pipe_collision(pipe_list)
        
        pipe_list = move_pipes(pipe_list)
        
        draw_pipes(pipe_list)
        
        score += 0.02
        
        score_display()
        
    else:
        if lives == 1:
            screen.blit(game_over_surface, game_over_rect)  
     
    
    
    #Floor
    #To move the floor backwards continuously
    floor_position -= 1
    
    create_floor()
    
    if floor_position <= -576:
        
        floor_position = 0
    
    
    
    
            
    pygame.display.update()
    clock.tick(120)
    
    