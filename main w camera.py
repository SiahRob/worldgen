import tsapp
import time
import pygame
import world_generation as w
pygame.init()

world_class = w.WorldGeneration(1)

world = world_class.generate_world()
window = tsapp.GraphicsWindow(1070, 682, (200, 200, 255))

# need to add a camera instead of chunk based.
# gotta rework how it gets compiled into chunks, rather give all blocks their unique position
# add two variables, x and y position, as the player moves, x and y position are updated
# camera is centered to the players position
# add an area around the camera, anything within that area is rendered, make it bigger than the screen ofc
# have a list of all the blocks that are rendered, since everything has its own unique value, there is no need for a list matrix
# check for collision for the blocks that are in that list, going to have to rework main even more :/

player = tsapp.Sprite("sprites/player person.png", 0, 0)
player.scale = 0.5
player.center_y = 341
player.center_x = 535
window.add_object(player)

while window.is_running:

    for i in range(len(world)):
        if -100 < world[i].sprite.center_x < window.width + 100 and -100 < world[i].sprite.center_y < window.height + 100:
            window.add_object(world[i].sprite)
        if -100 < world[i].sprite.center_x < window.width + 100 and -100 < world[i].sprite.center_y < window.height + 100:
            world[i].sprite.destroy()

    if tsapp.is_key_down(tsapp.K_d):
        for i in range(len(world)):
            world[i].sprite.x -= 20
    elif tsapp.is_key_down(tsapp.K_a):
        for i in range(len(world)):
            world[i].sprite.x += 20
    if tsapp.is_key_down(tsapp.K_w):
        for i in range(len(world)):
            world[i].sprite.y += 20
    elif tsapp.is_key_down(tsapp.K_s):
        for i in range(len(world)):
            world[i].sprite.y -= 20

    window.finish_frame()
