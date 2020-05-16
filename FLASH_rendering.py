# Last Updated April 14 2020

import pygame as pg
import math

class Camera:
    '''
    Translates the  2D span of the player's view into a 3D(ish) view of the surroundings
    ===============Attributes===============
    screenWidth (int): the width (in pixels) of the screen
    screenLength (int): the length (in pixels) of the screen
    fov (float): the span of the player's view
    screenIterator (int): this is both the value iterated through the range of the screen width, and also the width of the lines drawn as a result of ray casting (same value so no spaces between lines)
    pgScreenHandle (pygame.display): the screen to which the 3D view will be drawn to
    '''
    def __init__(self, screenWidth, screenLength, fov, screenIterator, pgScreenHandle):
        self.screenWidth = screenWidth
        self.screenLength = screenLength
        self.fov = fov
        self.screenIterator = screenIterator
        self.pgScreenHandle = pgScreenHandle

    def renderWalls(self, extendedRay, renderingDistance, horizontalScreenPixel, texturesToLoad, charY, flashlightFlag, flashlightRender):
        '''
        Draws the player's perspective to the screen by segmenting the texture according to the float value of the ray and subsurfacing the appropriate dimensions from the image before drawing it.        
        ===============Parameters===============
        extendedRay (Ray()): the fully cast ray
        renderingDistance (int): the value for which the farthest ray will be cast
        horizontalScreenPixel (int): the current pixel on the x-axis that is being drawn to
        texturesToLoad (Dict[string:pygame.image]): the dictionary that determines which image to use
        charY (float): y-position of the character, used to determine which offset to use for the image. charX can be used in the same way, the choice of charY is arbitrary
        flashlightFlag (bool): The power status of the flashlight (on = True, off = False)
        flashlightRender (int): the max distance a ray in the range of the flashlight portion of the screen can be cast
        
        returns nothing
        '''
        
        if extendedRay.distanceToObstruction <= renderingDistance:
            if extendedRay.obstructionChar == '#':
                texture = texturesToLoad['wall']
                ceiling = int(self.screenLength/2 - self.screenLength/extendedRay.distanceToObstruction)
                percent = extendedRay.distanceToObstruction/ renderingDistance
                lineLength = self.screenLength - (ceiling*2)
                if(int(charY + (extendedRay.yRayUnitVector*(extendedRay.distanceToObstruction - extendedRay.rayIncrementor))) != int(extendedRay.yTestUnitVector)):
                    rayTest = extendedRay.xTestUnitVector % 1  
                else:
                    rayTest = extendedRay.yTestUnitVector % 1
                
                textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))           
                drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                drawnImage = texture.subsurface(drawnImageRect)
                scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                darkRectangle.fill((0,0,0,(255)*percent))
                self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
            elif extendedRay.obstructionChar == 'E':
                texture = texturesToLoad['exit']
                ceiling = int(self.screenLength/2 - self.screenLength/extendedRay.distanceToObstruction)
                percent = extendedRay.distanceToObstruction/ renderingDistance
                lineLength = self.screenLength - (ceiling*2)
                if(int(charY + (extendedRay.yRayUnitVector*(extendedRay.distanceToObstruction - extendedRay.rayIncrementor))) != int(extendedRay.yTestUnitVector)):
                    rayTest = extendedRay.xTestUnitVector % 1  
                else:
                    rayTest = extendedRay.yTestUnitVector % 1
                
                textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))           
                drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                drawnImage = texture.subsurface(drawnImageRect)
                scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                darkRectangle.fill((0,0,0,(255)*percent))
                self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                
        else:
            texture = texturesToLoad['far wall']
            if flashlightFlag:
                ceiling = int(self.screenLength/2 - self.screenLength/flashlightRender)
            else:
                ceiling = int(self.screenLength/2 - self.screenLength/renderingDistance)
            lineLength = self.screenLength - (ceiling*2)
            drawnImageRect = pg.Rect(0, 0, self.screenIterator, lineLength)
            drawnImage = texture.subsurface(drawnImageRect)
            scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
            self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
   
    def renderMapElements(self, extendedRay, texturesToLoad, renderingDistance, flashlightRenderingDistance, horizontalScreenPixel, gameMap, shadow):
        '''
        Renders non-wall objects in a similar way to the wall function, but using just one image that always faces the player
        This is done in the raycasting method of the ray, as the math required must be done while the ray is extending
        ===============Parameters===============
        extendedRay (Ray()): the fully cast ray, extended beyond the map element so that a background is loaded behind the object
        texturesToLoad (Dict[string:pygame.image]): the dictionary that determines which image to use
        renderingDistance (int): the maximum rendering distance of the section
        flashlightRenderingDistance (int): the maximum possible rendering distance, used to determine if the current rendering distance is the same
        horizontalScreenPixel (int): the current pixel on the x-axis that is being drawn to
        gameMap (GameMap()): the map object that is used to remove a character given a set of conditions
        shadow (ShadowMonster()): the shadow object used to determine if the player is shining away a hallucination or not
        
        return nothing
        '''
        if extendedRay.objectsHit != []:
            extendedRay.objectsHit.reverse()
            for pointData in extendedRay.objectsHit:
                if pointData[0] == 'A':
                    texture = texturesToLoad['shadow monster']
                    ceiling = int(self.screenLength/2 - self.screenLength/pointData[1])
                    percentVision = pointData[1]/renderingDistance
                    lineLength = self.screenLength - (ceiling*2)
                    rayTest = pointData[2]
                    textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))
                    drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                    drawnImage = texture.subsurface(drawnImageRect)
                    scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                    darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                    darkRectangle.fill((0,0,0,(255)*percentVision))
                    self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                    self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                elif pointData[0] == 'B':
                    texture = texturesToLoad['battery']
                    ceiling = int(self.screenLength/2 - self.screenLength/(pointData[1]*1.25))
                    percentVision = pointData[1]/renderingDistance
                    lineLength = self.screenLength - (ceiling*2)
                    rayTest = pointData[2]
                    textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))
                    drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                    drawnImage = texture.subsurface(drawnImageRect)
                    scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                    darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                    darkRectangle.fill((0,0,0,(255)*percentVision))
                    self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                    self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                elif pointData[0] == 'K':
                    texture = texturesToLoad['key']
                    ceiling = int(self.screenLength/2 - self.screenLength/(pointData[1]*1.25))
                    percentVision = pointData[1]/renderingDistance
                    lineLength = self.screenLength - (ceiling*2)
                    rayTest = pointData[2]
                    textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))
                    drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                    drawnImage = texture.subsurface(drawnImageRect)
                    scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                    darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                    darkRectangle.fill((0,0,0,(255)*percentVision))
                    self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                    self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                     
                elif pointData[0] == 'H':
                    if renderingDistance != flashlightRenderingDistance:
                        texture = texturesToLoad['hallucination']
                        ceiling = int(self.screenLength/2 - self.screenLength/pointData[1])
                        percentVision = pointData[1]/renderingDistance
                        lineLength = self.screenLength - (ceiling*2)
                        rayTest = pointData[2]
                        textureXPos = int((texture.get_width() - self.screenIterator)*(rayTest))
                        drawnImageRect = pg.Rect(textureXPos, 0, self.screenIterator, texture.get_height())
                        drawnImage = texture.subsurface(drawnImageRect)
                        scaledImage = pg.transform.scale(drawnImage, (self.screenIterator, lineLength))
                        darkRectangle = pg.Surface((self.screenIterator,lineLength)).convert_alpha()
                        darkRectangle.fill((0,0,0,(255)*percentVision))
                        self.pgScreenHandle.blit(scaledImage, (horizontalScreenPixel, ceiling))
                        self.pgScreenHandle.blit(darkRectangle, (horizontalScreenPixel, ceiling))
                    else:
                        gameMap.removeChar(pointData[3])
                        shadow.spook = False


class Ray:
    '''
    Describes the a ray extending from some origin to some point
    ===============Attributes===============
    originX (int): x-coord for where ray comes from on a 2D map
    originY (int): y-coord for where ray comes from on a 2D map
    rayA (float): the value for the angle of the ray in radians
    xRayUnitVector (float): uses angle of the ray to find a unit vector for the x-axis
    yRayUnitVector (float): uses angle of the ray to find a unit vector for the y-axis
    distanceToObstruction (float): distance from the origin to a object blocking origins ray
    rayIncrementor (float): the amount describing the increment of the unit vector the ray will be extended
    objectsHit (List[char,float,float,Tuple[int]): the list of objects the current ray has hit so far with other information, like the distance before the first hit, the percentage of the line on the unit circle in the tile the ray is at, and the integer coordinates of the tile
    obstructionHit (bool): flag for whether ray has hit something
    '''
    def __init__(self, originX, originY, rayA, rayIncrementor):
        self.originX = originX
        self.originY = originY
        self.rayA = rayA
        self.xRayUnitVector = math.sin(rayA)
        self.yRayUnitVector = math.cos(rayA)
        self.distanceToObstruction = 0.0
        self.rayIncrementor = rayIncrementor# <---- adjust this to increase quality of walls
        self.objectsHit = []
        self.obstructionHit = False

    def rayCast(self, gameMap, groundChar, wallChars, renderingDistance):
        '''
        Casts ray from origin to the obstruction by incrementing ray till something is 'hit'
        Hit occurs if the ray's current point is not in the ground on the array representation of the map
        If a hit is on an object (battery, monster, etc.), the point must be in the further half of a circle within the tile the player is looking at. The point is then recorded so it isn't reiterated, and the ray is extended until a wall is hit
        The point the ray has hit is recorded and the distance to that point is recorded
        ===============Parameters===============
        gameMap (GameMap()): the map object that describes the 2D version of the map
        groundChar (char): character that indicates the ground, so the ray can pass over without considering it an obstruction
        wallChars (List[char]): characters that indicates a wall, so the ray can stop
        renderingDistance (int): maximum range of origin's ray casting extent
        
        returns nothing
        '''
        self.distanceToObstruction = 0.000001
        while (not self.obstructionHit) and (self.distanceToObstruction < renderingDistance):
            self.distanceToObstruction += self.rayIncrementor 
            self.xTestUnitVector = self.originX + (self.xRayUnitVector * self.distanceToObstruction)
            self.yTestUnitVector = self.originY + (self.yRayUnitVector * self.distanceToObstruction)
            if 0 <= self.xTestUnitVector <= (gameMap.width) and 0 <= self.yTestUnitVector <= (gameMap.height):
                if gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)] != groundChar:
                    if not gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)] in wallChars:
                        objectHitAlready = False
                        for hitInstances in self.objectsHit:
                            if hitInstances[0] == gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)]:
                                objectHitAlready = True
                                break
                        if not objectHitAlready:
                            # We move to a unit circle, I think this should be easier, rectangle will look weird and requires math too advanced for my point in time
                            try:
                                centerPoint = (int(self.xTestUnitVector)+0.5,int(self.yTestUnitVector)+0.5)
                                playerXDiff = centerPoint[0] - self.originX
                                playerYDiff = centerPoint[1] - self.originY
                                playerPerspectiveSlope = playerYDiff/playerXDiff
                                objLineSlope = -1/playerPerspectiveSlope
                                if abs(objLineSlope) > 1000000000:
                                    playerPerspectiveSlope = 0
                                    raise ZeroDivisionError
                                yOffset = centerPoint[1]- (centerPoint[0]*objLineSlope)
                                a = 1 + (objLineSlope**2)
                                b = 2*(-centerPoint[0]) + 2*objLineSlope*(yOffset -centerPoint[1])
                                c = (centerPoint[0]**2) + ((yOffset-centerPoint[1])**2) -0.25
                                #NOT BAD VARIABLE NAMES BECAUSE THIS IS LITERALLY THE QUADRATIC EQUATION
                                circleObjXIntersect1 = (-b + (((b**2) - (4*a*c))**0.5))/(2*a)
                                circleObjYIntersect1 = (circleObjXIntersect1*objLineSlope) + yOffset
                                circleObjXIntersect2 = (-b - (((b**2) - (4*a*c))**0.5))/(2*a)
                                circleObjYIntersect2 = (circleObjXIntersect2*objLineSlope) + yOffset
                                dVal = ((self.xTestUnitVector - circleObjXIntersect1)*(circleObjYIntersect2 - circleObjYIntersect1)) - ((self.yTestUnitVector - circleObjYIntersect1)*(circleObjXIntersect2 - circleObjXIntersect1))
                                if (dVal >= 0 and self.originY <= centerPoint[1]) or (dVal <= 0  and self.originY >= centerPoint[1]):
                                    circleCheck = ((self.xTestUnitVector - centerPoint[0])**2) + ((self.yTestUnitVector - centerPoint[1])**2)
                                    if circleCheck < 0.25:
                                        pointInFlag = True
                                    else:
                                        pointInFlag = False
                                else:
                                    pointInFlag = False
                                #===================================================
                                # crossProd = (xIntersect1*yIntersect2) - (yIntersect1*xIntersect2)
                                # distanceFromCenterToVector = ((self.xTestUnitVector -(int(self.xTestUnitVector)+0.5))**2) + ((self.yTestUnitVector -(int(self.yTestUnitVector)+0.5))**2)
                                # pointInFlag = crossProd >= 0 and distanceFromCenterToVector <= 0.25
                                #===================================================
                            except ZeroDivisionError:
                                if (self.originX < centerPoint[0] < self.xTestUnitVector) or (self.xTestUnitVector < centerPoint[0] < self.originX):
                                    circleCheck = ((self.xTestUnitVector - centerPoint[0])**2) + ((self.yTestUnitVector - centerPoint[1])**2)
                                    if circleCheck < 0.25:
                                        pointInFlag = True
                                    else:
                                        pointInFlag = False
                                else:
                                    pointInFlag = True
                            
                            
                        if not objectHitAlready and self.distanceToObstruction < renderingDistance and pointInFlag: #and (initialSpriteLevelX <= self.xTestUnitVector <= finalSpriteLevelX) and (initialSpriteLevelY <= self.yTestUnitVector <= finalSpriteLevelY):
                            #===================================================
                            # print((self.xTestUnitVector,self.yTestUnitVector))
                            # print('y = ' + str(objLineSlope)+ 'x + ' + str(yOffset))
                            # print('(x-' + str(centerPoint[0]) + ')^2 + (y-' + str(centerPoint[1]) + ')^2 = 0.25')
                            # print((circleObjXIntersect1,circleObjYIntersect1))
                            # print((circleObjXIntersect2,circleObjYIntersect2))
                            # print('vec: ' + str(self.xTestUnitVector))
                            # print('orig: '+ str(self.originX))
                            # print((self.xTestUnitVector - self.originX))
                            #===================================================
                            if playerPerspectiveSlope != 0:
                                try: 
                                    rayIntersectSlope = (self.yTestUnitVector - self.originY)/(self.xTestUnitVector - self.originX)
                                    yRayOffset = self.originY - (rayIntersectSlope*self.originX)
                                    intersectedX = (yOffset - yRayOffset)/(rayIntersectSlope - objLineSlope)
                                except ZeroDivisionError:
                                    intersectedX = self.originX
                                
                                if self.xTestUnitVector - self.originX != 0:
                                    intersectedY = (rayIntersectSlope*intersectedX) + yRayOffset
                                #===================================================
                                # print('first intersect: ' + str(((circleObjXIntersect1, circleObjYIntersect1))))
                                # print('second intersect: ' + str(((circleObjXIntersect2, circleObjYIntersect2))))
                                #===================================================
                                
                                try:
                                    percentageOfLine =  (intersectedX - circleObjXIntersect1)/(circleObjXIntersect2 - circleObjXIntersect1)
                                except ZeroDivisionError:
                                    percentageOfLine = (intersectedY - circleObjYIntersect1)/(circleObjYIntersect2 - circleObjYIntersect1)
                            
                            elif playerPerspectiveSlope == 0:
                                rayIntersectSlope = (self.yTestUnitVector - self.originY)/(self.xTestUnitVector - self.originX)
                                yRayOffset = self.originY - (rayIntersectSlope*self.originX)
                                yIntersected = (rayIntersectSlope*centerPoint[0]) + yRayOffset
                                if int(centerPoint[1]) <= yIntersected <= (int(centerPoint[1])+1):
                                    percentageOfLine =  yIntersected % 1
                                else:
                                    percentageOfLine = 0
                            
                            pointData = [gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)], self.distanceToObstruction, percentageOfLine]
                            if gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)] == 'H':
                                pointData.append((int(self.xTestUnitVector),int(self.yTestUnitVector)))
                            self.objectsHit.append(pointData)
                    else:
                        self.obstructionHit =  True
            else:
                self.obstructionHit = True
                self.distanceToObstruction = renderingDistance

        if self.distanceToObstruction >= renderingDistance:
            self.distanceToObstruction += 1
        else:
            self.obstructionChar = gameMap.mapArray[int(self.yTestUnitVector)][int(self.xTestUnitVector)]
