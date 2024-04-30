import blocks
import tsapp
import time

window = tsapp.GraphicsWindow(1070, 714, (200, 200, 255))


def load_chunks(chunkrem, chunkadd):
    for chunkre in chunkrem:
        chunkre.block_has_collision = False
        chunkre.sprite.visible = False
        chunkre.sprite.destroy()
    for chunkad in chunkadd:
        chunkad.block_has_collision = True
        chunkad.sprite.visible = True
        chunkad.refresh_sprite()
        window.add_object(chunkad.sprite)


player = tsapp.Sprite("sprites/player person.png", 0, 0)

player.scale = 0.5
player.center_x = 510
player.center_y = 437
chunks = []
test_blocks = []
test_blocks2 = []
test_blocks3 = []

for x in range(11):
    grass = tsapp.Sprite("sprites/grass block.png", 0, 0)
    grass.x = 0 + (x * (grass.width - 3))
    grass.y = 714 - grass.height
    block = blocks.Block(grass, (grass.center_x, grass.center_y), "grass block", True, window)
    test_blocks.append(block)

for x in range(11):
    grass = tsapp.Sprite("sprites/grass block.png", 0, 0)
    grass.x = 0 + (x * (grass.width - 3))
    grass.y = 617 - grass.height
    block = blocks.Block(grass, (grass.center_x, grass.center_y), "grass block", True, window)
    test_blocks2.append(block)


for x in range(11):
    grass = tsapp.Sprite("sprites/grass block.png", 0, 0)
    grass.x = 0 + (x * (grass.width - 3))
    grass.y = 514 - grass.height
    block = blocks.Block(grass, (grass.center_x, grass.center_y), "grass block", True, window)
    test_blocks3.append(block)

chunks.append(test_blocks)
chunks.append(test_blocks2)
chunks.append(test_blocks3)

for i in range(len(chunks[0])):
    center_block_index = len(chunks[0]) / 2
    window.add_object(chunks[0][i].sprite)
    chunks[0][i].block_has_collision = True
    player.y = chunks[0][int(center_block_index)].sprite.y - player.height * 1.2
    player.center_x = chunks[0][int(center_block_index)].sprite.center_x

current_chunk = 0
window.add_object(player)
player.y_speed = 300
start = time.time()
block_coll_var = 56
while window.is_running:
    seconds_passed = time.time() - start
    if tsapp.is_key_down(tsapp.K_d):
        for i in range(len(chunks[current_chunk])):
            block_right_face_coll = chunks[current_chunk][i].sprite.center_x - block_coll_var <= player.x + player.width <= chunks[current_chunk][i].sprite.center_x + block_coll_var and (player.y + player.height) > chunks[current_chunk][i].sprite.y + 15 and player.y < chunks[current_chunk][i].sprite.y + chunks[current_chunk][i].sprite.width
            if block_right_face_coll and chunks[current_chunk][i].block_has_collision:
                player.x_speed = 0
                player.x = chunks[current_chunk][i].sprite.x - player.width
                break
            elif not block_right_face_coll:
                player.x_speed = 200

    elif tsapp.is_key_down(tsapp.K_a):
        for i in range(len(chunks[current_chunk])):
            block_left_face_coll = chunks[current_chunk][i].sprite.center_x - block_coll_var <= player.x <= chunks[current_chunk][i].sprite.center_x + block_coll_var and (player.y + player.height) > chunks[current_chunk][i].sprite.y + 15 and player.y < chunks[current_chunk][i].sprite.y + chunks[current_chunk][i].sprite.width
            if block_left_face_coll and chunks[current_chunk][i].block_has_collision:
                player.x_speed = 0
                player.x = chunks[current_chunk][i].sprite.x + chunks[current_chunk][i].sprite.width
                break
            elif not block_left_face_coll:
                player.x_speed = -200

    else:
        player.x_speed = 0

    for i in range(len(chunks[current_chunk])):

        if player.is_colliding_rect(chunks[current_chunk][i].sprite) and chunks[current_chunk][i].block_has_collision:
            if tsapp.was_key_pressed(tsapp.K_SPACE):
                start = time.time()
                player.y -= 10
                player.y_speed = -300
                in_air = True
                break

            elif chunks[current_chunk][i].sprite.y + 15 > player.y + player.height > chunks[current_chunk][i].sprite.y and chunks[current_chunk][i].block_has_collision:
                player.y_speed = 0
                player.y = chunks[current_chunk][i].sprite.y - player.height

            elif chunks[current_chunk][i].sprite.y + chunks[current_chunk][i].sprite.width - 15 < player.y < chunks[current_chunk][i].sprite.y + chunks[current_chunk][i].sprite.width and chunks[current_chunk][i].block_has_collision:
                player.y_speed = 0
                player.y = chunks[current_chunk][i].sprite.y + chunks[current_chunk][i].sprite.width + 1

        elif seconds_passed > 0.425:
            player.y_speed = 300

    if player.center_x < 0:
        if not current_chunk == 0:
            load_chunks(chunks[current_chunk], chunks[current_chunk - 1])
            current_chunk -= 1
            player.center_x = 1070
            player.y = chunks[current_chunk][-1].sprite.y - player.height - 1
        elif player.x_speed < 0:
            player.x_speed = 0
    elif player.center_x > 1070:
        if not current_chunk == len(chunks) - 1:
            load_chunks(chunks[current_chunk], chunks[current_chunk + 1])
            current_chunk += 1
            player.center_x = 0
            player.y = chunks[current_chunk][0].sprite.y - player.height - 1
        elif player.x_speed > 0:
            player.x_speed = 0
    if player.center_y < 0:
        player.center_y = 714
    elif player.center_y > 714:
        player.center_y = 0
    window.finish_frame()
