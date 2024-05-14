import tsapp
import time
import world_generation as w


world_class = w.WorldGeneration(1)

world = world_class.generate_world()
print(world)
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
player.center_x = 510
player.center_y = 437
player.center_y = 341
player.center_x = 535
window.add_object(player)

x_position = 0
y_position = 0
while window.is_running:

    if tsapp.is_key_down(tsapp.K_d):
        x_position += 1
    elif tsapp.is_key_down(tsapp.K_a):
        x_position -= 1
    if tsapp.is_key_down(tsapp.K_w):
        y_position += 1
    elif tsapp.is_key_down(tsapp.K_s):
        y_position -= 1

    for i in range(len(world)):
        if x_position == world[i].position[0] and y_position == world[i].position[1]:
            window.add_object(world[i])


    window.finish_frame()
