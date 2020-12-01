


Malika Dikshit

											Super Flappy Bird

Project Description: My project will be a unique take on the classic Flappy Bird Game.

My Minimum Viable Project will be the Flappy Bird Game where the bird representing the user has to dodge the randomly generated pipes on the screen by pressing the space bar. The score of the user keeps increasing until the bird hits an obstacle. Once an obstacle is encountered, the game resets itself and places the bird back at the center of the screen with a score of 0. The user has three lives before the Game Over Screen is displayed.
To go beyond the MVP, my game will allow users to play in 2 modes: Voice Controlled and Normal
The voice Controlled version will implement voice controlled flappy bird where the program first asks the user for their vocal range: the lowest and highest possible note they can sing and then allow them to play the game where the bird's movement will be controlled by the pitch/frequency of the users voice. A higher pitch voice will move the bird upwards and a lower pitch will move it downwards.
The normal mode will display a home screen with instructions where users can choose 3 different environments : Classic, Underwater and Space.
The classic mode is implemented as described above. 
The underwater mode allows users to navigate the bird using arrow keys. Here, users can shoot debris but not jellyfish by clicking the mouse button. Shooting debris increases points by 5.
In the space mode, there is no gravity acting on the bird and by pressing the space bar the bird comes down. If the bird hits the debris, it does not die but is placed in the center of the screen where there may or may not be an asteroid resulting in a collision. If the bird hits an asteroid, there is a blast on screen.

The project can be run by running the Term Project 3.py file in the Term Project 3 folder which will be submitted on Gradescope. The Term Project 3 file imports the voiceController.py file which will also be included in the folder. The voice controlled version makes use of microphone, so the arguments to PyAudio object have to be given appropriately. Detailed instructions for microphone device are available as comments in the codebase. All necessary images and music files are included in the submitted folder.

The libraries used in my project are:
aubio
numpy
pyaudio
pygame
sys
random
math
time
argparse
threading (from threading import Thread)
queue
music21
voiceController(file name)

All of the above libraries can be installed in python using pip command.

There are no shortcut commands used in my project.

