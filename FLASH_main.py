#Last updated April 14 2020

import pygame as pg
import sys
import os
import FLASH_primarySettings as ps
import FLASH_characters
import FLASH_inanimates
import FLASH_rendering
import FLASH_menu


class MainLoop:
    '''
    The main loop object that describes the general methods to run the whole game
    ===============Attributes===============
    (Some of these are declared in startup() rather than init, so the game is replayable)
    windowHandle (pygame.display): the handle for the display the game is being drawn to
    gameMap (GameMap): the map object that describes the whole game
    camera (Camera): the camera of the player that translates the 2D math of their rays to a 3D views
    player (PlayerCharacter): the player's in-game representation
    clock (pygame.Clock): the clock describing the game's progress
    framerate (float): the framerate of the game that is used to track the current quality of the game
    imagesToLoad (Dict[string:pygame.image): dictionary for ease of access to assets to be sliced and rendered in game
    UI (Dict[string:pygame.image): dictionary for ease of access to assets that are rendered for player information
    shadow (ShadowMonster): the monster object that hunts the player throughout the game
    gameLoopFlag (bool): the flag that determines if the main game is running, or some other part is running
    '''
    def __init__(self):
        self.windowHandle = ps.window
        self.mapWidth = 16
        self.mapHeight = 42
        self.clock = pg.time.Clock()
        self.framerate = self.clock.tick(ps.frameLimit)
        self.imagesToLoad = {'wall':ps.wall, 'exit':ps.door, 'background':ps.background, 'far wall':ps.maxWallDistance, 'shadow monster': ps.shadowMonster, 'battery':ps.battery, 'hallucination':ps.hallucination, 'key':ps.key}
        self.UI = {'zero':ps.battery0, 'low':ps.batteryLow, 'med':ps.batteryMed, 'full':ps.batteryFull, 'key':ps.keyIcon}
        self.gameLoopFlag = True
        
    def startup(self, difficulty, screenIterator, mouseFlag):
        '''
        Establishes some parts of the game before the main loop is to be run
        Caption and icon is set, then the mouse is made invisible
        ===============Parameters===============
        difficulty (string): the difficulty of the game
        screenIterator (int): the width of the rendered slices in the game
        mouseFlag (bool): flag for whether a mouse or keyboard should be used (F = no mouse, T = mouse)
        
        returns nothing
        '''
        self.gameMap = FLASH_inanimates.GameMap(self.mapWidth,self.mapHeight, difficulty)
        self.startX = self.mapWidth/2 if self.mapWidth%2 == 0 else self.mapWidth//2 + 1
        self.startY = 2
        self.escapeOpacity = 260
        self.camera = FLASH_rendering.Camera(ps.windowWidth, ps.windowHeight, ps.FOV, screenIterator, self.windowHandle)
        self.player = FLASH_characters.PlayerCharacter(self.camera, self.startX, self.startY, 0.0, 0.0, ps.movementControls, mouseFlag, ps.renderingDistance, ps.flashlightRenderingDistance)
        self.shadow = FLASH_characters.ShadowMonster('A', difficulty)
        self.timePaused = 0
        ps.fog_level = 0
        ps.fog = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_RenderedElements', 'FLASH_fog.png'))
        ps.fog.fill((255,255,255))
        ps.escape = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_Environment', 'FLASH_escape.png')).convert_alpha()
        pg.display.set_caption('FLASH')
        pg.display.set_icon(ps.winIcon)
        pg.mouse.set_visible(False)
        
        
    
    def keypressChecks(self, event, menuTime):
        '''
        Changes player's various statuses depending on the event pygame is retrieving
        If escape, pause the game by going through a separate while loop
        ===============Parameters===============
        event (pygame.event): the event pygame has currently retrieved
        menuTime (float): number describing the amount of time in the main menu
        
        returns nothing
        '''
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                paused = True
                self.player.stopPhysicalMovement(pg.K_w, ps.step)
                pg.mixer.music.pause()
                pg.mixer.pause()
                while paused:
                    self.timePaused = (pg.time.get_ticks()/1000)- self.shadow.moveOpportunity - menuTime
                    self.windowHandle.blit(ps.pause,((0,0),(800,600)))
                    pg.display.update()
                    for event in pg.event.get():
                        if event == pg.QUIT:
                            pg.quit()
                            sys.exit()
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                paused = False
                                self.player.flashlight.batteries.off_time = pg.time.get_ticks()/1000
                                self.player.flashlight.batteries.drain = 1
                                pg.mixer.music.unpause()
                                pg.mixer.unpause()
                            if event.key == pg.K_q:
                                self.gameLoopFlag = False
                                paused = False
            if self.gameLoopFlag:    
                self.player.physicalMovementCalculation(event.key, ps.step)
                ps.fog_level = self.player.hideSwitch(event.key, self.windowHandle, self.clock, self.imagesToLoad, self.gameMap, self.shadow, self.UI, ps.flashlightSwitchSound, ps.step, ps.rayIncrementor, ps.fog, ps.fog_level, ps.fog_rect)
                self.player.flashlightSwitch(event.key)
                if not self.player.mouseFlag:
                    self.player.perspectiveMovementCalculation(event.key)
        if self.gameLoopFlag:
            if event.type == pg.KEYUP:
                self.player.stopPhysicalMovement(event.key, ps.step)
                if not self.player.mouseFlag:
                    self.player.perspectiveStop(event.key)
    
    def mover(self):
        '''
        Moves the player's physical position and perspective
        ===============Parameters===============
        ------------------NONE------------------
        
        returns nothing
        '''
        self.player.physicalMover(self.gameMap, ps.pickup, ps.keyPickup)
        self.player.perspectiveMover()

    def enemy(self, menuTime):
        '''
        Activates enemy functions
        ===============Parameters===============
        menuTime (int): the integer for the amount of time spent in the menu

        returns nothing
        '''
        charx = int(self.player.charX)
        chary = int(self.player.charY)
        if self.shadow.enemyX + 10 == charx or self.shadow.enemyX - 10 == charx or self.shadow.enemyY + 10 == chary or self.shadow.enemyY - 10 == chary:  #(abs(charx - self.shadow.enemyX) >= 5 or abs(chary - self.shadow.enemyY) >=5) and self.shadow.enemyX != 100:
            self.shadow.chase = False
            self.gameMap.mapArray[self.shadow.enemyY][self.shadow.enemyX] = '.'
            self.shadow.enemyY = 100
            self.shadow.enemyX = 100

        self.shadow.movementGenerator(self.player, self.gameMap, menuTime, self.timePaused)

        
    def renderScreen(self):
        '''
        Renders all the elements on the screen for the player
        ===============Parameters===============
        ------------------NONE------------------
        
        returns nothing
        '''
        self.windowHandle.fill((0,0,0))
        if not self.player.hiding:
            self.player.renderPlayerView(self.gameMap, '.', ['#','E'], self.imagesToLoad, self.shadow, ps.rayIncrementor)
            if self.shadow.fog == True:
                if ps.fog_level <= 150:
                    ps.fog_level += 1
            elif not self.shadow.fog:
                if ps.fog_level > 0:
                    ps.fog_level -= 1
            ps.fog.set_alpha(ps.fog_level)
            ps.window.blit(ps.fog, ps.fog_rect)
        
        if self.player.keyFlag:
            self.windowHandle.blit(self.UI['key'], (self.windowHandle.get_width() - self.UI['key'].get_width(), 0))
        self.player.flashlightControl(self.windowHandle, self.shadow, ps.flashlightSwitchSound)
        self.player.flashlight.batteries.drawBatteryLevel(self.windowHandle, self.UI)
        if self.escapeOpacity > 0:
            self.escapeOpacity -= 1
            self.windowHandle.blit(ps.escape, ((325, 250), (150, 100)))
        if self.escapeOpacity <= 255:
            ps.escape.fill((255, 255, 255, self.escapeOpacity), None, pg.BLEND_RGBA_MULT)

    
    def gameLoop(self, difficulty, screenIterator, mouseFlag, menuTime):
        '''
        The main loop for the game
        ===============Parameters===============
        difficulty (string): the difficulty of the game
        screenIterator (int): the width of the rendered slices in the game
        mouseFlag (bool): flag for whether a mouse or keyboard should be used (F = no mouse, T = mouse)
        menuTime (int): the integer for the amount of time spent in the menu
        
        returns nothing
        '''
        self.windowHandle.fill((0,0,0))
        pg.display.update()
        pg.time.delay(1000)
        self.startup(difficulty, screenIterator, mouseFlag)
        while self.gameLoopFlag:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                self.keypressChecks(event, menuTime)
            if self.gameLoopFlag:
                if self.player.mouseFlag:
                    self.player.perspectiveMovementCalculation(None)
                    if pg.mouse.get_focused():
                        pg.mouse.set_pos(self.player.initialPos)
                self.mover()
                self.renderScreen()
                self.enemy(menuTime)
                self.framerate = self.clock.tick(ps.frameLimit)
                pg.display.update()
            if self.player.winning == 0 and not self.player.flashlight.switching[0] and self.gameLoopFlag:
                self.player.stopPhysicalMovement(pg.K_w, ps.step)
                if self.player.hiding:
                    self.player.hideSwitch(pg.K_h, self.windowHandle, self.clock, self.imagesToLoad, self.gameMap, self.shadow, self.UI, ps.flashlightSwitchSound, ps.step, ps.rayIncrementor, ps.fog, ps.fog_level, ps.fog_rect)
                pg.mixer.fadeout(6000)
                pg.mixer.music.fadeout(6000)
                self.renderScreen()
                pg.display.update()
                self.player.loss(self.clock, self.windowHandle, self.gameMap, '.', ['#','E'], self.imagesToLoad, self.UI, ps.cutscene, self.shadow, ps.gameOverScreen, ps.gameOverNoise, ps.jumpScareNoise, ps.shadowSwoosh, ps.rayIncrementor)
                self.gameLoopFlag = False
            
            elif self.player.winning == 1:
                self.player.stopPhysicalMovement(pg.K_w, ps.step)
                if self.player.hiding:
                    self.player.hideSwitch(pg.K_h, self.windowHandle, self.clock, self.imagesToLoad, self.gameMap, self.shadow, self.UI, ps.flashlightSwitchSound, ps.step, ps.rayIncrementor, ps.fog, ps.fog_level, ps.fog_rect)
                pg.mixer.fadeout(6000)
                pg.mixer.music.fadeout(6000)
                self.renderScreen()
                pg.display.update()
                self.player.win(self.windowHandle, self.clock, self.gameMap, '.', ['#', 'E'], self.imagesToLoad, self.UI, self.shadow, ps.rayIncrementor, ps.difficulty, ps.win)
                self.gameLoopFlag = False
                


    def main(self):
        '''
        The loop describing all events of the game
        ===============Parameters===============
        ------------------NONE------------------
        
        returns nothing
        '''
        mainFlag = True
        gameFlag = False
        fullscreen = False
        difficulty = 1 #0 = Easy, 1 = Normal, 2 = Hard
        graphic_Setting = 1 #0 = Low, 1 = Medium, 2 = High
        controls = 0 #0 =  Mouse, 1 = Keyboard
        if sys.platform == 'darwin': 
            title = False
        else:
            title = True
        while mainFlag:
            if not gameFlag:
                settings = FLASH_menu.main_Menu(fullscreen, difficulty, graphic_Setting, controls, title)
                menuTime = settings[4]
                del(settings[4])
                FLASH_menu.settings_Change(settings)
                if settings[3] == True:
                    pg.display.set_mode((800,600), pg.HWSURFACE|pg.DOUBLEBUF|pg.FULLSCREEN)
                gameFlag = True
                title = False
                difficulty = settings[0]
                graphic_Setting = settings[1]
                controls = settings[2]
                fullscreen = settings[3]
            elif gameFlag:          
                self.gameLoop(ps.difficulty, ps.screenIterator, ps.mouseFlag, menuTime)
                ps.escape.fill((255, 255, 255, 255), None, pg.BLEND_RGBA_MULT)
                self.gameLoopFlag = True
                gameFlag = False
            

if __name__ == '__main__':
    game = MainLoop()
    game.main()
    pg.quit()
