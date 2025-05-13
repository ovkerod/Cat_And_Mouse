"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame
import game_objects as obj
import random
import sys
from pygame import mixer


# Define some colors
BLACK = (0, 0, 0)
DIRT = (81, 51, 7)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
GREEN = (0, 125, 0)
DARK_GREEN = (0, 25, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 139)
LIGHT_BLUE = (135, 206, 235)
YELLOW = ('#E2BC00')

pygame.init()

mixer.init()
mixer.music.load("Assets/Audio/Music/game-music-loop-7-145285.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.5)


# Set the width and height of the screen [width, height]


GAME_NAME = "Cat and Mouse"
screen_w, screen_h = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
w, h = screen.get_size()
SPACING = (h+w)/2 * 0.1
CAT_BORDER = (h+w)/2 * 0.025

mute_button = obj.AudioButton(w, h)

pygame.display.set_caption(GAME_NAME)



fancy_font = pygame.font.SysFont(name='vivaldi', size=125)
basic_font_small = pygame.font.SysFont(name='arial', size=12)
basic_font_large = pygame.font.SysFont(name='arial', size=32)
basic_font_xl = pygame.font.SysFont(name='arial', size=72, bold=True)

cats = [obj.Cat((w, h)) for _ in range(10)]
menu_cat = obj.Cat((w, h))
cheese_objects = [obj.Cheese((w, h)) for _ in range(10)]
heart = obj.Heart((w, h))
player = obj.Mouse((w, h))

peaceful = False

game_manager = obj.GameManager()


def reset_button_command():
    return True

def end_session():
    pygame.quit()
    sys.exit()





reset_button = obj.Button(text="Main Menu", command=reset_button_command,
                          position=(w//2, 2*h//3), fg=BLACK, bg=DIRT, border_color=BLACK, font=basic_font_large)

exit_button = obj.Button(text="Quit Game", command=end_session,
                          position=(w//2, 9*h//10), fg=BLACK, bg=GREEN, border_color=BLACK, font=basic_font_large)

def generate_text(text, fg, bg, rect_center, border=None, border_width=5, font=basic_font_large):
    return_text = font.render(text, True, fg, bg)
    return_rect = return_text.get_rect()
    return_rect.center = rect_center
    if border:
        border_rect = return_rect.inflate(border_width, border_width)
        return (return_text, return_rect, (border, border_rect))
    return return_text, return_rect

def keep_mouse_inbounds():
    PLAY_AREA_LEFT = SPACING
    PLAY_AREA_TOP = SPACING
    PLAY_AREA_RIGHT = w - SPACING - player.sprite.get_width()//2
    PLAY_AREA_BOTTOM = h - SPACING - player.sprite.get_height()//2
    # Get current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Clamp mouse position within the play area
    clamped_x = max(PLAY_AREA_LEFT, min(PLAY_AREA_RIGHT, mouse_x))
    clamped_y = max(PLAY_AREA_TOP, min(PLAY_AREA_BOTTOM, mouse_y))
    new_position = (clamped_x, clamped_y)
    player.location = (
        clamped_x,
        clamped_y
    )
    # Actively reset the mouse position if it's out of bounds
    pygame.mouse.set_pos(new_position)
    if new_position == (mouse_x, mouse_y):
        player.bound_corrected = False
    else:
        player.bound_corrected = True


def generate_creatures():
    for cat in cats:
        if cat.spawned:
            screen.blit(cat.sprite, tuple(cat.location))
    if menu_cat.spawned:
        screen.blit(menu_cat.sprite, tuple(menu_cat.location))
    for cheese in cheese_objects:
        if cheese.spawned:
            screen.blit(cheese.sprite, tuple(cheese.location))

    screen.blit(player.sprite, player.location)


def generate_start_screen():
    screen.fill(LIGHT_BLUE)
    pygame.draw.rect(
        screen, GREEN, [0, 2*h//3, w, h//3], 0)
    pygame.draw.rect(
        screen, DIRT, [0, 3*h//4, w, h//4], 0)
    text_items = GAME_NAME.split(" ")
    generate_creatures()
    for index, item in enumerate(text_items):
        rect_center = (w * (index+1) // 4, 100 + h * (index+1) // 8)
        text, text_rect = generate_text(
            text=item, fg=BLACK, bg=LIGHT_BLUE, rect_center=rect_center, font=fancy_font)
        screen.blit(text, text_rect)

    start_text, start_rect = generate_text(
        "(Click Anywhere to Start)", DIRT, GREEN, (w//2, 45*h//64))
    screen.blit(start_text, start_rect)


    mute_button.rect= pygame.Rect(w/2-mute_button.w/2, 4*h/5 - mute_button.h/2, mute_button.w, mute_button.h)
    screen.blit(mute_button.sprites[int(mute_button.audio_playing)], mute_button.rect)

    pygame.draw.rect(screen, exit_button.border_color,
                        exit_button.border_rect)
    screen.blit(exit_button.text, exit_button.rect)

    version_text, version_rect = generate_text(
        "Alpha Version 1.0.0 \u00A9 Oleksander Kerod 2024",
        GREEN, DIRT, (w-200//2-5, h-12//2), font=basic_font_small)
    screen.blit(version_text, version_rect)


def generate_play_screen():
    # game field
    screen.fill(DIRT)
    pygame.draw.rect(
        screen, GREEN, [SPACING, SPACING, w-2*SPACING, h-2*SPACING], 0)

    # game objects
    generate_creatures()

    # player HUD
    score_text, score_rect = generate_text(
        f"Score: {game_manager.score}", BLACK, DIRT, (100, 30))
    screen.blit(score_text, score_rect)
    for i in range(game_manager.health):
        screen.blit(heart.sprite, (70 + w/50*i, 60))

    # menu after player dies
    if not player.active:
        pygame.draw.rect(
            screen, DIRT, [w//3-20, h//4-20, w//3+40, h//2+40], 0)
        pygame.draw.rect(
            screen, GREY, [w//3, h//4, w//3, h//2], 0)
        final_score_text, final_score_rect = generate_text(f"Final Score: {game_manager.score}",
                                                           WHITE,
                                                           GREY,
                                                           (w//2, h//3)
                                                           )
        final_time_text, final_time_rect = generate_text(f"Survival Time: {player.survival_time} s",
                                                         WHITE,
                                                         GREY,
                                                         (w//2, h//2)
                                                         )
        screen.blit(final_score_text, final_score_rect)
        screen.blit(final_time_text, final_time_rect)
        pygame.draw.rect(screen, reset_button.border_color,
                         reset_button.border_rect)
        screen.blit(reset_button.text, reset_button.rect)

    if paused:

        pygame.draw.rect(
            screen, DIRT, [w//3-20, h//4-20, w//3+40, h//2+40], 0)
        pygame.draw.rect(
            screen, GREY, [w//3, h//4, w//3, h//2], 0)
        pause_text, pause_rect = generate_text(
            "Paused", BLACK, GREY, (w//2, h//3), font=basic_font_xl)
        screen.blit(pause_text, pause_rect)
        pygame.draw.rect(screen, reset_button.border_color,
                         reset_button.border_rect)
        mute_button.rect= pygame.Rect(w/2 - mute_button.w/2, h/2 - mute_button.h/2, mute_button.w, mute_button.h)
        screen.blit(mute_button.sprites[int(mute_button.audio_playing)], mute_button.rect)
        screen.blit(reset_button.text, reset_button.rect)


def reset_home_anim():
    menu_cat.spawn([-300, 2*h//3 - menu_cat.sprite.get_height()])
    menu_cat.running = True

    player.location = [-50, 2*h//3 - player.sprite.get_height()]
    player.spawn()





def main():
    global paused
    clock = pygame.time.Clock()
    previous_animation_time = pygame.time.get_ticks()
    started = False

    pygame.mouse.set_visible(True)
    reset_home_anim()
    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_session()

            if event.type == pygame.MOUSEBUTTONUP:
                if mute_button.rect.collidepoint(event.pos):
                    if mute_button.audio_playing:
                        mute_button.audio_playing = False
                        mixer.music.set_volume(0)
                    else:
                        mute_button.audio_playing = True
                        mixer.music.set_volume(0.5)
                elif exit_button.rect.collidepoint(event.pos):
                    exit_button.command()
                else:
                    menu_cat.despawn()
                    started = True
        current_time = pygame.time.get_ticks()
        # home screen animation

        # home screen animation
        if current_time - previous_animation_time > 100:
            player.animate_running()
            player.location[0] += 9
            menu_cat.animate_running()
            menu_cat.location[0] += 10
            previous_animation_time = current_time

        if menu_cat.location[0] > w:
            reset_home_anim()

        generate_start_screen()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

        # Loop until the user clicks the close button.
    player.active = False
    pygame.mouse.set_visible(False)
    done = False
    paused = False
    # Used to manage how fast the screen updates
    previous_animation_time = pygame.time.get_ticks()
    previous_cheese_spawn_time = pygame.time.get_ticks()
    session_active = True
    immunity_time = 0
    death_time = None
    pygame.mouse.set_pos([w//2, h//2])   
    if not peaceful:
        cats[0].spawn(location=[50, 50])
        cats[0].speed = 8
        cats[0].pause_hold_state = (True, 8)
        cats[0].attack(pygame.mouse.get_pos())
        cats[0].stop_time = pygame.time.get_ticks()
        cats[0].running = True

    next_spawn = 1
    collision_counter = 0
    total_pause_duration = 0
    pause_duration = 0


    # -------- Main Program Loop -----------
    session_start_timer = pygame.time.get_ticks()
    while not done:
        current_time = pygame.time.get_ticks()
        running_time = current_time - pause_duration - total_pause_duration
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_session()
            if event.type == pygame.MOUSEBUTTONUP and (paused or not player.active):
                if mute_button.rect.collidepoint(event.pos) and paused:
                    if mute_button.audio_playing:
                        mute_button.audio_playing = False
                        mixer.music.set_volume(0)
                    else:
                        mute_button.audio_playing = True
                        mixer.music.set_volume(0.5)
                try:
                    if reset_button.rect.collidepoint(event.pos):
                        done = reset_button.command()
                except NameError:
                    pass
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and session_active:

                    if paused:
                        paused = False
                        pygame.mouse.set_visible(False)
                        pygame.mouse.set_pos((player.location[0] + player.sprite.get_width()//2,
                                              player.location[1] + player.sprite.get_height()//2))
                        total_pause_duration += pause_duration
                        pause_duration = 0

                    else:
                        paused = True
                        pygame.mouse.set_visible(True)
                        pause_start_time = current_time

        # --- Game logic should go here

        if not player.active and session_active and not paused:
            player.active = True
            player.location = (
                pygame.mouse.get_pos()[0] - player.sprite.get_width()//2,
                pygame.mouse.get_pos()[1] - player.sprite.get_height()//2
            )
            previous_location = player.location[0]

        # cat logic
        if session_active:
            for index, cat in enumerate(cats):
                if cat.spawned and player.active:
                    cat.move()
                    cat.update_rect()
                    if cat.location[0] + cat.sprite.get_size()[0] >= w-CAT_BORDER or cat.location[0] <= CAT_BORDER or cat.location[1] + cat.sprite.get_size()[1] >= h - CAT_BORDER or cat.location[1] <= CAT_BORDER:
                        side_detector = {cat.location[0] + cat.sprite.get_size()[0] >= w-CAT_BORDER: 'right', cat.location[0] <= CAT_BORDER: 'left',
                                         cat.location[1] + cat.sprite.get_size()[1] >= h-CAT_BORDER: 'bottom', cat.location[1] <= CAT_BORDER: 'top'}
                        if cat.collision_side != side_detector[True]:
                            cat.stop_time = pygame.time.get_ticks()
                            cat.speed_hold = cat.speed
                            cat.speed = 0
                            cat.running = False
                            cat.collision_side = side_detector[True]
                            if cat == cats[0]:
                                collision_counter += 1

                                if collision_counter % 3 == 0:
                                    try:
                                        cats[next_spawn].spawn([50, 50])
                                        cats[next_spawn].speed = 8
                                        cats[next_spawn].attack(
                                            pygame.mouse.get_pos())
                                        cats[next_spawn].running = True
                                        next_spawn += 1
                                    except IndexError:
                                        pass

                    if pygame.time.get_ticks() - cat.stop_time > cat.wait_time and not cat.running and not cat.paused:
                        cat.launch_time = pygame.time.get_ticks()
                        if (cat.launch_time - cat.stop_time > 2000):
                            print(f"""Launch Timing Error: {
                                cat.launch_time - cat.stop_time}, Cat No. {index}""")
                        cat.attack(pygame.mouse.get_pos())
                        cat.speed = cat.speed_hold
                        cat.running = True

                        cat.speed = min(cat.speed + 1, 20)
                        cat.wait_time = random.randint(50, 2000)
                    if not player.immune and cat.collision_rect.colliderect(player.collision_rect):
                        player.immune = True
                        immunity_time = running_time
                        death = game_manager.touch_cat()
                        if death:
                            for cat in cats:
                                cat.running = False
                                cat.speed = 0
                            session_active = False

            # mouse logic
            if not paused:
                keep_mouse_inbounds()

                player.location = (
                    pygame.mouse.get_pos()[0] - player.sprite.get_width()//2,
                    pygame.mouse.get_pos()[1] - player.sprite.get_height()//2
                )
            player.update_rect()
            if previous_location != player.location[0] and not player.bound_corrected and player.active:
                player.running = True
                position_change = player.location[0] - previous_location
                player.check_direction(position_change)
                previous_location = player.location[0]
            else:
                player.running = False
            if player.immune and running_time - immunity_time > 2000:
                player.immune = False

            # cheese logic
            for cheese in cheese_objects:
                if not cheese.spawned and running_time - previous_cheese_spawn_time > 5000:
                    cheese.spawn()
                    previous_cheese_spawn_time = running_time
                    break
                elif cheese.spawned and cheese.collision_rect.colliderect(player.collision_rect):
                    game_manager.eat_cheese()
                    cheese.despawn()

        # pause logic

        if paused:
            for cat in cats:
                if not cat.paused:
                    cat.pause()
            pause_duration = current_time - pause_start_time
        else:
            for cat in cats:
                if cat.paused:
                    cat.unpause()


        # animation control
        if current_time - previous_animation_time > 100:
            if player.active:
                if not player.running and session_active:
                    player.animate_idle()
                elif session_active:
                    player.animate_running()
                elif player.active:
                    player.animate_death()
                    if player.death_anim_index == 0:
                        if not death_time:
                            death_time = running_time
                            player.survival_time = (
                                death_time - session_start_timer) / 1000
                        player.death_anim_index -= 1

                        if pygame.time.get_ticks() - death_time > 1000:

                            player.active = False
                            pygame.mouse.set_visible(True)

            for cat in cats:
                if not cat.running:
                    cat.animate_idle()
                else:
                    cat.animate_running()
            previous_animation_time = current_time

        # --- Drawing code should go here
        generate_play_screen()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)
    for cat in cats:
        cat.despawn()
        cat.facing_left = False
        cat.running = False
    for cheese in cheese_objects:
        cheese.despawn()
    player.last_direction = 'forward'
    player.immune = False
    game_manager.reset()
    main()


if __name__ == "__main__":
    main()
