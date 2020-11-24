import pygame
import sys
import random

pygame.init()
home_screen = pygame.display.set_mode((576,1024))
surface_1 = pygame.image.load('background-day copy.png').convert() 
surface_1 = pygame.transform.scale2x(surface_1)
surface_2 = pygame.image.load('underwayer copy.png').convert()
surface_3 = pygame.image.load('space copy.png').convert()

while True:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            pygame.quit()
            
            sys.exit()

    #start_button = pygame.draw.rect(home_screen,(255,255,255),(0,0,200,200))
    
    home_screen.blit(surface_1,(0,0),(0,0,576,1024//3))
    
    home_screen.blit(surface_2,(0,1024//3),(0,0,576,1024//3))
    
    home_screen.blit(surface_3,(0,2*(1024//3)),(0,0,576,1024//3))
    
    normal_button = pygame.draw.rect(home_screen,(255,255,255),(190,150,200,50))    
    
    underwater_button = pygame.draw.rect(home_screen,(255,255,255),(190,500,200,50))   
    
    space_button = pygame.draw.rect(home_screen,(255,255,255),(190,700,200,50))        
    
    game_font = pygame.font.Font(pygame.font.get_default_font(),30)        
    
    normal_surface = game_font.render("Classic",True,(0,0,0))                            
    
    normal_rect = normal_surface.get_rect(center = (300,170))
    
    home_screen.blit(normal_surface,normal_rect)
    
    underwater_surface = game_font.render("Underwater",True,(0,0,0))                             
    
    underwater_rect = underwater_surface.get_rect(center = (300,520))
    
    home_screen.blit(underwater_surface,underwater_rect)
        
    space_surface = game_font.render("Space",True,(0,0,0))                            
    
    space_rect = space_surface.get_rect(center = (300,720))
    
    home_screen.blit(space_surface,space_rect)
    
    while True:
    
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                
                pygame.quit()
            
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= 190 and pygame.mouse.get_pos()[1] >= 150:
                    if pygame.mouse.get_pos()[0] <= 390 and pygame.mouse.get_pos()[1] <= 200:
                        
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
                                                
                
                if pygame.mouse.get_pos()[0] >= 190 and pygame.mouse.get_pos()[1] >= 500:
                    if pygame.mouse.get_pos()[0] <= 390 and pygame.mouse.get_pos()[1] <= 550:
                            def create_floor():
                                screen.blit(floor_surface,(floor_position,900))
                                screen.blit(floor_surface,(floor_position + 576,900))

                            def create_jelly():
                                random_jelly_pos = random.choice(jelly_height) 
                                
                                bottom_jelly = jelly_surface.get_rect(midtop = (512,random.randint(0,150)))
                                
                                top_jelly = jelly_surface.get_rect(midbottom = (512,random.randint(700,1000)))
                                
                                return bottom_jelly,top_jelly

                            def move_jelly(jellies):
                                
                                for jelly in jellies:
                                   
                                    jelly.centerx += random.randint(0,9)
                                    
                                    jelly.centerx -= 8
                                    
                                return jellies

                            def draw_jellies(jellies):
                                
                                for jelly in jellies:
                                        
                                    screen.blit(jelly_surface, jelly)
                                        

                            def check_collision(jellies):
                                
                                for jelly in jellies:
                                    bird = bird_rect.inflate(-40,-40)
                                    if bird.colliderect(jelly):
                                        return False
                                        
                                if bird_rect.top<= -100 or bird_rect.bottom >= 900:
                                    return False
                                
                                if bird_rect.left<=0:
                                    return False
                                
                                    
                                return True

                            def rotate_bird(bird):
                                
                                new_bird = pygame.transform.rotozoom(bird,-bird_pos*3,1)
                                return new_bird
                                
                            def bird_animation():
                                
                                new_bird = bird_frames[bird_index]
                                
                                new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
                                
                                return new_bird, new_bird_rect


                            def score_display():
                                
                                score_surface = game_font.render(str(int(score)),True,(255,255,255))
                                
                                score_rect = score_surface.get_rect(center = (288,100))
                                
                                screen.blit(score_surface,score_rect)
                                
                                
                            pygame.init()

                            screen = pygame.display.set_mode((576,1024))

                            clock = pygame.time.Clock()

                            game_font = pygame.font.Font(pygame.font.get_default_font(),40)

                            bg_surface = pygame.image.load('underwater2.jpg').convert()

                            floor_surface = pygame.image.load('base.png').convert()

                            floor_surface = pygame.transform.scale2x(floor_surface)

                            floor_position = 0


                            bird_downflap = pygame.transform.scale2x(pygame.image.load('bluebird-downflap.png').convert_alpha())

                            bird_midflap = pygame.transform.scale2x(pygame.image.load('bluebird-midflap.png').convert_alpha())

                            bird_upflap = pygame.transform.scale2x(pygame.image.load('bluebird-upflap.png').convert_alpha())

                            bird_frames = [bird_downflap,bird_midflap,bird_upflap]

                            bird_index = 0

                            bird_surface = bird_frames[bird_index]

                            bird_rect = bird_surface.get_rect(center = (100,512))

                            BIRDFLAP = pygame.USEREVENT + 1
                            pygame.time.set_timer(BIRDFLAP,1200)

                            bird_surface = pygame.image.load('bluebird-midflap.png').convert_alpha()

                            bird_surface = pygame.transform.scale2x(bird_surface)

                            bird_rect = bird_surface.get_rect(center = (100,512))

                            jelly_surface = pygame.image.load('jellyfish.png').convert_alpha()


                            jelly_list = []

                            SPAWNJELLY = pygame.USEREVENT

                            pygame.time.set_timer(SPAWNJELLY,2000)

                            jelly_height = [100,80,90] 

                            bird_pos = 0

                            game_state = True

                            viscosity = 2

                            gravity = 0.25

                            score = 0

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
                                                
                                                print("ydg")
                                                game_state = True 
                                                
                                                jelly_list.clear()
                                                
                                                bird_rect.center = (100, 512) 
                                                
                                                bird_pos = 0
                                                
                                                score = 0
                                                
                                        if event.key == pygame.K_RIGHT and game_state:
                                            
                                            bird_rect.centerx += 50
                                            
                                        if event.key == pygame.K_UP and game_state:
                                            
                                            bird_rect.centery -= 70
                                            
                                        if event.key == pygame.K_DOWN and game_state:
                                            
                                            bird_rect.centery += 70  
                                            
                                    if event.type == SPAWNJELLY:
                                        jelly_list.extend(create_jelly())
                                        
                                        
                                    if event.type == BIRDFLAP:
                                        
                                        if bird_index<2:
                                            
                                            bird_index += 1
                                        
                                        else:
                                            
                                            bird_index = 0
                                            
                                        bird_surface, bird_rect = bird_animation()
                                        
                                screen.blit(bg_surface,(0,0))
                                        
                                if game_state:

                                    #Bird
                                    #bird_pos += gravity
                                    bird_rect.centerx -= viscosity      
                                    
                                    rotated_bird = rotate_bird(bird_surface)
                                    
                                    bird_rect.centery += bird_pos
                                    
                                    screen.blit(rotated_bird,bird_rect)
                                    
                                    game_state = check_collision(jelly_list)
                                    
                                    jelly_list = move_jelly(jelly_list)
                                    
                                    draw_jellies(jelly_list)
                                    
                                    score += 0.01
                                    
                                    score_display()
                                            
                                            
                                floor_position -= 1
                                
                                create_floor()
                                
                                if floor_position <= -576:
                                    
                                    floor_position = 0
                                           
                                
                                
                                #screen.blit(bird_surface,bird_rect)
                                
                                #screen.blit(jelly_surface,jelly_rect)
                                pygame.display.update()
                                clock.tick(120)
#                             
                if pygame.mouse.get_pos()[0] >= 190 and pygame.mouse.get_pos()[1] >= 700:
                    if pygame.mouse.get_pos()[0] <= 390 and pygame.mouse.get_pos()[1] <= 750:
                            print ("hcwqv")
                            def create_floor():
                                screen.blit(floor_surface,(floor_position,900))
                                screen.blit(floor_surface,(floor_position + 576,900))


                            def create_asteroid():
                                random_asteroid_pos = random.choice(asteroid_height) 
                                
                                #bottom_asteroid = asteroid_surface.get_rect(midtop = (512,random.randint(0,150)))
                                bottom_asteroid = asteroid_surface.get_rect(midtop = (512,random_asteroid_pos))
                                
                                top_asteroid = asteroid_surface.get_rect(midbottom = (512,random.randint(700,1000)))
                                #top_jelly = jelly_surface.get_rect(midbottom = (700,random_jelly_pos - 600))
                                
                                return bottom_asteroid,top_asteroid
                            
                            def create_debris():
                                
                                top_debris = debris_surface.get_rect(midtop = (512,random.randint(0,100)))
                                bottom_debris = debris_surface.get_rect(midtop = (512,random.randint(900,1000)))
                                return top_debris,bottom_debris

                            def move_asteroid(asteroids):
                                count = 0
                                for asteroid in asteroids:
                                    
                                    #jelly.centerx -= 3
                                    #count = random.randint(0,5)
                                    
                                    if count%2 == 0 or count%2 == 1:
                                        
                                        asteroid.centery += random.randint(0,7)
                                        
                                    count += 1
                                    
                                    asteroid.centerx -= 3
                                    
                                return asteroids
                            
                            def move_debris(debris_list):
                                
                                for debris in debris_list:
                                    debris.centerx -= 3
                                    
                                return debris_list


                            def draw_asteroids(asteroids):
                                
                                for asteroid in asteroids:
                                    
                                    #if jelly.bottom >= 1024:
                                        
                                    screen.blit(asteroid_surface, asteroid)
                                    
                            def draw_debris(debris_list):
                                for debris in debris_list:
                                    
                                    screen.blit(debris_surface,debris)
                                    

                            def check_collision(asteroids):
                                
                                for asteroid in asteroids:
                                    #jelly = jelly.inflate(-20,-20)
                                    bird = bird_rect.inflate(-70,-70)
                                    if bird.colliderect(asteroid):
                                        screen.blit(blast_surface,blast_rect)
                                        #jelly_rect.inflate(10,15)
                                        print("Yay")
                                        return False
                                        
                                if bird_rect.top<= -100 or bird_rect.bottom >= 900:
                                    print("feqwfq")
                                    return False
                                
                                #if bird_rect.left<=0:
                                    #return False
                                
                                return True
                            
                            def check_debris(debris_list):
                                
                                for debris in debris_list:
                                    bird = bird_rect.inflate(-70,-70)
                                    if bird.colliderect(debris):
                                        #bird_rect.centery += 40
                                        bird_rect.center = (288, 512)
                                        

                            def rotate_bird(bird):
                                
                                new_bird = pygame.transform.rotozoom(bird,-bird_pos*3,1)
                                return new_bird
                                
                            def bird_animation():
                                
                                new_bird = bird_frames[bird_index]
                                
                                new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
                                
                                return new_bird, new_bird_rect


                            def score_display():
                                
                                score_surface = game_font.render(str(int(score)),True,(255,255,255))
                                
                                score_rect = score_surface.get_rect(center = (288,100))
                                
                                screen.blit(score_surface,score_rect)
                           
                            
                            pygame.init()
                            
                            screen = pygame.display.set_mode((576,1024))

                            clock = pygame.time.Clock()

                            game_font = pygame.font.Font(pygame.font.get_default_font(),40)

                            bg_surface = pygame.image.load('space.png').convert()

                            floor_surface = pygame.image.load('base.png').convert()

                            floor_surface = pygame.transform.scale2x(floor_surface)

                            floor_position = 0

                            bird_downflap = pygame.transform.scale2x(pygame.image.load('bluebird-downflap.png').convert_alpha())

                            bird_midflap = pygame.transform.scale2x(pygame.image.load('bluebird-midflap.png').convert_alpha())

                            bird_upflap = pygame.transform.scale2x(pygame.image.load('bluebird-upflap.png').convert_alpha())

                            bird_frames = [bird_downflap,bird_midflap,bird_upflap]

                            bird_index = 0

                            bird_surface = bird_frames[bird_index]

                            bird_rect = bird_surface.get_rect(center = (100,512))

                            BIRDFLAP = pygame.USEREVENT + 1
                            pygame.time.set_timer(BIRDFLAP,1200)

                            ast_normal = pygame.transform.scale2x(pygame.image.load('asteroid.png').convert_alpha())

                            blast_surface = pygame.transform.scale2x(pygame.image.load('blast.png').convert_alpha())

                            blast_rect = blast_surface.get_rect(center = (288,512))

                            bird_surface = pygame.image.load('bluebird-midflap.png').convert_alpha()

                            bird_surface = pygame.transform.scale2x(bird_surface)

                            bird_rect = bird_surface.get_rect(center = (100,512))

                            asteroid_surface = pygame.image.load('asteroid.png').convert_alpha()

                            SPAWNASTEROID = pygame.USEREVENT

                            pygame.time.set_timer(SPAWNASTEROID,3000)

                            asteroid_height = [100,50,25]
                            
                            asteroid_list = []

                            debris_surface = pygame.image.load('debris.png').convert_alpha()
                            
                            SPAWNDEBRIS = pygame.USEREVENT+2
                            
                            pygame.time.set_timer(SPAWNDEBRIS, 2500)
                            
                            debris_list = []
                            
                            bird_pos = 0

                            game_state = True

                            viscosity = 2

                            gravity = 0.25

                            score = 0

                            while True:
                                

                                for event in pygame.event.get():
                                    
                                    if event.type == pygame.QUIT:
                                        
                                        pygame.quit()
                                        
                                        sys.exit()
                                        
                                    if event.type == pygame.KEYDOWN:    
                                        
                                        if event.key == pygame.K_SPACE and game_state:
                                                
                                                bird_pos = 0
                                                bird_pos += 8
                                                
                                        if event.key == pygame.K_SPACE and game_state == False:
                                                  
                                                
                                                game_state = True 
                                                
                                                asteroid_list.clear()
                                                
                                                bird_rect.center = (100, 512) 
                                                
                                                bird_pos = 0
                                                
                                                score = 0
                                                
                                        if event.key == pygame.K_RIGHT and game_state:
                                            
                                            bird_rect.centerx += 50
                                            
                                        if event.key == pygame.K_UP and game_state:
                                            
                                            bird_rect.centery -= 70
                                            
                                        if event.key == pygame.K_DOWN and game_state:
                                            
                                            bird_rect.centery += 70  
                                            
                                    if event.type == SPAWNASTEROID:
                                        asteroid_list.extend(create_asteroid())
                                        
                                    if event.type == SPAWNDEBRIS:
                                        debris_list.extend(create_debris())
                                        
                                        
                                    if event.type == BIRDFLAP:
                                        
                                        if bird_index<2:
                                            
                                            bird_index += 1
                                        
                                        else:
                                            
                                            bird_index = 0
                                            
                                        bird_surface, bird_rect = bird_animation()
                                        
                                screen.blit(bg_surface,(0,0))
                                        
                                if game_state:

                                    #Bird
                                    bird_pos -= gravity
                                    
                                    rotated_bird = rotate_bird(bird_surface)
                                    
                                    bird_rect.centery += bird_pos
                                    
                                    screen.blit(rotated_bird,bird_rect)
                                    
                                    game_state = check_collision(asteroid_list)
                                    
                                    asteroid_list = move_asteroid(asteroid_list)
                                    
                                    draw_asteroids(asteroid_list)
                                    
                                    check_debris(debris_list)
                                    
                                    debris_list = move_debris(debris_list)
                                    
                                    draw_debris(debris_list)
                                    
                                    score += 0.01
                                    
                                    score_display()
                                
                                floor_position -= 1
                                
                                create_floor()
                                
                                if floor_position <= -576:                                    
                                    floor_position = 0                                
                                pygame.display.update()
                                clock.tick(120)

            pygame.display.update()

    pygame.display.update()