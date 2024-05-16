import tsapp
# import time
import pygame
import world_generation as w
import blocks
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
player.center_y = window.height / 2
player.center_x = window.width / 2
window.add_object(player)
rendered_blocks = []
block_coll_var = 56
while window.is_running:
    mouse_x, mouse_y = tsapp.get_mouse_position()

    for i in range(len(world)):
        if -100 < world[i].sprite.center_x < window.width + 100 and -100 < world[i].sprite.center_y < window.height + 100:
            window.add_object(world[i].sprite)
            rendered_blocks.append(world[i])
        if -100 < world[i].sprite.center_x < window.width + 100 and -100 < world[i].sprite.center_y < window.height + 100:
            world[i].sprite.destroy()
            rendered_blocks.remove(world[i])
        if world[i].sprite.is_colliding_point((mouse_x, mouse_y)) and tsapp.was_mouse_pressed():
            air = tsapp.Sprite("sprites/air block.png", world[i].sprite.x, world[i].sprite.y)
            block = blocks.Block(air, (), "air block", False)
            window.add_object(air)
            world[i] = block

    if tsapp.is_key_down(tsapp.K_d):
        """
        for i in range(len(world)):
            block_right_face_coll = world[i].sprite.center_x - block_coll_var <= player.x + player.width <= world[i].sprite.center_x + block_coll_var and (player.y + player.height) > world[i].sprite.y + 15 and player.y < world[i].sprite.y + world[i].sprite.width
            if block_right_face_coll and world[i].block_has_collision:
                break
        else:
            for i in range(len(world)):
        """
        for i in range(len(world)):
            world[i].sprite.x -= 15

    if tsapp.is_key_down(tsapp.K_a):
        """
        for i in range(len(world)):
            block_left_face_coll = world[i].sprite.center_x - block_coll_var <= player.x <= world[i].sprite.center_x + block_coll_var and (player.y + player.height) > world[i].sprite.y + 15 and player.y < world[i].sprite.y + world[i].sprite.width
            if block_left_face_coll and world[i].block_has_collision:
                break
        else:
            for i in range(len(world)):
        """
        for i in range(len(world)):
            world[i].sprite.x += 15

    if tsapp.is_key_down(tsapp.K_w):
        """"
        for i in range(10):
            for i in range(len(world)):
                if player.is_colliding_rect(world[i].sprite) and world[i].block_has_collision:
                    block_bottom_face_coll = world[i].sprite.y + world[i].sprite.width - 56 < player.y < world[i].sprite.y + world[i].sprite.width
                    if block_bottom_face_coll and world[i].block_has_collision:
                        break
            else:
                for i in range(len(world)):
        """
        for i in range(len(world)):
            world[i].sprite.y += 15

    if tsapp.is_key_down(tsapp.K_s):
        """
        for i in range(len(world)):
            if player.is_colliding_rect(world[i].sprite) and world[i].block_has_collision:
                block_top_face_coll = world[i].sprite.y + 56 > player.y + player.height > world[i].sprite.y
                if block_top_face_coll and world[i].block_has_collision:
                    break
        else:
            for i in range(len(world)):
        """
        for i in range(len(world)):
            world[i].sprite.y -= 15

    window.finish_frame()
