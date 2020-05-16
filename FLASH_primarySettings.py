# last edited April 14, 2020
import os
import pygame as pg
import math

############# Settings #############
windowHeight = 600
windowWidth = 800
gameFullscreen = True
FOV = math.pi/4
screenIterator = 5
rayIncrementor = 0.05
movementControls = [pg.K_w, pg.K_s, pg.K_a, pg.K_d]
mouseFlag = False
renderingDistance = 5
flashlightRenderingDistance = 10
frameLimit = 30
fog_level = 0
fog_rect = pg.Rect(0,0,800,600)
difficulty = 'normal'

# Pygame window
pg.init()
window = pg.display.set_mode((windowWidth, windowHeight), pg.HWSURFACE|pg.DOUBLEBUF)
pg.mixer.init()

############# Menu Assets #############
pause = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_pause.png')).convert_alpha()

############# General Assets #############
winIcon = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_MenuAssets', 'FLASH_icon.png')).convert_alpha()


############# Game Assets #############
# Environment
background = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_background.png')).convert_alpha()
maxWallDistance = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_maxWallDistance.jpg')).convert_alpha()
wall = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_wall.png')).convert_alpha()
door = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_door.png')).convert_alpha()
battery = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Pickups', 'FLASH_battery.png')).convert_alpha()
shadowMonster = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Monster', 'FLASH_shadowMonster.png')).convert_alpha()
hallucination = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Monster', 'FLASH_hallucination.png')).convert_alpha()
fog = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_fog.png'))
fog.fill((255,255,255))
gameOverScreen = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_MenuAssets', 'FLASH_over.png')).convert_alpha()
key = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Pickups', 'FLASH_key.png')).convert_alpha()
keyIcon = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_key.png')).convert_alpha()
escape = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_escape.png')).convert_alpha()
win = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_MenuAssets', 'FLASH_win.png')).convert_alpha()
win = pg.transform.scale(win,(800,600))

# Environment sounds
step = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_steps.wav'))
step.set_volume(0.5)
pickup = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_ding.wav'))
keyPickup = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_discovery.wav'))

# Player Loss
cutscene = sorted(os.listdir('FLASH_JumpScare'))
jumpScareNoise = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_jumpscare.ogg'))
gameOverNoise = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_gameOver.ogg'))
shadowSwoosh = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_swoosh.ogg'))

# Flashlight
# Flashlight Images
flashlightHalf = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Flashlight', 'FLASH_flashlightHalfway.png')).convert_alpha()
flashlightOff = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Flashlight', 'FLASH_flashlightOff.png')).convert_alpha()
flashlightOn = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_InteractiveAssets', 'FLASH_Flashlight', 'FLASH_flashlightOn.png')).convert_alpha()

# Flashlight Noise
flashlightSwitchSound = pg.mixer.Sound(os.path.join(os.path.dirname('__file__'), 'FLASH_SoundEffects', 'FLASH_flashlightOn.wav'))
flashlightSwitchSound.set_volume(0.1)

# Battery
battery0 =  pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_battery0.png')).convert_alpha()
batteryLow =  pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_batteryLow.png')).convert_alpha()
batteryMed =  pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_batteryMed.png')).convert_alpha()
batteryFull =  pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_UI', 'FLASH_batteryFull.png')).convert_alpha()