#Last updated April 14 2020
import pygame as pg
import FLASH_primarySettings as ps
import random

class GameMap:
    '''
    Map of the game, used for accessing width, height, and map generator function
    ===============Attributes===============
    width (int): the number of columns in the map
    height (int): the number of rows in the map
    mapArray(List[List[char]]): the list of characters that describes the map the player is on
    exitCoord (Tuple(int)): the x and y integer for the location of the exit
    '''
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.mapArray = self.generateMap(difficulty)
        rowCounter = 0
#===============================================================================
#         self.mapArray = [
# ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
# ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
# ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'], 
# ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'], 
# ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
# ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'], 
# ['#', '.', '.', '.', '.', '.', '#', '#', '#', '#', '.', '.', '.', '.', '.', '#'],
# ['#', '.', '.', '.', '.', '.', '#', '#', '#', '#', '.', '.', '.', '.', '.', '#'],
# ['#', '.', '.', '.', '.', '.', '#', '#', '#', '#', '.', '.', '.', '.', '.', '#'],
# ['E', '.', '.', '.', '.', 'B', '#', '#', '#', '#', '.', '.', '.', '.', '.', '#'],
# ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
# ['#', '.', '.', '.', '.', 'K', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
# ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
# ['#', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
# ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]
#===============================================================================
        for row in self.mapArray:
            columnCounter = 0
            for column in row:
                if column == 'E':
                    self.exitCoord = (columnCounter, rowCounter)
                columnCounter += 1
            
            rowCounter += 1
             
        self.width = len(self.mapArray[0])
        self.height = len(self.mapArray)
    
    
    def randString(self):
        '''
        This creates a random string using a specific set of letters
        ===============Parameters===============
        ------------------NONE------------------
        
        returns string
        '''
        letters = '#.'
        newwall = ''
        for i in range(self.width):
            newwall += (random.choice(letters))
        return newwall

    def newWall(self):
        '''
        This determines what all the variables for the new walls are
        ===============Parameters===============
        ------------------NONE------------------
        
        returns string
        '''
        wallStart = '#'
        wallEnd = '#'
        wallMiddle = self.randString()
        finalWall = wallStart + wallMiddle + wallEnd
        return finalWall


    def generateMap(self, difficultySelect):
        '''
        This is what actually makes the random map.
        ===============Parameters===============
        difficultySelect (string): the string describing how many batteries should be in the map
        
        returns List[List[char]]
        '''

        if difficultySelect == 'easy':
            mapDivider = 6
        elif difficultySelect == 'normal':
            mapDivider = 4
        elif difficultySelect == 'hard':
            mapDivider = 2

        gamemap = []
        keyPlace = random.randint(0, self.width - 1)
        keyLine = '#'
        for generation in range(self.width):
            if generation == keyPlace:
                keyLine += 'K'
            else:
                keyLine += '.'
        keyLine += '#'
        for i in range(self.height):
            #top wall of just (###############)
            topWall = "#" + '#' *self.width + '#'
            #empty walls (#...............#)
            emptyWalls = "#" + "." *self.width + '#'

            endWall = "#" + '#' *self.width + '#'
            exitSpot = random.randint(0,2)
            if exitSpot == 1:
                exitLine = "E" + "." * self.width + "#"
            else:
                exitLine = "#" + "." * self.width + "E"
    
            addedWall = self.newWall()
            if addedWall == ("#" + '#' *self.width + '#'):
                addedWall = emptyWalls
            gamemap.append(addedWall)
            gamemap.append(emptyWalls)
            
        
        gamemap.insert(0, topWall)
        gamemap.insert(1,emptyWalls)
        gamemap.insert(1,emptyWalls)
        gamemap.append(endWall)
        gamemap.append(endWall)
        exitSpot = random.randint(1,3)
        gamemap.insert(exitSpot, exitLine)
        gamemap.insert(0, topWall)
        
        
        gamemap.insert(-2, keyLine)
        
        rowIterator = 0
        for row in gamemap:
            gamemap[rowIterator] = list(row)
            rowIterator += 1

        section = (self.height * 2) / mapDivider
        nextSection = 1
        tempSection = section
        for batteryPlacement in range(1,mapDivider + 1):
            batteryPlace = random.randint(1, self.width - 2)
            lineChosen = random.randint(int(nextSection),int(tempSection))
            if gamemap[lineChosen][batteryPlace] == 'K':
                gamemap[lineChosen-1][batteryPlace] = 'B'
            else:
                gamemap[lineChosen][batteryPlace] = 'B'
            nextSection += section
            tempSection = section * (batteryPlacement + 1)

        return gamemap
    
    def printMap(self):
        '''
        Function purely for programming use, so the map can be visualised easily
        ===============Parameters===============
        ------------------NONE------------------
        returns nothing
        '''
        for row in self.mapArray:
            print(row)
    
    def removeChar(self, coordinates):
        '''
        Replaces a character on the map with the character describing the map's floor
        ===============Parameters===============
        coordinates (Tuple[int]): the 2 integers that describe the part of the map to remove
        
        returns nothing
        '''
        self.mapArray[coordinates[1]][coordinates[0]] = '.'
    
    def enemyAdded(self,shadow):
        '''
        Adds either a hallucination sprite or monster sprite to the game map.
        ===============Parameters===============
        shadow(shadowMonster()): Used to acquire enemy location to place sprite
        
        returns nothing
        '''
        if shadow.scareChoice == 'hallucination':
            if self.mapArray[shadow.enemyY][shadow.enemyX] == 'B' or self.mapArray[shadow.enemyY][shadow.enemyX] == 'K':
                self.mapArray[shadow.enemyY][shadow.enemyX + 1] = 'H'
            else:
                self.mapArray[shadow.enemyY][shadow.enemyX] = 'H'
        if shadow.chase == True and self.mapArray[shadow.enemyY][shadow.enemyX] != 'K':
            self.mapArray[shadow.enemyY][shadow.enemyX] = 'A'
        elif shadow.chase == True and self.mapArray[shadow.enemyY][shadow.enemyX] == 'K':
            self.mapArray[shadow.enemyY][shadow.enemyX + 1] = 'A'

class MapElement:
    '''
    Describes general attributes between elements on the map, more so used for inheriting than direct instancing
    ===============Attributes===============
    mapChar (char): the character on the map that indicates which map element it is
    '''
    def __init__(self, mapChar):
        self.mapChar = mapChar


class Flashlight:
    '''
    Object that describes the physical image of the flashlight, as well whether its on or off, and its battery level
    ===============Attributes===============
    onStatus (bool): flag for whether the flashlight is off or on
    switching (List[bool]): list of 2 booleans, first determines whether the flashlight is in the process of switching, second is what it is switching to
    frame (int): the current frame the flashlight is on in terms of its transition
    onImages (List(pygame.image]): a list of images in order to make the flashlight look like it's being pulled out and turned on
    offImages (List(pygame.image]): a reversed version of onImages
    rect (pygame.Rect()): a rectangle describing the image sizes of the flashlight, and a position in the bottom right of the screen
    batteries (Battery()): the battery object that describes how much time the flashlight has left to be used
    '''
    def __init__(self, flashlightFlag, batteryMapChar):
        self.onStatus = flashlightFlag
        self.switching = [False, not flashlightFlag]
        if flashlightFlag:
            self.frame = 0
        else:
            self.frame = 12
        self.onImages = [ps.flashlightHalf, ps.flashlightOff, ps.flashlightOn]
        self.offImages = self.onImages[::-1]
        self.rect = self.onImages[0].get_rect()
        self.rect.x = ps.windowWidth - self.onImages[0].get_width()
        self.rect.y = ps.windowHeight - self.onImages[0].get_height()
        self.batteries = Battery(batteryMapChar)
        
    def drawChanges(self, window, switchSound):
        '''
        Drawing function that draws images as long as the flashlight is switching modes, and changes the status of the flashlight at the appropriate time
        ===============Parameters===============
        window (pygame.display): window the changes are being drawn to
        switchSound (pygame.mixer.Sound): the sound played when the flashlight status is switched
        
        returns nothing
        '''
        if self.switching[0] and self.switching[1] == True and self.frame < 12:
            window.blit(self.onImages[(self.frame//4)], self.rect)
            self.frame +=1
        elif self.switching[0] and self.switching[1] == False and self.frame < 12:
            if self.frame == 4:
                self.onStatus = False
                switchSound.play()
            window.blit(self.offImages[(self.frame//4)], self.rect)
            self.frame +=1
        
        if self.frame == 12:
            if self.switching[1]:
                self.onStatus = True
                switchSound.play()
            self.switching[0] = False
            self.switching[1] = not self.switching[1]
            
    def drawStableState(self, window):
        '''
        Drawing function only occurring when the flashlight is on and not transitioning
        ===============Parameters===============
        window (pygame.display): the window the on image is being drawn to
        
        returns nothing
        '''
        window.blit(self.onImages[2], self.rect)


class Battery(MapElement):
    '''
    Describes how long the flashlight can be used for and what to draw to the screen
    ===============Attributes===============
    power (int): the integer describing the number of seconds the battery can be used for
    drain (int): Allows battery to be able to drain every second it's on
    batRect (pygame.Rect): the rectangle on the screen that describes where the battery status icons should be drawn
    offTime (None/int): Separate timer that tracks the time the flashlight is off so as to not drain battery life during that time
    usage (None/int): Main timer that tracks timer the flashlight is on, actively draining the battery every second.
    '''
    def __init__(self, mapChar):
        MapElement.__init__(self, mapChar)
        self.power = 90
        self.drain = 1
        self.batRect = pg.Rect(10,10,100,50)
        self.offTime = None
        self.usage = None

    def deplete(self, flashLightStatus, shadow):
        '''
        Drains battery life, whether from active usage or enemy tampering.
        ===============Parameters===============
        flashlightStatus (bool): flag for testing if flashlight's battery should be reduced or not
        shadow (ShadowMonster()): shadow monster object used to test if extra power should be taken away from the player
        
        returns nothing
        '''
        if shadow.moveChoice == 'drain':
            self.power -= 10
            shadow.moveChoice = 'none'
            pg.mixer.music.load('FLASH_SoundEffects/FLASH_shock.wav')
            pg.mixer.music.play(0,0.0)

        if flashLightStatus:
            self.usage = (pg.time.get_ticks() / 1000) - self.off_time
            if (self.usage - 0.06) <= self.drain <= (self.usage + 0.06):
                self.power -= 1
                self.drain += 1
        
        if not flashLightStatus:
            self.drain = 1
            self.off_time = pg.time.get_ticks() / 1000
        
    def drawBatteryLevel(self, window, UIDict):
        '''
        Displays current battery life on the screen.
        ===============Parameters===============
        window (pygame.display): the display the battery image should be drawn to
        UIDict (Dict[string:pygame.image): the image to be displayed depending on battery level
        
        returns nothing
        '''
        if self.power <= 0:
            window.blit(UIDict['zero'], self.batRect)
        elif 1 <= self.power <= 30:
            window.blit(UIDict['low'], self.batRect)
        elif 31 <= self.power <= 60:
            window.blit(UIDict['med'], self.batRect)
        elif 61 <= self.power <= 90:
            window.blit(UIDict['full'], self.batRect) 

        
