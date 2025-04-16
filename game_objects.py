import random
import pygame
import math
import pathlib


deg_to_rad = math.pi / 180

# game characters


class Cat(object):
    def __init__(self, screen_size):
        self.screen_size = screen_size
    
        # import and format running animations
        running_file_list = [file for file in pathlib.Path(
            'Assets/3 Cat/Run Frames').iterdir()]
        self.normal_running_sprites = [pygame.transform.scale(
            pygame.image.load(item), (screen_size[0]*0.035, screen_size[1]*0.035)) for item in running_file_list]
        self.flipped_running_sprites = [pygame.transform.flip(
            item, True, False) for item in self.normal_running_sprites]
        self.running_anim_index = 0

        # import and format idle animations
        idle_file_list = [file for file in pathlib.Path(
            'Assets/3 Cat/Idle Frames').iterdir()]
        self.normal_idle_sprites = [pygame.transform.scale(
            pygame.image.load(item), (screen_size[0]*0.035, screen_size[1]*0.035)) for item in idle_file_list]
        self.flipped_idle_sprites = [pygame.transform.flip(
            item, True, False) for item in self.normal_idle_sprites]
        self.idle_anim_index = 0
        sample = pygame.Rect(0, 0, 100, 100)
        self.sprite = self.normal_idle_sprites[0]
        self.facing_left = False
        self.running = False
        self.spawned = False
        self.location = None
        self.direction = None
        self.collision_side = None
        self.speed = 8
        self.speed_hold = None
        self.wait_time = 500
        self.collision_rect = None
        self.pause_hold_state = None
        self.paused = False

        # error testing
        self.stop_time = 0
        self.launch_time = None
        self.status_log = []

    def spawn(self, location=[50, 50]):
        self.location = location
        self.spawned = True
        self.collision_side = None
        self.update_rect()

    def despawn(self):
        self.spawned = False
        self.speed_hold = 8

    def move(self):
        self.location[0] += self.speed * math.cos(self.direction)
        print(self.speed)
        self.location[1] += self.speed * math.sin(-self.direction)
        self.collision_rect = self.sprite.get_rect()

    def animate_idle(self):

        self.sprite = self.normal_idle_sprites[self.idle_anim_index]
        self.idle_anim_index = (self.idle_anim_index + 1) % 4
        self.running_anim_index = 0

    def animate_running(self):
        self.sprite = self.normal_running_sprites[
            self.running_anim_index] if not self.facing_left else self.flipped_running_sprites[self.running_anim_index]
        self.running_anim_index = (self.running_anim_index + 1) % 6

    def reflect(self, wall):
        if wall == 'vertical':
            self.direction = 180 * deg_to_rad - self.direction
            self.location[0] += 2 * math.cos(self.direction)
        if wall == 'horizontal':
            self.direction = 360 * deg_to_rad - self.direction
            self.location[1] += 2 * math.sin(-self.direction)

    def attack(self, mouse_pos):
        self.sprite = pygame.transform.scale(
            pygame.image.load('Assets/3 Cat/Still.png'), (self.screen_size[0]*0.035, self.screen_size[1]*0.035))
        x, y = mouse_pos
        self.facing_left = int(x - self.location[0] < 0)
        attack_vector = [x - self.location[0], self.location[1] - y]
        self.direction = math.atan(
            attack_vector[1] / attack_vector[0]) - self.facing_left * 180 * deg_to_rad

    def update_rect(self):
        w, h = self.sprite.get_size()
        x, y = self.location
        self.collision_rect = pygame.rect.Rect(w//2 + x, h//2+y, w, h)

    def pause(self):
        self.pause_hold_state = self.running, self.speed
        self.running = False
        self.speed = 0
        self.paused = True

    def unpause(self):
        self.running, self.speed = self.pause_hold_state
        self.paused = False


class Mouse(object):
    def __init__(self, screen_size):

        # import and format idle animations
        idle_file_list = [file for file in pathlib.Path(
            'Assets/5 Rat/Idle Frames').iterdir()]
        self.normal_idle_sprites = [pygame.transform.scale(
            pygame.image.load(item), (screen_size[0]*0.035, screen_size[1]*0.015)) for item in idle_file_list]
        self.flipped_idle_sprites = [pygame.transform.flip(
            item, True, False) for item in self.normal_idle_sprites]
        self.damaged_idle_frames = [pygame.transform.scale(
            pygame.image.load(f'Assets/5 Rat/Damaged Idle Frames/tile00{i}.png'), (screen_size[0]*0.035, screen_size[1]*0.015)) for i in range(0, 3, 2)]

        self.damaged_flipped_idle_frames = [pygame.transform.flip(
            item, True, False) for item in self.damaged_idle_frames]
        self.idle_anim_index = 0

        # import and format running animations
        running_file_list = [file for file in pathlib.Path(
            'Assets/5 Rat/Run Frames').iterdir()]
        self.normal_running_sprites = [pygame.transform.scale(
            pygame.image.load(item), (screen_size[0]*0.035, screen_size[1]*0.015)) for item in running_file_list]
        self.flipped_running_sprites = [pygame.transform.flip(
            item, True, False) for item in self.normal_running_sprites]
        self.damaged_running_frames = [pygame.transform.scale(
            pygame.image.load(f'Assets/5 Rat/Damaged Run Frames/tile00{i}.png'), (screen_size[0]*0.035, screen_size[1]*0.015)) for i in range(0, 3, 2)]

        self.damaged_flipped_running_frames = [pygame.transform.flip(
            item, True, False) for item in self.damaged_running_frames]
        self.running_anim_index = 0

        # import and format death animation
        death_file_list = [file for file in pathlib.Path(
            'Assets/5 Rat/Death Frames').iterdir()]
        self.normal_death_sprites = [pygame.transform.scale(
            pygame.image.load(item), (screen_size[0]*0.035, screen_size[1]*0.015)) for item in death_file_list]
        self.flipped_death_sprites = [pygame.transform.flip(
            item, True, False) for item in self.normal_death_sprites]
        self.death_anim_index = 0

        self.sprite = self.normal_idle_sprites[self.idle_anim_index]
        self.last_direction = 'forward'
        self.location = None
        self.survival_time = None
        self.active = False
        self.direction = 'right'
        self.bound_corrected = False
        self.running = True
        self.immune = False
        self.collision_rect = None

    def spawn(self):
        self.active = True
        self.update_rect()

    def animate_running(self):
        sprite_direction = {'reverse': self.flipped_running_sprites,
                            'forward': self.normal_running_sprites}
        sprite_direction_damaged = {'reverse': self.damaged_flipped_running_frames,
                                    'forward': self.damaged_running_frames}
        self.sprite = sprite_direction[self.last_direction][self.running_anim_index] if self.running_anim_index % 2 != 0 or not self.immune else sprite_direction_damaged[self.last_direction][self.running_anim_index//2-1]
        self.running_anim_index = (self.running_anim_index + 1) % 4

    def animate_idle(self):

        self.running_anim_index = 0
        sprite_direction = {'reverse': self.flipped_idle_sprites,
                            'forward': self.normal_idle_sprites}
        sprite_direction_damaged = {'reverse': self.damaged_flipped_idle_frames,
                                    'forward': self.damaged_idle_frames}
        self.sprite = sprite_direction[self.last_direction][self.idle_anim_index] if self.idle_anim_index % 2 != 0 or not self.immune else sprite_direction_damaged[self.last_direction][self.idle_anim_index//2-1]
        self.idle_anim_index = (self.idle_anim_index + 1) % 4

    def animate_death(self):
        sprite_direction = {'reverse': self.flipped_death_sprites,
                            'forward': self.normal_death_sprites}
        self.sprite = sprite_direction[self.last_direction][self.death_anim_index]
        self.death_anim_index = (self.death_anim_index + 1) % 4

    def check_direction(self, direction_change):
        direction_table = {direction_change < 0: 'reverse',
                           direction_change > 0: 'forward'}
        try:
            self.last_direction = direction_table[True]
        except KeyError:
            pass

    def update_rect(self):
        w, h = self.sprite.get_size()
        x, y = self.location
        self.collision_rect = pygame.rect.Rect(w//2 + x, h//2+y, w, h)

# inanimate objects


class Cheese(object):
    def __init__(self, screen_size):
        self.sprite = pygame.transform.scale(pygame.image.load(
            'Assets/Items/Cheese.png'), (screen_size[0] * 0.035, screen_size[1] * 0.035))
        self.screen_size = screen_size
        self.location = None
        self.spawned = False
        self.collision_rect = None

    def spawn(self):
        self.location = [random.randint(
            200, self.screen_size[0] - 200), random.randint(200, self.screen_size[1] - 200)]
        self.spawned = True
        self.update_rect()

    def despawn(self):
        self.spawned = False

    def update_rect(self):
        w, h = self.sprite.get_size()
        x, y = self.location
        self.collision_rect = pygame.rect.Rect(w//2 + x, h//2+y, w, h)


class Heart(object):
    def __init__(self, screen_size):
        self.sprite = pygame.transform.scale(pygame.image.load(
            'Assets/Items/Heart.png'), (screen_size[0] * 0.015, screen_size[0] * 0.015))


class Button(object):
    def __init__(self, text: pygame.Surface, command, position: tuple, fg: tuple, bg: tuple, font: pygame.font.Font, border_color=None, border_width=5):
        self.text = font.render(text, True, fg, bg)
        self.command = command
        self.border_color = border_color
        self.border_width = border_width
        self.rect = self.text.get_rect()
        self.rect.center = position
        self.border_rect = pygame.Rect(
            self.rect.left-border_width, 
            self.rect.top-border_width, 
            self.rect.width + 2 * border_width, 
            self.rect.height + 2 * border_width
            )

class AudioButton(object):
    def __init__(self, w, h):
        self.audio_playing_sprite = pygame.transform.scale(
            pygame.image.load('Assets/Audio/Playing.png'), (w*0.025, h*0.035))

        self.audio_muted_sprite = pygame.transform.scale(
                    pygame.image.load('Assets/Audio/Muted.png'), (w*0.025, h*0.035))

        self.sprites = (self.audio_muted_sprite, self.audio_playing_sprite)

        self.w, self.h = self.audio_playing_sprite.get_size()
        self.rect: pygame.Rect = None

        self.audio_playing = True

    
        
        
# abstract objects


class GameManager:
    def __init__(self, health=3, score=0):
        self.health = health
        self.score = score
        self.reset_values = (health, score)

    def reset(self):
        self.health, self.score = self.reset_values

    def eat_cheese(self):
        self.score += 1

    def touch_cat(self):
        self.health -= 1
        if self.health == 0:
            return True
        return False
