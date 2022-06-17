import pyglet

spaceships_pngs = []
spaceship1 = pyglet.image.load('images\spaceship1.png')
spaceships_pngs.append(spaceship1)
spaceship2 = pyglet.image.load('images\spaceship2.png')
spaceships_pngs.append(spaceship2)
spaceship3 = pyglet.image.load('images\spaceship3.png')
spaceships_pngs.append(spaceship3)

for png in spaceships_pngs:
    png.anchor_x = png.width // 2
    png.anchor_y = png.height // 2

meteor_pngs = []
meteor1 = pyglet.image.load('images\meteorGrey_big1.png')
meteor_pngs.append(meteor1)
meteor2 = pyglet.image.load('images\meteorGrey_big2.png')
meteor_pngs.append(meteor2)
meteor3 = pyglet.image.load('images\meteorGrey_big3.png')
meteor_pngs.append(meteor3)
meteor4 = pyglet.image.load('images\meteorGrey_big4.png')
meteor_pngs.append(meteor4)
meteor5 = pyglet.image.load('images\meteorGrey_med1.png')
meteor_pngs.append(meteor5)
meteor6 = pyglet.image.load('images\meteorGrey_med2.png')
meteor_pngs.append(meteor6)
meteor7 = pyglet.image.load('images\meteorGrey_small1.png')
meteor_pngs.append(meteor7)
meteor8 = pyglet.image.load('images\meteorGrey_small2.png')
meteor_pngs.append(meteor8)
meteor9 = pyglet.image.load('images\meteorGrey_tiny1.png')
meteor_pngs.append(meteor9)
meteor10 = pyglet.image.load('images\meteorGrey_tiny2.png')
meteor_pngs.append(meteor10)

for png in meteor_pngs:
    png.anchor_x = png.width // 2
    png.anchor_y = png.height // 2

laser = pyglet.image.load('images\laser.png')
laser.anchor_x = laser.width // 2
laser.anchor_y = laser.height // 2

wallpaper = pyglet.image.load('images\wallpaper.png')