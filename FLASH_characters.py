#Last updated April 14 2020

import pygame as pg
import os
import sys
from datetime import date
import random
import math
import FLASH_inanimates
import FLASH_rendering

class Character:
    '''
    Describes a basic character in the game.
    ===============Attributes===============
    charX (int): x-coordinate position of the character
    charY (int): y-coordinate position of the character
    charDelX (float): value for change in x position, essentially x-speed
    charDelY (float): value for change in y position, essentially y-speed
    '''
    def __init__(self, charX, charY, charDelX, charDelY):
        self.charX = charX
        self.charY = charY
        self.charDelX = charDelX
        self.charDelY = charDelY
        
        
class PlayerCharacter(Character):
    '''
    Describes a playable character in the game, inherits from character.
    ===============Attributes===============
    playerCam (Camera): the player's camera that renders their POV
    charAngle (float): angle of the player relative to the position it was in from initialization
    charDelAngle (float): value for change in angle
    movementControls (List[pygame.key]): list of keys for physical movement, follows the pattern [fwd, bwd, left,right]
    mouseFlag (bool): Determines if the mouse should be used for moving player perspective (if false, use arrow keys instead)
    renderingDistance (int): the max range of the player's unaided eye
    flashlightRenderingDistance (int): the max range of the player's vision with the help of a flashlight
    flashlight (Flashlight): the flashlight object the player holds
    flashlightScreenDivision (int): the number of pixels wide the screen is segmented into
    moving (bool): flag for whether the player is moving or not so the step sound clip is not interrupted by itself
    keyFlag (bool): flag for whether the player has picked up the key
    hiding (bool): flag for whether the player is hiding from the monster
    drain (int): Used to drain battery power every second while flashlight is active.
    offTime (int): Tracks time flashlight is off so battery power cannot drain during that time.
    usage (int): Tracks time flashlight is on so battery power can drain during that time.
    bLid / tLid (pygame.Rect): Sets position of rectangles which are used to obstruct player view when hiding.
    winning (int): integer displaying if the player has won or lost (0 = going to lose, 1 = going to win, 2 = playing)
    initialPos (Tuple[int]): the coordinates of the mouse when the game begins (sometimes not used if the player uses arrow keys)
    '''
    def __init__(self,camera, charX, charY, charAngle, charDelAngle, movementControls, mouseFlag, renderingDistance, flashlightRenderingDistance):
        super(PlayerCharacter, self).__init__(charX, charY, 0.0, 0.0)
        self.playerCam = camera
        self.charAngle = charAngle
        self.charDelAngle = charDelAngle
        self.movementControls = movementControls
        self.mouseFlag = mouseFlag
        self.renderingDistance = renderingDistance
        self.flashlightRenderingDistance = flashlightRenderingDistance
        self.flashlight = FLASH_inanimates.Flashlight(False, 'B')
        self.flashlightScreenDivision =  camera.screenWidth // 16
        self.moving = False
        self.hiding = False
        self.keyFlag = False
        self.drain = 1
        self.offTime = None
        self.usage = None
        self.bLid = pg.Rect(0, 600, 800, 300)
        self.tLid = pg.Rect(0, -300, 800, 300)
        self.winning = 2
        if self.mouseFlag:
            self.initialPos = pg.mouse.get_pos()

    def physicalMovementCalculation(self, enteredKey, stepSound):
        '''
        Determines the amount the player character moves given a specific key and adjusts the player attribute accordingly
        splits up the player's movement into x and y so it can be translated onto the map grid. Multiplied so the player is
        going slow enough
        ===============Parameters===============
        enteredKey (pygame.key): the pressed key detected by pygame
        stepSound (pygame.mixer.Sound): the sound that is used to create stepping audio
        
        returns nothing
        '''
        if enteredKey in self.movementControls and not self.hiding:
            if enteredKey == self.movementControls[0]:
                self.charDelX = (math.sin(self.charAngle)) * 0.05 #frameRate/200
                self.charDelY = (math.cos(self.charAngle)) * 0.05 #frameRate/200
    
            if enteredKey == self.movementControls[1]:
                self.charDelX = - (math.sin(self.charAngle)) * 0.05 #frameRate/200
                self.charDelY = - (math.cos(self.charAngle)) * 0.05 #frameRate/200
    
            if enteredKey == self.movementControls[2]:
                leftAngle = self.charAngle + (math.pi/2)
                self.charDelX = (-math.sin(leftAngle)) * 0.05 #frameRate/200
                self.charDelY = (-math.cos(leftAngle)) * 0.05 #frameRate/200
    
            if enteredKey == self.movementControls[3]:
                leftAngle = self.charAngle + (math.pi/2)
                self.charDelX = (math.sin(leftAngle)) * 0.05 #frameRate/200
                self.charDelY = (math.cos(leftAngle)) * 0.05 #frameRate/200
            
            if self.moving == False:
                stepSound.play(loops=-1)
                self.moving = True
            
        
    def physicalMover(self, gameMap, pickupSound, discoverySound):
        '''
        Depending on whether the player is walking over the ground or not, moves the player by checking if the position
        is on the floor. Also handles pickups and exiting the map
        ===============Parameters===============
        gameMap (GameMap): the map object that describes the game's 2D version of the map
        pickupSound (pygame.mixer.Sound): the sound that is played when a battery is picked up
        discoverySound (pygame.mixer.Sound): the sound that is played when a key is picked up
        
        returns nothing
        '''
        wallStopperX =  math.copysign(0.1, self.charDelX)
        wallStopperY = math.copysign(0.1, self.charDelY)
        # I THINK THIS IS WHERE U PUT A TRY STATEMENT FOR WINNING
        if gameMap.mapArray[int(self.charY + self.charDelY + wallStopperY)][int(self.charX +self.charDelX + wallStopperX)] == '.' or gameMap.mapArray[int(self.charY + self.charDelY + wallStopperY)][int(self.charX +self.charDelX + wallStopperX)] == 'B' or gameMap.mapArray[int(self.charY + self.charDelY + wallStopperY)][int(self.charX +self.charDelX + wallStopperX)] == 'K' and not self.hiding:
            if gameMap.mapArray[int(self.charY + self.charDelY + wallStopperY)][int(self.charX +self.charDelX + wallStopperX)] == 'B':
                gameMap.removeChar((int(self.charX +self.charDelX + wallStopperX),int(self.charY + self.charDelY + wallStopperY)))
                if self.flashlight.batteries.power <= 60:
                    self.flashlight.batteries.power += 30
                else:
                    self.flashlight.batteries.power = 90
                pickupSound.play()
            elif gameMap.mapArray[int(self.charY + self.charDelY + wallStopperY)][int(self.charX +self.charDelX + wallStopperX)] == 'K':
                self.keyFlag = True
                gameMap.removeChar((int(self.charX +self.charDelX + wallStopperX),int(self.charY + self.charDelY + wallStopperY)))
                gameMap.removeChar(gameMap.exitCoord)
                discoverySound.play()
            
            elif int(self.charX +self.charDelX) == gameMap.exitCoord[0] and int(self.charY + self.charDelY) == gameMap.exitCoord[1]:
                self.winning = 1
    
                 
            
            self.charX += self.charDelX
            self.charY += self.charDelY

    def stopPhysicalMovement(self, enteredKey, stepSound):
        '''
        Stops player movement by testing if the raised key is one of the movementControls
        ===============Parameters===============
        enteredKey (pygame.Key): the raised key
        stepSound (pygame.mixer.Sound): the sound that must be stopped if the player is no longer moving
        
        returns nothing
        '''
        if enteredKey in self.movementControls:
            self.charDelX = 0.0
            self.charDelY = 0.0
            self.moving = False
            stepSound.stop()
    
    def perspectiveMovementCalculation(self, enteredKey):
        '''
        Calculates the player's angle movement depending on their control scheme
        if keys, simply checks pressed keys and adjusts change in angle appropriately
        if mouse, checks if mouse is to the left or right of the original mouse position
        ===============Parameters===============
        enteredKey (pygame.key/None): the pressed key detected by pygame (given None if control scheme uses mouse)
        
        returns nothing
        '''
        if not self.mouseFlag:
            if enteredKey == pg.K_LEFT:
                self.charDelAngle = -0.03 #* frameRate*1.5
            elif enteredKey == pg.K_RIGHT:
                self.charDelAngle = 0.03 #* frameRate*1.5
        else:
            if pg.mouse.get_focused():
                if pg.mouse.get_pos()[0] < self.initialPos[0]:
                    self.charDelAngle = -0.03 #* frameRate *1.5
                    
                elif pg.mouse.get_pos()[0] > self.initialPos[0]:
                    self.charDelAngle = 0.03#* frameRate*1.5
                    
                elif self.charDelAngle != 0:
                    self.charDelAngle = 0

    def perspectiveMover(self):
        '''
        Moves the player's angle according to the calculated difference in angle positions
        ===============Parameters===============
        ------------------NONE------------------
        
        returns nothing
        '''
        if not self.hiding:
            self.charAngle += self.charDelAngle
    
    def perspectiveStop(self, enteredKey):
        '''
        Stops the angle movement if the player's released key is the correct key
        ===============Parameters===============
        enteredKey (pygame.key): the released key detected by pygame
        
        returns nothing
        '''
        if (self.charDelAngle < 0 and enteredKey == pg.K_LEFT) or (self.charDelAngle > 0 and enteredKey == pg.K_RIGHT):
            self.charDelAngle = 0
            
    def flashlightSwitch(self, enteredKey):
        '''
        Begins the flashlight's switching process
        ===============Parameters===============
        enteredKey (pygame.key): the key that determines if the player wants to switch the flashlight's status
        
        returns nothing
        '''
        if enteredKey == pg.K_f and self.flashlight.batteries.power > 0 and not self.hiding:
            self.flashlight.switching[0] = True
            self.flashlight.frame = 0
            
    def hideSwitch(self, enteredKey, window, clock, texturesToLoad, gameMap, enemy, UIDict, flashlightSound, stepSound, rayIncrementor, fog, fog_level, fog_rect):
        '''
        Begins the player's hiding process if the player presses 'h'
        ===============Parameters===============
        enteredKey (pygame.key): the key that determines if the player wants to hide
        window (pygame.display): the window to draw the hiding process to
        clock (pygame.clock): the clock that spaces out how the blinking is drawn
        texturesToLoad (Dict[string:pygame.image): the dictionary that determines which image to draw
        gameMap (Map): the map object that determines where the player walks and where other objects are
        enemy (ShadowMonster): the enemy object that determines the actions it should take
        UIDict (Dict[string:pygame.image]): the dictionary that determines which images in the players information display to draw
        flashlightSound (pygame.mixer.Sound): the sound played when the flashlight is switched, only used in the hide function when calling the flashlightControl function
        stepSound (pygame.mixer.Sound): the sound played when the player is stepping
        rayIncrementor (float): the value determining how much the ray is extended before its checked, used in hide function in renderPlayerView function
        fog (pygame.image): the image that overlays the player's vision if the monster is using fog as a move
        fog_level (int): the integer that determines the opacity of the fog image
        fog_rect (pygame.Rect): the rectangle that determines the size and position of the fog image
        
        returns int
        '''
        if enteredKey == pg.K_h:
            fog_level = self.hide(window, clock, texturesToLoad, gameMap, enemy, UIDict, flashlightSound, stepSound, rayIncrementor, fog, fog_level, fog_rect)
        
        return fog_level
    def flashlightControl(self, window, shadow, switchSound):
        '''
        Draws the flashlight to the screen depending on if it's switching position or on and being used. If the player has run out of battery, force the flashlight away and
        indicate player loss
        ===============Parameters===============
        window (pygame.display): the window to draw the flashlight's position to 
        shadow (ShadowMonster): shadow monster object used for the deplete function
        switchSound (pygame.mixer.Sound): the sound played when the flashlight is turned off
        
        returns nothing
        '''
        if self.flashlight.frame < 12:
            self.flashlight.drawChanges(window,switchSound)

        if self.flashlight.onStatus and not self.flashlight.switching[0] and not self.hiding:
            self.flashlight.drawStableState(window)
        
        self.flashlight.batteries.deplete(self.flashlight.onStatus, shadow)
        
        if self.flashlight.batteries.power <= 0:
            if self.flashlight.onStatus and not self.flashlight.switching[0] and not self.hiding:
                self.flashlight.switching[0] = True
                self.flashlight.frame = 0
            self.winning = 0    
          
    def renderPlayerView(self, gameMap, groundChar, wallChars, texturesToLoad, shadow, rayIncrementor):
        '''
        Renders the player's view according to whether their flashlight is on or not
        if on, render 10/16 of the screen as if the flashlight were off (rendering distance is low) and 3/8 of the screen with an extended rendering distance
        if off, render the whole screen with low rendering distance
        after that, render any objects the rays hit
        ===============Parameters===============
        gameMap (GameMap): the map object, with an array that is used to determine whether a ray is hitting anything or not
        groundChar (char): the character that indicates a position is the ground
        wallChar (char): the character that indicates a position is the wall
        texturesToLoad (Dict[string:pygame.image]): the dictionary that determines which image to use
        shadow (ShadowMonster): the monster object used to determine if a hallucination has been shone away or not
        rayIncrementor (float): the number used to determine how far a ray is extended before it's checked for collision      
        
        returns nothing
        '''
        nonFlashlightSections = self.flashlightScreenDivision * 5
        flashlightSection = nonFlashlightSections + (self.flashlightScreenDivision*6)
        rayHitsList = []
        if self.flashlight.onStatus:
            for horizontalScreenPixel in range(0, (nonFlashlightSections + 1), self.playerCam.screenIterator):
                currentRayAngle = (self.charAngle - (self.playerCam.fov/2)) + ((horizontalScreenPixel/self.playerCam.screenWidth) * self.playerCam.fov)
                extendedRay = FLASH_rendering.Ray(self.charX, self.charY, currentRayAngle, rayIncrementor)
                extendedRay.rayCast(gameMap, groundChar, wallChars, self.renderingDistance)
                if extendedRay.objectsHit !=[]:
                    rayHitsList.append([extendedRay, horizontalScreenPixel, False])
                self.playerCam.renderWalls(extendedRay, self.renderingDistance, horizontalScreenPixel, texturesToLoad, self.charY, self.flashlight.onStatus, self.flashlightRenderingDistance)
            
            for horizontalScreenPixel in range(nonFlashlightSections, (flashlightSection + 1), self.playerCam.screenIterator):
                currentRayAngle = (self.charAngle - (self.playerCam.fov/2)) + ((horizontalScreenPixel/self.playerCam.screenWidth) * self.playerCam.fov)
                extendedRay = FLASH_rendering.Ray(self.charX, self.charY, currentRayAngle, rayIncrementor)
                extendedRay.rayCast(gameMap, groundChar, wallChars, self.flashlightRenderingDistance)
                if extendedRay.objectsHit !=[]:
                    rayHitsList.append([extendedRay, horizontalScreenPixel, self.flashlight.onStatus])
                self.playerCam.renderWalls(extendedRay, self.flashlightRenderingDistance, horizontalScreenPixel, texturesToLoad, self.charY, self.flashlight.onStatus, self.flashlightRenderingDistance)
            
            for horizontalScreenPixel in range(flashlightSection, (flashlightSection + nonFlashlightSections + 1), self.playerCam.screenIterator):
                currentRayAngle = (self.charAngle - (self.playerCam.fov/2)) + ((horizontalScreenPixel/self.playerCam.screenWidth) * self.playerCam.fov)
                extendedRay = FLASH_rendering.Ray(self.charX, self.charY, currentRayAngle, rayIncrementor)
                extendedRay.rayCast(gameMap, groundChar, wallChars, self.renderingDistance)
                if extendedRay.objectsHit !=[]:
                    rayHitsList.append([extendedRay, horizontalScreenPixel, False])
                self.playerCam.renderWalls(extendedRay, self.renderingDistance, horizontalScreenPixel, texturesToLoad, self.charY, self.flashlight.onStatus, self.flashlightRenderingDistance)
            
        else:
            for horizontalScreenPixel in range(0, self.playerCam.screenWidth + 1, self.playerCam.screenIterator):
                currentRayAngle = (self.charAngle - (self.playerCam.fov/2)) + ((horizontalScreenPixel/self.playerCam.screenWidth) * self.playerCam.fov)
                extendedRay = FLASH_rendering.Ray(self.charX, self.charY, currentRayAngle, rayIncrementor)
                extendedRay.rayCast(gameMap, groundChar, wallChars, self.renderingDistance)
                if extendedRay.objectsHit !=[]:
                    rayHitsList.append([extendedRay, horizontalScreenPixel, self.flashlight.onStatus])
                self.playerCam.renderWalls(extendedRay, self.renderingDistance, horizontalScreenPixel, texturesToLoad, self.charY, self.flashlight.onStatus, self.flashlightRenderingDistance)
        
        for rayData in rayHitsList:
            if rayData[2]:
                self.playerCam.renderMapElements(rayData[0], texturesToLoad, self.flashlightRenderingDistance, self.flashlightRenderingDistance, rayData[1], gameMap, shadow)
            else:
                self.playerCam.renderMapElements(rayData[0], texturesToLoad, self.renderingDistance, self.flashlightRenderingDistance, rayData[1], gameMap, shadow)
        
    def hide(self, window, clock, texturesToLoad, gameMap, shadow, UIDict, flashlightSound, stepSound, rayIncrementor, fog, fog_level, fog_rect):
        '''
        Closes the players 'eyes' by extending two black rectangles down or up depending on what the player wants, (also must draw the view again when opening eyes)
        making the player invisible to the enemy upon pressing 'h'
        ===============Parameters===============
        most of these parameters are used for the drawing functions, the ones not used for
        drawing functions will be explained:
        clock (pygame.time.Clock): Measures internal framerate and the speed at which screen is covered.
        shadow (ShadowMonster): used to change the monster's behaviour if the player is hiding
        UIDict (Dict[string:pygame.image]): the dictionary used to draw the parts of the screen that are there for user information
        flashlightSound (pygame.mixer.Sound): the sound played when the flashlight is switched
        stepSound (pygame.mixer.Sound): the sound played when the player is moving
        fog (pygame.image): the image that overlays the player's vision if the monster is using fog as a move
        fog_level (int): the integer that determines the opacity of the fog image
        fog_rect (pygame.Rect): the rectangle that determines the size and position of the fog image
        
        returns int
        '''
        if not self.hiding:
            if shadow.spook == True:
                shadow.spook = False
            self.moving = False
            self.stopPhysicalMovement(pg.K_w, stepSound)
            while self.bLid.top > 300:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                clock.tick(90)
                self.flashlightControl(window, shadow, flashlightSound)
                pg.draw.rect(window, (0, 0, 0), self.bLid)
                pg.draw.rect(window, (0, 0, 0), self.tLid)
                self.flashlight.batteries.drawBatteryLevel(window, UIDict)
                if self.keyFlag:
                    window.blit(UIDict['key'], (window.get_width() - UIDict['key'].get_width(), 0))
                self.bLid.top -= 4
                self.tLid.top += 4
                pg.display.update()
            self.hiding = True
        elif self.hiding == True:
            self.hiding = False
            while self.bLid.top < 600:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                clock.tick(90)
                window.fill((0, 0, 0))
                self.renderPlayerView(gameMap, '.', ['#','E'], texturesToLoad, shadow, rayIncrementor)
                if shadow.fog == True:
                    if fog_level <= 150:
                        fog_level += 1
                elif not shadow.fog:
                    if fog_level > 0:
                        fog_level -= 1
                fog.set_alpha(fog_level)
                window.blit(fog, fog_rect)
                self.flashlightControl(window, shadow, flashlightSound)
                pg.draw.rect(window, (0, 0, 0), self.bLid)
                pg.draw.rect(window, (0, 0, 0), self.tLid)
                self.flashlight.batteries.drawBatteryLevel(window, UIDict)
                if self.keyFlag:
                    window.blit(UIDict['key'], (window.get_width() - UIDict['key'].get_width(), 0))
                self.bLid.top += 4
                self.tLid.top -= 4
                pg.display.update()
        
        return fog_level

    def loss(self, clock, window, gameMap, groundChar, wallChars, texturesToLoad, UIDict, cutscene, shadow, overScreen, overSound, jumpscareSound, swoosh, rayIncrementor):
        '''
        Shows the player a loss sequence after they meet one of the appropriate conditions
        Begin by fading the screen to black
        Play a cutscene sequence, then have a random delay before the final jumpscare
        Display the loss image before returning to menu
        ===============Parameters===============
        clock (pygame.time.Clock): Measures internal framerate and the speed at which screen is covered.
        window (pygame.display): the display the whole sequence is drawn to
        gameMap (GameMap): map object used to render the map from the player perspective
        groundChar (char): character used for rendering
        wallChars (List[char]): characters used for rendering
        texturesToLoad (Dict[string:pygame.image): the dictionary used to draw the various textures that must be rendered
        UIDict (Dict[string:pygame.image]): the dictionary used to draw the parts of the screen that are there for user information
        cutscene (List[string]): the list of image names that describe the cutscene that will be rendered
        shadow (ShadowMonster): monster object used in the render player view, but not really required in this instance, as stopping hallucinations before the player loses is pointless
        overScreen (pygame.image): the image that displays the player's loss with art
        overSound (pygame.mixer.Sound): the sound played when the overScreen image is shown
        jumpscareSound (pygame.mixer.Sound): the sound played when the shadow monster image jumps up on the screen
        swoosh (pygame.mixer.Sound): the sound played when the shadow's hallucination move across the screen
        rayIncrementor (float): the amount the ray is extended before it's position is checked
        
        returns nothing
        '''
        startTime = pg.time.get_ticks()
        screenFill = False
        rect = pg.Surface((800,600))
        colour = pg.Color(0,0,0,255)
        rect.fill(colour)
        while not screenFill:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
            clock.tick(90)
            lossTime = pg.time.get_ticks()
            timeDiff = lossTime-startTime
            if timeDiff > 6000:
                timeDiff = 6000
            percent = timeDiff/6000
            rect.set_alpha(255*percent)
            self.renderPlayerView(gameMap, groundChar, wallChars, texturesToLoad, shadow, rayIncrementor)
            window.blit(rect, (0,0))
            if self.keyFlag:
                window.blit(UIDict['key'], (window.get_width() - UIDict['key'].get_width(), 0))
            self.flashlight.batteries.drawBatteryLevel(window, UIDict)
            pg.display.update()
            
            if timeDiff == 6000:
                screenFill = True
        window.fill((0,0,0))
        swoosh.set_volume(0.8)
        scareDelay = random.randint(3000,4500)
        for image in cutscene:
            pg.event.get()
            clock.tick(8)
            window.fill((0,0,0))
            imToLoad = pg.image.load(os.path.join(os.path.dirname('__file__'), 'FLASH_JumpScare', image)).convert_alpha()
            if image != 'FLASH_21.png' and image != 'FLASH_02.png':
                if image == 'FLASH_05.png' or  image == 'FLASH_10.png':
                    #or image == 'FLASH_13.png':
                    swoosh.play()
                elif image == 'FLASH_22.png':
                    jumpscareSound.play()
                    pg.mixer.fadeout(1500)
                window.blit(imToLoad, (0,0))
            elif image == 'FLASH_02.png':
                window.blit(imToLoad, (0,0))
                pg.display.update()
                pg.time.delay(1000)
                swoosh.play()
            else:
                window.blit(imToLoad, (0,0))
                pg.display.update()
                pg.time.delay(scareDelay)
            
            pg.display.update()
        
        pg.time.delay(3000)
        window.fill((0,0,0))
        pg.display.update()
        pg.time.delay(1000)
        overSound.play()
        secondStartTime = pg.time.get_ticks()
        secondScreenFill = False
        while not secondScreenFill:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
            clock.tick(90)
            overTime = pg.time.get_ticks()
            timeDiff = overTime-secondStartTime
            if timeDiff > 6000:
                timeDiff = 6000
            percent = timeDiff/6000
            rect.set_alpha(255 - (255*percent))
            window.blit(overScreen, (0,0))
            window.blit(rect, (0,0))
            pg.display.update()
            
            if timeDiff == 6000:
                secondScreenFill = True
        window.fill((0,0,0))
    
        pg.time.delay(3000)
        
        startTime = pg.time.get_ticks()
        screenFill = False
        rect = pg.Surface((800,600))
        colour = pg.Color(0,0,0,255)
        rect.fill(colour)
        while not screenFill:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
            clock.tick(90)
            fadeOutTime = pg.time.get_ticks()
            timeDiff = fadeOutTime-startTime
            if timeDiff > 6000:
                timeDiff = 6000
            percent = timeDiff/6000
            rect.set_alpha(255*percent)
            window.blit(overScreen,(0,0))
            window.blit(rect, (0,0))
            pg.display.update()
            
            if timeDiff == 6000:
                screenFill = True
    
    def win(self, window, clock, gameMap, groundChar, wallChars, texturesToLoad, UIDict, shadow, rayIncrementor, difficulty, winScreen):
        '''
        Shows the player a win sequence after they exit the maze
        Begin by fading the screen to black
        Display the win image with the time it took for the player to win
        Fade the screen to black before returning to main menu
        ===============Parameters===============
        window (pygame.display): the display the whole sequence is drawn to
        clock (pygame.time.Clock): Measures internal framerate and the speed at which screen is covered.
        gameMap (GameMap): map object used to render the map from the player perspective
        groundChar (char): character used for rendering
        wallChars (List[char]): characters used for rendering
        texturesToLoad (Dict[string:pygame.image): the dictionary used to draw the various textures that must be rendered
        UIDict (Dict[string:pygame.image]): the dictionary used to draw the parts of the screen that are there for user information
        shadow (ShadowMonster): monster object used in the render player view, but not really required in this instance, as stopping hallucinations before the player wins is pointless
        rayIncrementor (float): the amount the ray is extended before it's position is checked
        difficulty (string): the difficulty of the game, used for record keeping purposes in the win screen
        winScreen (pygame.image): the image that informs the player they escaped and the time they left in
        
        returns nothing
        '''
        escapeTime = (int(shadow.moveOpportunity)) / 60
        if escapeTime >= 10:
            seconds = str(escapeTime)[3:5]
            selTwo = 2
        else:
            seconds = str(escapeTime)[2:4]
            selTwo = 1
        
        seconds = int(int(seconds) * 0.6)
        if 0 <= seconds <= 9:
            seconds = str(seconds)
            seconds = '0' + seconds
        seconds = str(seconds)
        escapeTime = str(escapeTime)
        day = date.today()
        font = pg.font.SysFont(None, 60)
        file = open('FLASH_Scores.txt','a+')
        recordTimes = file.write('\nTime:' + escapeTime[0:selTwo] + ':' + seconds + ' (' + str(day) + ') (' + difficulty + ')\n')
        timeDisplay = font.render((escapeTime[0:selTwo] + ':' + seconds), True, ((255, 255, 255)), None)
        file.close()
        
        startTime = pg.time.get_ticks()
        screenFill = False
        rect = pg.Surface((800,600))
        colour = pg.Color(0,0,0,255)
        rect.fill(colour)
        while not screenFill:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
            clock.tick(90)
            winTime = pg.time.get_ticks()
            timeDiff = winTime-startTime
            if timeDiff > 6000:
                timeDiff = 6000
            percent = timeDiff/6000
            rect.set_alpha(255*percent)
            self.renderPlayerView(gameMap, groundChar, wallChars, texturesToLoad, shadow, rayIncrementor)
            if self.keyFlag:
                window.blit(UIDict['key'], (window.get_width() - UIDict['key'].get_width(), 0))
            self.flashlight.batteries.drawBatteryLevel(window, UIDict)
            window.blit(rect, (0,0))
            pg.display.update()
            
            if timeDiff == 6000:
                screenFill = True
        
        window.fill((0,0,0))
        pg.display.update()
        rect = pg.Surface((800,600))
        colour = pg.Color(0,0,0,255)
        rect.fill(colour)
        secondStartTime = pg.time.get_ticks()
        secondScreenFill = False
        while not secondScreenFill:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
            clock.tick(90)
            overTime = pg.time.get_ticks()
            timeDiff = overTime-secondStartTime
            if timeDiff > 6000:
                timeDiff = 6000
            percent = timeDiff/6000
            rect.set_alpha(255 - (255*percent))
            window.blit(winScreen, (0, 0))
            window.blit(timeDisplay,((350,270),(130,80)))
            window.blit(rect, (0,0))
            pg.display.update()
            
            if timeDiff == 6000:
                secondScreenFill = True
        
        startTime = pg.time.get_ticks()
        screenFill = False
        rect = pg.Surface((800,600))
        colour = pg.Color(0,0,0,255)
        rect.fill(colour)
        while not screenFill:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
            clock.tick(90)
            fadeOutTime = pg.time.get_ticks()
            timeDiff = fadeOutTime-startTime
            if timeDiff > 6000:
                timeDiff = 6000
            percent = timeDiff/6000
            rect.set_alpha(255*percent)
            window.blit(winScreen,(0,0))
            window.blit(timeDisplay,((350,270),(130,80)))
            window.blit(rect, (0,0))
            pg.display.update()
            
            if timeDiff == 6000:
                screenFill = True
        
        
class ShadowMonster(FLASH_inanimates.MapElement):
    '''
    Describes the enemy that hunts the player throughout the game. Inherits from the MapElement class
    
    ===============Attributes===============
    move (int): Gives the enemy an opportunity to act every 10 seconds ingame.
    fog_timer (int): Measures how long the fog will be visible to the player.
    movementStage (int): Activates chase flag when this variable is equal to a specific value.
    chase (bool): Activates when enemy appears to chase the player, if the enemy escapes, it is disabled.
    spook (bool): Activates when player action is required to ward off the enemy.
    moveChoice (string): Action that enemy will proceed with in a turn.
    movementOpportunity (int): the integer describing the current time, used to check if it's the appropriate interval to have the monster take an action
    scareChoice (string): Sub-action that enemy will proceed with in a turn when 'scare' is chosen from moveChoice.
    aiLevel (int): Sets frequency of enemy action depending on game difficulty.
    fog (bool): Activates when fog action is made by enemy, opens up new actions to enemy.
    enemyX / enemyY (int): Measures position of enemy on game map.
    '''
    def __init__(self, mapChar, difficulty):
        FLASH_inanimates.MapElement.__init__(self, mapChar)
        self.move = 10
        self.fog_timer = 0
        self.movementStage = 0
        self.moveOpportunity = 0
        self.enemyX = 100
        self.enemyY = 100
        self.chase = False
        self.spook = False
        self.fog = False
        self.scareChoice = 'none'
        self.moveChoice = 'none'
        if difficulty == 'easy':
            self.aiLevel = 10
        elif difficulty == 'normal':
            self.aiLevel = 15
        elif difficulty == 'hard':
            self.aiLevel = 20
    
    def movementGenerator(self,player,gameMap, menuTime, timePaused):
        '''
        Determines which move the monster will make. Also checks if player made an action to ward off enemy.
        ===============Parameters===============
        player (PlayerCharacter): the player object used to track if the monster is close to the player
        gameMap (GameMap): map used to add enemy in the game
        menuTime (float): the number that describes how much time was spent in the menu
        timePaused (float): the number that describes how long the game was paused for
        
        return nothing
        '''
        self.moveOpportunity = (pg.time.get_ticks() / 1000) - menuTime -timePaused
        #self.moveOpportunity = 0 #This disables ai
        if self.fog_timer == self.move:
                self.fog = False
                self.fog_timer = 0
        if (self.move - 0.06) <= self.moveOpportunity:
            self.move += 10
            if self.chase == True:
                player.winning = 0
            if self.spook == True:
                if self.scareChoice == 'hallucination':
                    self.moving(player,gameMap)
                    self.spook = False
                else:
                    player.winning = 0
            elif self.spook == False and self.scareChoice == 'fog':
                pass #this will disable the fog(?)

            chance = random.randint(0,20)
            if self.fog:
                chance -= 2
            if player.keyFlag:
                chance -= 3
            if self.aiLevel >= chance:
                self.moveChoice = random.choice(['move','drain','scare'])
                if self.moveChoice == 'move':
                    self.moving(player,gameMap)
                elif self.moveChoice == 'scare':
                    self.scare(player,gameMap)
            else:
                pass
        
    def moving(self,player,gameMap):
        '''
        Used to track if enemy will appear on the map to chase player.
        ===============Parameters===============
        player (PlayerCharacter): the player object used to track if the monster is close to the player
        gameMap (GameMap): map used to add enemy in the game
        
        returns nothing
        '''
        self.movementStage += 1
        if self.movementStage == 3:  #change to 2 for real game
            self.movementStage = 0
            self.chase = True
            if player.keyFlag:
                self.enemyY = int(player.charY - 1)
            else:
                self.enemyY = int(player.charY + 1)
            self.enemyX = int(player.charX)
            self.move += 10
            gameMap.enemyAdded(self)
            pg.mixer.music.load('FLASH_Music/FLASH_chase.ogg')
            pg.mixer.music.play(0,0.0)
    def scare(self,player, gameMap):
        '''
        Used to determine sub-action taken if moveChoice == 'scare'.
        ===============Parameters===============
        player (PlayerCharacter): the player object used to track if the monster is close to the player
        gameMap (GameMap): map used to add enemy in the game
        
        returns nothing
        '''
        self.scareChoice = random.choice(['footsteps','hallucination','fog'])
        if self.fog == True:
            self.scareChoice = random.choice(['hallucination','growl'])
        if self.scareChoice == 'footsteps':
            self.spook = True
            pg.mixer.music.load('FLASH_SoundEffects/FLASH_monsterSteps.ogg')
            pg.mixer.music.play(0, 0.0)
        elif self.scareChoice == 'growl':
            self.spook = True
            pg.mixer.music.load('FLASH_SoundEffects/FLASH_lowMonster.wav')
            pg.mixer.music.play(0,0.0)
        elif self.scareChoice == 'hallucination': #maybe add spook here
            self.spook = True
            self.enemyY = int(player.charY + (random.choice([-2,-1,1])))
            self.enemyX = int(player.charX + (random.choice([-2,-1,1])))
            if 0 < self.enemyY < gameMap.height and 0 < self.enemyX < gameMap.width:
                gameMap.enemyAdded(self)
            else:
                if player.keyFlag:
                    self.enemyY = int(player.charY - 1)
                else:
                    self.enemyY = int(player.charY + 1)
                self.enemyX = int(player.charX)
                gameMap.enemyAdded(self)
        elif self.scareChoice == 'fog':  #Idk maybe another sound thing instead just want to utilize hide mechanic.
            self.fog_timer = self.move + 20
            self.fog = True
            self.movementStage = 2
