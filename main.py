'''
ToDo:
Upravit na každém volání kontrolu kolize. 
Má být - na Spaceship volat skrz všechny objetky hit_by_spaceship a každý objekt rozhodne
nemá být - na Meteoru se vola skrz vsechny objekty hit_by_laser
'''


# Screen size (in pixels)
from tkinter import LEFT
from turtle import width
import pyglet
import math
from random import randrange, choice, uniform
from pyglet import gl

#screen resolution
WIDTH = 900
HEIGHT = 600

#game speed
ROTATION_SPEED = 4  # radians per second
ACCELERATION = 250

objects = [] #list of all objects in game
stisknute_klavesy = set()  # set of pressed keys
classes_in_game = set() # set of classes in game - for check, if in the game is stil an asteroid, laser etc. 

# List of PNG pictures
batch = pyglet.graphics.Batch()
from pngs import spaceships_pngs, meteor_pngs, laser, wallpaper

#collision and distances checks between circles
def distance(a, b, wrap_size):
    """Distance in one direction (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):
    """Returns true iff two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared

class SpaceObject:
    def __init__(self, picture):
        self.x = 0
        self.y = 0
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = 0
        self.sprite = pyglet.sprite.Sprite(picture, batch=batch)

    def tick(self, dt):
        #object mechanic
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed
        #check wheter object is in window
        #exit from window on the right
        if self.x > WIDTH:
            self.x = 0
        #exit from window on the left
        if self.x < 0:
            self.x = WIDTH
        #exit from window on the top
        if self.y > HEIGHT:
            self.y = 0
        #exit from window at bottom
        if self.y < 0:
            self.y = HEIGHT

        #sprite coordinates
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - math.degrees(self.rotation)
    
    def reset(self):
        pass

    def delete(self):
        objects.remove(self)
        self.sprite.delete()
        del self

    #method "hit_by_spaceship" called for every object,
    #only by objet meteor causes deleting the ship
    def hit_by_spaceship(self, ship):
        pass
    
    #method "hit_by_laser" called for every object,
    #only by object meteor causes deleting the meteor and laser itself
    def hit_by_laser(self, meteor):
        pass

class Spaceship(SpaceObject):
    def __init__(self, picture):
        super().__init__(picture)
        self.name = "Spaceship"
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.lifes = 3
        self.immortality_time = 3
        self.radius = 40
        self.attack_time = 0.5
    
    def __str__(self):
        return self.name

    def reset(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.immortality_time = 3
        
    def tick(self, dt):
        #object mechanic
        super().tick(dt)
        self.attack_time -= dt
        self.immortality_time -= dt

        #reactions on pressed keys
        if ('right') in stisknute_klavesy:
            self.rotation = self.rotation - dt * ROTATION_SPEED
        if ('left') in stisknute_klavesy:
            self.rotation = self.rotation + dt * ROTATION_SPEED
        if ('nahoru') in stisknute_klavesy:
            self.x_speed += dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed += dt * ACCELERATION * math.sin(self.rotation)
        if ('dolu') in stisknute_klavesy:
            self.x_speed -= dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed -= dt * ACCELERATION * math.sin(self.rotation)
        if ('space') in stisknute_klavesy and self.attack_time < 0:
            objects.append(Laser(laser, self.x, self.y, self.rotation))
            self.attack_time = 0.5

        #max velocity check
        if self.x_speed > 500:
            self.x_speed = 500
        if self.y_speed > 500:
            self.y_speed = 500
        if self.x_speed < -500:
            self.x_speed = -500
        if self.y_speed < -500:
            self.y_speed = -500
        
        #collison check with other objects
        for object in objects:
            if overlaps(self, object):
                object.hit_by_spaceship(self) #pokud je kolize, vola se metoda h_b_s a predava se ji argument - nazev lodi (pokud by bylo lodi vic, aby trida Meteor vedela, kterou lod smazat)

class Meteor(SpaceObject):
    def __init__(self, picture):
        super().__init__(picture)
        self.name = "Meteor"
        self.x = randrange(0, WIDTH)
        self.y = randrange(0, HEIGHT)
        self.x_speed = randrange(10, 150)
        self.y_speed = randrange(10, 150)
        self.rotation = randrange(-1, 1)
        self.rotation_speed = uniform(-3, 3)
        self.radius = 50

    def __str__(self):
        return self.name
    
    def tick(self, dt):
        #object mechanic
        super().tick(dt)
        self.rotation = self.rotation + dt * self.rotation_speed
        
        #collison check with other objects --> PŘEDĚLAT NA VOLANÍ SKRZ OBJEKTY "hit_by_meteor"!!!
        for object in objects:
            if overlaps(self, object):
                object.hit_by_laser(self) #pokud je kolize, vola se metoda h_b_s a predava se ji argument - nazev lodi (pokud by bylo lodi vic, aby trida Meteor vedela, kterou lod smazat)
    
    #changed method hit_by_spaceship, which takes argument - concete ship (if there were more than one, so it is clear, which one to destroy)
    def hit_by_spaceship(self, ship):
        if ship.immortality_time < 0:
            ship.x_speed = 0
            ship.y_speed = 0
            ship.rotation = 0
            ship.x = WIDTH / 2
            ship.y = HEIGHT / 2
            ship.lifes -= 1
            ship.immortality_time = 3

class Laser(SpaceObject):
    def __init__(self, picture, x, y, rot):
        super().__init__(picture)
        self.name = "Laser"
        self.x = x
        self.y = y
        self.rotation = rot
        self.radius = 15
        self.time = 2
        self.x_speed = math.cos(self.rotation) * 600
        self.y_speed = math.sin(self.rotation) * 600

    def __str__(self):
        return self.name

    def tick(self, dt):
        super().tick(dt)

        self.time -= dt
        if self.time < 0:
            self.delete()

        #check if the laser is in window
        #window exit on the left or right
        if self.x > (WIDTH-6) or self.x < 6:
            self.delete()
        #window exit on the top or at the bottom
        if self.y > (HEIGHT-6) or self.y < 6: 
            self.delete()
    
    def hit_by_laser(self, meteor):
        meteor.delete()
        self.delete()

class Level:
    def __init__(self):
        self.level = 1

    def create_asteroids(self):
        for i in range(self.level * 3):
            objects.append(Meteor(meteor_pngs[randrange(10)]))
    
    def tick(self, dt):
        if ship.lifes == 0:
            pass
        for object in objects:
            classes_in_game.add(str(object))
        if "Meteor" not in classes_in_game:
            self.level += 1 
            for object in objects:
                object.reset()           
            self.create_asteroids()
        print(classes_in_game)
        classes_in_game.clear()

def stisk_klavesy(symbol, modifikatory):
    if symbol == pyglet.window.key.UP:
        stisknute_klavesy.add('nahoru')
    if symbol == pyglet.window.key.DOWN:
        stisknute_klavesy.add('dolu')
    if symbol == pyglet.window.key.RIGHT:
        stisknute_klavesy.add('right')
    if symbol == pyglet.window.key.LEFT:
        stisknute_klavesy.add('left')
    if symbol == pyglet.window.key.SPACE:
        stisknute_klavesy.add('space')

def pusteni_klavesy(symbol, modifikatory):
    if symbol == pyglet.window.key.UP:
        stisknute_klavesy.discard('nahoru')
    if symbol == pyglet.window.key.DOWN:
        stisknute_klavesy.discard('dolu')
    if symbol == pyglet.window.key.RIGHT:
        stisknute_klavesy.discard('right')
    if symbol == pyglet.window.key.LEFT:
        stisknute_klavesy.discard('left')
    if symbol == pyglet.window.key.SPACE:
        stisknute_klavesy.discard('space')

def nakresli_text(text, x, y, pozice_x):
    """Draw the text in added position

    Arg ``pozice_x`` is "left" or "right", defines the text aligment
    """
    napis = pyglet.text.Label(
        text,
        font_name='Impact',
        font_size=22,
        x=x, y=y, anchor_x=pozice_x
    )
    napis.draw()

def nakresli_skore():
    score = pyglet.sprite.Sprite(ship_pic)
    score.scale = 0.5
    score.x = 40
    score.y = 80
    for i in range(ship.lifes):
        score.draw()
        score.x += 50

def background():
    wall_spr = pyglet.sprite.Sprite(wallpaper)
    wall_spr.x = 0
    wall_spr.y = 0
    wall_spr.scale = 0.75
    for i in range(4):
        for j in range(6):
            wall_spr.draw()
            wall_spr.x += 192
        wall_spr.x = 0
        wall_spr.y += 192

def obnov_stav(dt):
    # calls on all object method 'tick'
    for object in objects:
        object.tick(dt)
    level.tick(dt)

def vykresli():
    
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # clear window --> black color
    gl.glColor3f(100, 100, 100)  # set the draw line onto white

    background()

    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            # Remember the current state
            gl.glPushMatrix()
            # Move everything drawn from now on by (x_offset, y_offset, 0)
            gl.glTranslatef(x_offset, y_offset, 0)

            # Draw
            batch.draw()

            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()
    
    #draw score and lifes
    nakresli_text(f'Level {level.level}', 20, 20, LEFT)
    nakresli_skore()

ship_pic = choice(spaceships_pngs)
ship = Spaceship(ship_pic)
objects.append(ship)
level = Level()
level.create_asteroids()


window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy
)

pyglet.clock.schedule_interval(obnov_stav, 1/30)
pyglet.app.run()  # starts the game