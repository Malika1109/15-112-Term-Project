import aubio
import numpy as np
import pyaudio

import pygame
import sys
import random
import math


import time
import argparse

from threading import Thread
import queue

import music21

from threading import Thread


from voiceController import Q, get_current_note

a = input("What mode do you want to play? (Enter Voice/Normal) ")
if a == "Voice":
    pygame.init()
    screenWidth, screenHeight = 288, 512
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()
    running = True
    titleFont = pygame.font.Font(pygame.font.get_default_font(), 34)
    titleText = titleFont.render("Sing a", True, (0, 128, 0))
    titleCurr = titleFont.render("Low Note", True, (0, 128, 0))
    noteFont = pygame.font.Font(pygame.font.get_default_font(), 55)
    t = Thread(target=get_current_note)
    t.daemon = True
    t.start()
    low_note = ""
    high_note = ""
    have_low = False
    have_high = True
    noteHoldLength = 20  # how many samples in a row user needs to hold a note
    noteHeldCurrently = 0  # keep track of how long current note is held
    noteHeld = ""  # string of the current note
    centTolerance = 20  # how much deviance from proper note to tolerate
    q = queue.Queue()
    p = pyaudio.PyAudio()
    # Open stream.
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, input=True,
                    input_device_index=0, frames_per_buffer=4096) #Here my input_device_index is 0 but it depends on the user's
                                                                   #device 
    time.sleep(1)
    # Aubio's pitch detection.
    pDetection = aubio.pitch("default", 2048,
        2048//2, 44100)
    # Set unit.
    pDetection.set_unit("Hz")
    pDetection.set_silence(-40)

    def position_on_range(low_note, high_note, volume_thresh=.001, cent_range=3):
        lowNote = music21.note.Note(low_note)
        highNote = music21.note.Note(high_note)
        vocalInterval = music21.interval.notesToInterval(lowNote, highNote)
        current_pitch = music21.pitch.Pitch()
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            samples = np.fromstring(data,
                                    dtype=aubio.float_type)
            pitch = pDetection(samples)[0]

            # Compute the energy (volume) of the
            # current frame.
            volume = np.sum(samples**2)/len(samples)

            if pitch and volume > volume_thresh: # adjust with your mic! .0002 if for my telecaster, .001 for my mic
                current_pitch.frequency = pitch
            else:
                continue

            if current_pitch.microtone.cents > cent_range:
                #print("Outside of Cent Range with %i" % current_pitch.microtone.cents)
                continue

            current = current_pitch.nameWithOctave
            cur_interval = music21.interval.notesToInterval(lowNote, current_pitch)
            #print(cur_interval.cents/vocalInterval.cents)
            q.put(cur_interval.cents / vocalInterval.cents)
            

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        screen.fill((0, 0, 0))
        
        # draw line to show visually how far away from note voice is
        pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
        pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290),
                         (screenWidth - 10, 310))
        pygame.draw.line(screen, (255, 255, 255), (10, 300),
                         (screenWidth - 10, 300))

        # our user should be singing if there's a note on the queue
        if not Q.empty():
            b = Q.get()
            #print(b)
            if b['Cents'] < 15:
                pygame.draw.circle(screen, (0, 128, 0), 
                                   (screenWidth // 2 + (int(b['Cents']) * 2),300),
                                   5)
            else:
                pygame.draw.circle(screen, (128, 0, 0),
                                   (screenWidth // 2 + (int(b['Cents']) * 2), 300),
                                   5)

            noteText = noteFont.render(b['Note'], True, (0, 128, 0))
            if b['Note'] == noteHeldCurrently:
                noteHeld += 1
                if noteHeld == noteHoldLength:
                    if not have_low:
                        low_note = noteHeldCurrently
                        have_low = True
                        titleCurr = titleFont.render("High Note", True, 
                                                     (128, 128, 0))
                    else:
                        if int(noteHeldCurrently[-1]) <= int(low_note[-1]):
                            noteHeld = 0  # we're holding a lower octave note
                        elif int(noteHeldCurrently[-1]) and not high_note:
                            high_note = noteHeldCurrently
                            have_high = True
                            titleText = titleFont.render("Perfect!", True,
                                                         (0, 128, 0))
                            titleCurr = titleFont.render("%s to %s" % 
                                                         (low_note, high_note), 
                                                         True, (0, 128, 0))
                            
                            #print(low_note,high_note)
                            
                            m = Thread(target=position_on_range, args=(low_note, high_note))
                            m.daemon = True
                            m.start()
                            
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
                                        
                                        #hit_sound.play()                                        
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
                                score_rect = score_surface.get_rect(center = (288,150))
                                screen.blit(score_surface,score_rect)
                                
                            def lives_display():
                                life_surface = game_font.render("LIVES",True,(255,255,255))
                                life_rect = life_surface.get_rect(center = (60,60))
                                screen.blit(life_surface,life_rect)
                                
                            def bird_pic_display(lives):                                
                                #if lives == 3:
                                for i in range(lives):
                                    bird_surface = pygame.image.load('bluebird-midflap.png').convert_alpha()
                                    bird_surface = pygame.transform.scale2x(bird_surface)
                                    bird_rect = bird_surface.get_rect(center = (150 + 80*i,60))                                
                                    screen.blit(bird_surface,bird_rect)


                            pygame.init()
                            screen = pygame.display.set_mode((576,1024))
                            clock = pygame.time.Clock()
                            game_font = pygame.font.Font(pygame.font.get_default_font(),40)  
                            gravity = 0.05
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
                            pygame.time.set_timer(GETPIPE,2500)
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
                                        #if event.key == pygame.K_SPACE and game_state == False:
                                        if game_state == False:
                                        
                                            game_state = True
                                            pipe_list.clear()
                                            bird_rect.center = (100, 512)                                             
                                            score = 0
                                            lives -= 1
                                            if lives == 0:
                                                lives = 3                                            
                                            
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
                                    rotated_bird = rotate_bird(bird_surface)
                                    if not q.empty():
                                        b = q.get()
                                        #print(b)
                                        if b > 0 and b < 1:
                                            print(b)
                                            bird_rect.centery = 700 - int(700*b)

                                    screen.blit(rotated_bird,bird_rect)                                    
                                    game_state = pipe_collision(pipe_list)                                    
                                    pipe_list = move_pipes(pipe_list)                                    
                                    draw_pipes(pipe_list)                                    
                                    score += 0.02                                    
                                    score_display()                                    
                                    lives_display()                                    
                                    bird_pic_display(lives)
                                    
                                else:
                                    if lives == 1:
                                        screen.blit(game_over_surface, game_over_rect)                                        
                                        score_display()
                                    score_display()
                                
                                
                                #Floor
                                #To move the floor backwards continuously
                                floor_position -= 1                                
                                create_floor()                                
                                if floor_position <= -576:                                    
                                    floor_position = 0
                                pygame.display.update()
                                clock.tick(120)    

            else:
                noteHeldCurrently = b['Note']
                noteHeld = 1
            screen.blit(noteText, (50, 400))

        screen.blit(titleText, (10,  80))
        screen.blit(titleCurr, (10, 120))
        pygame.display.flip()
        clock.tick(30)
    

if a == "Normal":

    pygame.init()
    home_screen = pygame.display.set_mode((576,1024))
    surface_1 = pygame.image.load('background-day copy.png').convert() 
    surface_1 = pygame.transform.scale2x(surface_1)
    surface_2 = pygame.image.load('underwayer copy.png').convert()
    surface_3 = pygame.image.load('space copy.png').convert()
    running1 = True
    running2 = True
    running3 = True
    running4 = True
    running5 = True
    running6 = True
    
    #Function which draws home screen
    def home_menu():     
            pygame.init()
            home_screen = pygame.display.set_mode((576,1024))
            surface_1 = pygame.image.load('background-day copy.png').convert() 
            surface_1 = pygame.transform.scale2x(surface_1)
            surface_2 = pygame.image.load('underwayer copy.png').convert()
            surface_3 = pygame.image.load('space copy.png').convert()
            home_screen.blit(surface_1,(0,0),(0,0,576,1024//3))            
            home_screen.blit(surface_2,(0,1024//3),(0,0,576,1024//3))            
            home_screen.blit(surface_3,(0,2*(1024//3)),(0,0,576,1024//3))            
            game_font = pygame.font.Font(pygame.font.get_default_font(),30)            
            instructions_button = pygame.draw.rect(home_screen,(255,255,255),(190,75,200,50))            
            instructions_surface = game_font.render("Instructions",True,(0,0,0))                                        
            instructions_rect = instructions_surface.get_rect(center = (280,100))            
            home_screen.blit(instructions_surface,instructions_rect)            
            normal_button = pygame.draw.rect(home_screen,(255,255,255),(190,150,200,50))                
            underwater_button = pygame.draw.rect(home_screen,(255,255,255),(190,500,200,50))               
            space_button = pygame.draw.rect(home_screen,(255,255,255),(190,700,200,50))                    
            normal_surface = game_font.render("Classic",True,(0,0,0))                                        
            normal_rect = normal_surface.get_rect(center = (300,170))            
            home_screen.blit(normal_surface,normal_rect)            
            underwater_surface = game_font.render("Underwater",True,(0,0,0))                                         
            underwater_rect = underwater_surface.get_rect(center = (300,520))            
            home_screen.blit(underwater_surface,underwater_rect)                
            space_surface = game_font.render("Space",True,(0,0,0))                                        
            space_rect = space_surface.get_rect(center = (300,720))            
            home_screen.blit(space_surface,space_rect)
            
    

    while running1:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                
                sys.exit()
                running1 = False
                running2 = False
        
        home_menu()
        
        while running2:
        
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                  
                    home_menu()
                   
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    running3 = True
                    running4 = True
                    running5 = True
                    running6 = True
                    if pygame.mouse.get_pos()[0] >= 190 and pygame.mouse.get_pos()[1] >= 75:
                        if pygame.mouse.get_pos()[0] <= 390 and pygame.mouse.get_pos()[1] <= 125:
                            running6 = True
                            
                            
                            pygame.init()
                            screen = pygame.display.set_mode((576,1024))

                            clock = pygame.time.Clock()

                            game_font = pygame.font.Font(pygame.font.get_default_font(),40)
                            game_font2 = pygame.font.Font(pygame.font.get_default_font(),20)
                            
                            bg_surface = pygame.image.load('background-day.png').convert() 
                            bg_surface = pygame.transform.scale2x(bg_surface)
                            
                            while running6:
                                
                                for event in pygame.event.get():
                                    
                                    if event.type == pygame.QUIT:
                                        home_menu
                                        running6 = False
                            
                                screen.blit(bg_surface,(0,0))
                                
                                line1_surface = game_font.render("Instructions",True,(0,0,0))                            
            
                                line1_rect = line1_surface.get_rect(center = (285,150))
            
                                home_screen.blit(line1_surface,line1_rect)
                                
                                
                                line2_surface = game_font2.render("For Classic Flappy Bird game, press Space to Jump",True,(0,0,0))                            
            
                                line2_rect = line2_surface.get_rect(center = (275,300))
            
                                home_screen.blit(line2_surface,line2_rect)
                                
                                line3_surface = game_font2.render("For Underwater Environment, navigate with right",True,(0,0,0))                            
            
                                line3_rect = line3_surface.get_rect(center = (275,400))
            
                                home_screen.blit(line3_surface,line3_rect)
                                
                                line4_surface = game_font2.render(",up and down arrow keys",True,(0,0,0))                            
            
                                line4_rect = line4_surface.get_rect(center = (275,450))
            
                                home_screen.blit(line4_surface,line4_rect)
                                
                                line5_surface = game_font2.render("Click Mouse button to shoot debris and Space to restart",True,(0,0,0))                            
            
                                line5_rect = line5_surface.get_rect(center = (275,500))
            
                                home_screen.blit(line5_surface,line5_rect)
                                 
                                line6_surface = game_font2.render("For Space Environment, prese space bar to go down",True,(0,0,0))                            
            
                                line6_rect = line6_surface.get_rect(center = (275,600))
            
                                home_screen.blit(line6_surface,line6_rect)
                                
                                line7_surface = game_font2.render("Collision with debris places bird at center",True,(0,0,0))                            
            
                                line7_rect = line7_surface.get_rect(center = (275,650))
            
                                home_screen.blit(line7_surface,line7_rect)
                                
                                line8_surface = game_font2.render("and collision with asteroid results in a blast",True,(0,0,0))                            
            
                                line8_rect = line8_surface.get_rect(center = (275,700))
            
                                home_screen.blit(line8_surface,line8_rect)
                                
                                
                                pygame.display.update()
                                clock.tick(120)
                    
                    
                    if pygame.mouse.get_pos()[0] >= 190 and pygame.mouse.get_pos()[1] >= 150:
                        if pygame.mouse.get_pos()[0] <= 390 and pygame.mouse.get_pos()[1] <= 200:
                            running3 = True
                            
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
                                        
                                        hit_sound.play()
                                        
                                        return False
                                        
                                if bird_rect.top<= -90 or bird_rect.bottom >= 1000:
                                    hit_sound.play()
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
                                score_rect = score_surface.get_rect(center = (288,150))
                                screen.blit(score_surface,score_rect)
                                
                            def lives_display():
                                life_surface = game_font.render("LIVES",True,(255,255,255))
                                life_rect = life_surface.get_rect(center = (60,60))
                                screen.blit(life_surface,life_rect)
                                
                            def bird_pic_display(lives):
                                
                                #if lives == 3:
                                for i in range(lives):
                                    bird_surface = pygame.image.load('bluebird-midflap.png').convert_alpha()

                                    bird_surface = pygame.transform.scale2x(bird_surface)

                                    bird_rect = bird_surface.get_rect(center = (150 + 80*i,60))
                                
                                    screen.blit(bird_surface,bird_rect)


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
                            #Sound files obtained from https://www.sounds-resource.com/mobile/flappybird/sound/5309/
                            wing_sound = pygame.mixer.Sound('sfx_wing.wav')

                            hit_sound = pygame.mixer.Sound('sfx_hit.wav')

                            score_sound = pygame.mixer.Sound('sfx_point.wav')

                            pipe_list = []

                            GETPIPE = pygame.USEREVENT
                            pygame.time.set_timer(GETPIPE,1000)

                            pipe_height = [400,600,800] 

                            #Game over image obtained at https://github.com/ian13456/flapp5/blob/master/assets/sprites/message.png
                            game_over_surface = pygame.image.load('message.png').convert_alpha()
                            game_over_surface = pygame.transform.scale2x(game_over_surface)
                            game_over_rect = game_over_surface.get_rect(center = (288,512))

                            lives = 3


                            while running3:
                                
                                for event in pygame.event.get():
                                    
                                    if event.type == pygame.QUIT:
                                        home_menu()
                                        running3 = False
                                        #pygame.quit()
                                       
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE and game_state:
                                            bird_pos = 0
                                            bird_pos -= 8
                                            
                                            wing_sound.play()
                                        
                                        
                                        if event.key == pygame.K_SPACE and game_state == False:
                                            
                                            game_state = True
                                            pipe_list.clear()
                                            bird_rect.center = (100, 512) 
                                            bird_pos = 0
                                            score = 0
                                            lives -= 1
                                            if lives == 0:
                                                lives = 3
                                            
                                            
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
                                    
                                    lives_display()
                                    
                                    bird_pic_display(lives)
                                    
                                else:
                                    if lives == 1:
                                        screen.blit(game_over_surface, game_over_rect)
                                        
                                        score_display()
                                        
                                    score_display()
                                
                                
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
                            
                            running4 = True
                            
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
                                    
                                    jelly.centerx -= 5
                                    if score>20:
                                        jelly.centerx -= 7
                                    if score>40 :
                                         jelly.centerx -= 10
                                    if score>60:
                                        jelly.centerx -= 13
                                    
                                return jellies

                            def draw_jellies(jellies,collision_jelly_state = False):
                                
                                for jelly in jellies:
                                    
                                    if collision_jelly_state == False:
                                        
                                        screen.blit(jelly_surface, jelly)
                                        

                            def check_jelly(jellies):
                                
                                for jelly in jellies:
                                    
                                    bird = bird_rect.inflate(-70,-70)
                                    if bird.colliderect(jelly):
                                        hit_sound.play()
                                        return False
                                    
                                
                                if bird_rect.top<= -100 or bird_rect.bottom >= 900:
                                    hit_sound.play()
                                    return False

                                if bird_rect.left<=0:
                                    hit_sound.play()
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
                                
                            def create_debris():
                                    
                                    top_debris = debris_surface.get_rect(midtop = (512,random.randint(0,1024)))
                                    bottom_debris = debris_surface.get_rect(midtop = (512,random.randint(900,1000)))
                                    return top_debris,bottom_debris
                                
                                
                            def draw_debris(debris_list,collision_state = False):
                                    for debris in debris_list:
                                        if collision_state == False:
                                            screen.blit(debris_surface,debris)
                                        
                            def move_debris(debris_list):
                                    
                                    for debris in debris_list:
                                        debris.centerx -= 3
                                        
                                    return debris_list
                                
                            def check_debris(debris_list):
                                    
                                    for debris in debris_list:
                                        bird = bird_rect.inflate(-500,-500)
                                        if bird.colliderect(debris):
                                            #bird_rect.centery += 40
                                            return False
                                            
                            def create_bullet():
                                
                                top_bullet = bullet_surface.get_rect(midtop = (bird_rect.center))
                                bottom_bullet = bullet_surface.get_rect(midtop = (bird_rect.center))
                                #print(bullet_surface,bullet_rect)
                                return top_bullet,bottom_bullet

                            def draw_bullet(bullet_list,collision_state = False):
                                
                                for i in range(len(bullet_list)):
                                    if collision_state == False:
                                        screen.blit(bullet_surface,bullet_list[i])
                                    
                                    
                            def get_coords(xy_position):
                                return xy_position[0],xy_position[1]
                                    
                            def move_bullet(bullet_list,xy_position=(0,0)):
                               # Mouse_x, Mouse_y = pygame.mouse.get_pos()
                                for bullet in bullet_list:
                                    if xy_position == (0,0):
                                        pass
                                    else:
                                        print(xy_position)
                      
                                    bullet.centerx+= 10
                                   
                                return bullet_list

                            def check_bullet(bullet_list,debris_list,count=1):
                                collided = False
                                for bullet in bullet_list:
                                    for debris in debris_list:
                                        if bullet.colliderect(debris):
                                          
                                            collided = True
                                            debris_list.remove(debris)
                                            bullet_list.remove(bullet)
                                            
                                        
                                return collided

                            def check_bullet2(bullet_list,jelly_list):
                                collided = False
                                for bullet in bullet_list:
                                    for jelly in jelly_list:
                                        if bullet.colliderect(jelly):
                                            collided = True
                                            jelly_list.remove(jelly)
                                            
                                            
                                            
                            def lives_display():
                                life_surface = game_font.render("LIVES",True,(255,255,255))
                                life_rect = life_surface.get_rect(center = (60,60))
                                screen.blit(life_surface,life_rect)
                                
                            def bird_pic_display(lives):
                                
                                #if lives == 3:
                                for i in range(lives):
                                    bird_surface = pygame.image.load('bluebird-midflap.png').convert_alpha()

                                    bird_surface = pygame.transform.scale2x(bird_surface)

                                    bird_rect = bird_surface.get_rect(center = (150 + 80*i,60))
                                
                                    screen.blit(bird_surface,bird_rect)

                                
                            pygame.init()

                            screen = pygame.display.set_mode((576,1024))

                            clock = pygame.time.Clock()

                            game_font = pygame.font.Font(pygame.font.get_default_font(),40)

                            bg_surface = pygame.image.load('underwater2.jpg').convert()

                            floor_surface = pygame.image.load('base copy.png').convert()

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

                            debris_surface = pygame.image.load('debris.png').convert_alpha()

                            bullet_surface = pygame.image.load('bullet.png').convert_alpha()

                            wing_sound = pygame.mixer.Sound('sfx_wing.wav')

                            hit_sound = pygame.mixer.Sound('sfx_hit.wav')

                            score_sound = pygame.mixer.Sound('sfx_point.wav')

                            #Game over image obtained at https://github.com/ian13456/flapp5/blob/master/assets/sprites/message.png
                            game_over_surface = pygame.image.load('message.png').convert_alpha()
                            game_over_surface = pygame.transform.scale2x(game_over_surface)
                            game_over_rect = game_over_surface.get_rect(center = (288,512))

                            lives = 3

                            SPAWNDEBRIS = pygame.USEREVENT+2
                                
                            pygame.time.set_timer(SPAWNDEBRIS, 2500)
                                
                            debris_list = []

                            SPAWNJELLY = pygame.USEREVENT

                            pygame.time.set_timer(SPAWNJELLY,3000)

                            jelly_height = [100,80,90]

                            bullet_list = []

                            SPAWNBULLET = pygame.USEREVENT+3

                            pygame.time.set_timer(SPAWNBULLET, 2500)

                            bird_pos = 0

                            game_state = True

                            viscosity = 2

                            gravity = 0.25

                            score = 0

                            xy_position = (100,100)
                            co_list = []
                            def new_list(xy_position=(0,0)):
                                
                                #co_list = []
                                co_list.append(xy_position)
                                #print(co_list)
                                return co_list

                            #while True:
                            while running4:
                                
                                for event in pygame.event.get():
                                    
                                    if event.type == pygame.QUIT:
                                        home_menu()
                                        running4 = False
                                        
                                    if event.type == pygame.KEYDOWN:    
                                       
                                            
                                        if event.key == pygame.K_SPACE and game_state == False:
                                                
                                              
                                                game_state = True                                                 
                                                jelly_list.clear()                                                
                                                debris_list.clear()                                                
                                                bullet_list.clear()                                                
                                                co_list.clear()
                                                bird_rect.center = (100, 512)                                                 
                                                bird_pos = 0                                                
                                                score = 0                                                
                                                lives -= 1
                                                if lives == 0:
                                                    lives = 3
                                                
                                                
                                        if event.key == pygame.K_RIGHT and game_state:
                                            
                                            bird_rect.centerx += 50
                                            wing_sound.play()
                                            
                                        if event.key == pygame.K_UP and game_state:
                                            
                                            bird_rect.centery -= 70                                            
                                            wing_sound.play()
                                            
                                        if event.key == pygame.K_DOWN and game_state:
                                            
                                            bird_rect.centery += 70                                            
                                            wing_sound.play()
                                
                                    
                                    if event.type == SPAWNJELLY:
                                        jelly_list.extend(create_jelly())
                                        
                                    if event.type == SPAWNDEBRIS:
                                        debris_list.extend(create_debris())
                                        
                                        
                                    if event.type == BIRDFLAP:
                                        
                                        if bird_index<2:                                            
                                            bird_index += 1
                                        
                                        else:
                                            
                                            bird_index = 0                                            
                                        bird_surface, bird_rect = bird_animation()
                                        
                                    if event.type == pygame.MOUSEBUTTONDOWN and game_state:

                                        
                                        xy_position = event.pos
                                        new_list(xy_position)
                                        
                                        
                                        x_coord = xy_position[0]
                                        y_coord = xy_position[1]
                                        
                                        x_dist = (((bird_rect.center[0]-xy_position[0])**2) + ((bird_rect.center[1]-xy_position[1])**2))**0.5
                                        
                                        y_dist = abs(xy_position[0] - bird_rect.center[0])
                                        
                                        angle = math.acos(y_dist/x_dist)
                                        n_angle = angle * (180/math.pi)
                                        
                                        if xy_position[1]>bird_rect.center[1]:
                                            bird_surface = pygame.transform.rotate(bird_surface,-n_angle)
                                        else:
                                            bird_surface = pygame.transform.rotate(bird_surface,n_angle)
                                       
                                        bullet_list.extend(create_bullet())
                                        
                                                
                                                
                                        bullet_list = move_bullet(bullet_list,xy_position)
                                                
                                        draw_bullet(bullet_list)
                                            
                                screen.blit(bg_surface,(0,0))
                                
                                if game_state:
                                    
                                    #Bird
                                    bird_rect.centerx -= viscosity      
                                    
                                    rotated_bird = rotate_bird(bird_surface)
                                    
                                    bird_rect.centery += bird_pos
                                    
                                    screen.blit(rotated_bird,bird_rect)
                                    

                                    game_state = check_jelly(jelly_list)
                                    
                                    jelly_list = move_jelly(jelly_list)
                                    
                                    draw_jellies(jelly_list)

                                    collision_state = check_bullet(bullet_list,debris_list)
                                    
                                    if collision_state == True:
                                        score+= 5
                                    
                                    draw_bullet(bullet_list,collision_state)
                                    
                                    bullet_list = move_bullet(bullet_list)
                                    
                                    check_debris(debris_list)
                                        
                                    debris_list = move_debris(debris_list)
                                        
                                    draw_debris(debris_list,collision_state)
                                    
                                    score += 0.01
                                    
                                    score_display()
                                    
                                    lives_display()
                                    
                                    bird_pic_display(lives)
                                    
                                else:
                                    if lives == 1:
                                        screen.blit(game_over_surface, game_over_rect)
                                        
                                        score_display()
                                        
                                        
                                    score_display()
                                                                                  
                                floor_position -= 1
                                
                                create_floor()
                                
                                if floor_position <= -576:
                                    
                                    floor_position = 0

                                pygame.display.update()
                                clock.tick(120)
                                
    #                             
                    if pygame.mouse.get_pos()[0] >= 190 and pygame.mouse.get_pos()[1] >= 700:
                        if pygame.mouse.get_pos()[0] <= 390 and pygame.mouse.get_pos()[1] <= 750:
                            
                            running5 = True
                            
                            def create_floor():
                                screen.blit(floor_surface,(floor_position,900))
                                screen.blit(floor_surface,(floor_position + 576,900))


                            def create_asteroid():
                                random_asteroid_pos = random.choice(asteroid_height) 
                                bottom_asteroid = asteroid_surface.get_rect(midtop = (512,random_asteroid_pos))
                                
                                top_asteroid = asteroid_surface.get_rect(midbottom = (512,random.randint(700,1000)))
                                return bottom_asteroid,top_asteroid

                            def create_debris():
                                
                                top_debris = debris_surface.get_rect(midtop = (512,random.randint(0,100)))
                                bottom_debris = debris_surface.get_rect(midtop = (512,random.randint(900,1000)))
                                return top_debris,bottom_debris

                            def move_asteroid(asteroids):
                                count = 0
                                for asteroid in asteroids:
                                   
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
                                  screen.blit(asteroid_surface, asteroid)
                                    
                            def draw_debris(debris_list):
                                for debris in debris_list:
                                    
                                    screen.blit(debris_surface,debris)
                                    

                            def check_collision(asteroids):
                                
                                for asteroid in asteroids:
                                    bird = bird_rect.inflate(-70,-70)
                                    if bird.colliderect(asteroid):
                                        screen.blit(blast_surface,blast_rect)
                                        hit_sound.play()           
                                        return False
                                        
                                if bird_rect.top<= -100 or bird_rect.bottom >= 900:
                                    hit_sound.play()
                                    return False
                               
                                return True

                            def check_debris(debris_list):
                                
                                for debris in debris_list:
                                    bird = bird_rect.inflate(-70,-70)
                                    if bird.colliderect(debris):
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
                                
                            def lives_display():
                                life_surface = game_font.render("LIVES",True,(255,255,255))
                                life_rect = life_surface.get_rect(center = (60,60))
                                screen.blit(life_surface,life_rect)
                                
                            def bird_pic_display(lives):
                                
                                #if lives == 3:
                                for i in range(lives):
                                    bird_surface = pygame.image.load('bluebird-midflap.png').convert_alpha()
                                    bird_surface = pygame.transform.scale2x(bird_surface)
                                    bird_rect = bird_surface.get_rect(center = (150 + 80*i,60))                                
                                    screen.blit(bird_surface,bird_rect)    




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
                            #Asteroid image obtained from http://www.pngmart.com/image/51311
                            ast_normal = pygame.transform.scale2x(pygame.image.load('asteroid.png').convert_alpha())
                            #Blast image obtained from http://www.pngall.com/explosion-png
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

                            wing_sound = pygame.mixer.Sound('sfx_wing.wav')

                            hit_sound = pygame.mixer.Sound('sfx_hit.wav')

                            score_sound = pygame.mixer.Sound('sfx_point.wav')

                            debris_surface = pygame.image.load('debris.png').convert_alpha()

                            #Game over image obtained at https://github.com/ian13456/flapp5/blob/master/assets/sprites/message.png
                            game_over_surface = pygame.image.load('message.png').convert_alpha()
                            game_over_surface = pygame.transform.scale2x(game_over_surface)
                            game_over_rect = game_over_surface.get_rect(center = (288,512))

                            lives = 3

                            SPAWNDEBRIS = pygame.USEREVENT+2
                            pygame.time.set_timer(SPAWNDEBRIS, 2500)
                            debris_list = []
                            bird_pos = 0
                            game_state = True
                            viscosity = 2
                            gravity = 0.25
                            score = 0
                            #while True:
                            while running5:
                                

                                for event in pygame.event.get():
                                    
                                    if event.type == pygame.QUIT:
                                        home_menu()
                                        running5 = False
                                        
                                    if event.type == pygame.KEYDOWN:    
                                        
                                        if event.key == pygame.K_SPACE and game_state:
                                                
                                                bird_pos = 0
                                                bird_pos += 8                                                
                                                wing_sound.play()
                                          
                                        if event.key == pygame.K_SPACE and game_state == False:
                                                                                                  
                                                game_state = True 
                                                asteroid_list.clear()
                                                bird_rect.center = (100, 512) 
                                                bird_pos = 0
                                                score = 0
                                                lives -= 1
                                                if lives == 0:
                                                    lives = 3
                                            
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
                                    lives_display()                                    
                                    bird_pic_display(lives)
                                    
                                else:
                                    if lives == 1:
                                        screen.blit(game_over_surface, game_over_rect)                                        
                                        score_display()
                                    score_display()
                                           
                                floor_position -= 1                                
                                create_floor()                                
                                if floor_position <= -576:                                    
                                    floor_position = 0
                                
                                pygame.display.update()
                                clock.tick(120)
                pygame.display.update()

        pygame.display.update()
        
else:
    print("Please enter correct input")
    
        