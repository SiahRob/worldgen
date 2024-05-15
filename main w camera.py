import tsapp
import time
import world_generation as w


world_class = w.WorldGeneration(1)

world = world_class.generate_world() #1070 682
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

x_position = 970
y_position = 682
for i in range(len(world)):
    if 100 < world[i].position[0] < 970 and 100 < world[i].position[1] < 682:
        window.add_object(world[i].sprite)

while window.is_running:
    print(x_position, y_position)

    for i in range(len(world)):
        if 100 < world[i].position[0] < 970 and 100 < world[i].position[1] < 682:
            window.add_object(world[i].sprite)
            world[i].refresh_sprite()
        if 100 > world[i].position[0] > 970 and 100 > world[i].position[1] > 682:
            world[i].sprite.destroy()
            world[i].refresh_sprite()

    if tsapp.is_key_down(tsapp.K_d):
        for i in range(len(world)):
            world[i].sprite.x -= 20
        x_position -= 20
    elif tsapp.is_key_down(tsapp.K_a):
        for i in range(len(world)):
            world[i].sprite.x += 20
        x_position += 20
    if tsapp.is_key_down(tsapp.K_w):
        for i in range(len(world)):
            world[i].sprite.y += 20
        y_position += 20
    elif tsapp.is_key_down(tsapp.K_s):
        for i in range(len(world)):
            world[i].sprite.y -= 20
        y_position -= 20





    window.finish_frame()
