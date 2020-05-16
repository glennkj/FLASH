#Last updated April 14, 2020
import pygame as pg
import sys
import FLASH_primarySettings as ps

# A class for the buttons in the menu.
# Adapted from https://gist.githubusercontent.com/ohsqueezy/2802185/raw/a6b503e7f917a94b6b0042e9480ce09f730526f1/pygame-menu-mouseover.py
class Option:
    # States whether or not the cursor is hovered over the button
    mouseOver = False

    # Takes in the button image, highlighted image, its position and dimensions
    def __init__(self, img1, img2, position, dimensions, window):
        # States a rect for the button
        self.rect = pg.Rect(position[0], position[1], dimensions[0], dimensions[1])
        self.img1 = img1
        self.img2 = img2
        self.dimensions = dimensions
        self.position = position
        self.highlight()
        self.display(window)
    # Changes the button's images whether or not the cursor is over the button
    def highlight(self):
        if self.mouseOver == True:
            return(self.img2)
        else:
            return(self.img1)
    # Loads and scales the button's image to its given dimensions while blitting and updating the screen
    def display(self, window):
        img = pg.image.load(self.highlight())
        img = pg.transform.scale(img, self.dimensions)
        window.blit(img, self.position)
        pg.display.update()

# Takes a 4:3 image, blows it up to fit the window and displays as a background
def show_Background(background_Image, window):
    background_Image = pg.image.load(background_Image)
    background_Image = pg.transform.scale(background_Image, (800,600))
    window.blit(background_Image, (0,0))

# Takes an image and displays to its given position and size
def show_Title(title_img, position, size, window):
    title = pg.image.load(title_img)
    title = pg.transform.scale(title, size)
    window.blit(title, position)

# Studio opening screen
def open_Screen(window):
    # Takes the Studio's title, scales and positions it
    logo = pg.image.load("FLASH_MenuAssets/FLASH_Logos/FLASH_Title.png")
    logo = pg.transform.scale(logo, (406, 201))
    window.blit(logo, (185, 185))
    pg.display.update()
    pg.time.wait(2500)
    opacity = 0
    blackScreen = pg.Surface((800, 600))
    while opacity <= 5:
        # Keeps blitting a translucent surface to the screen until it completely covers the image
        blackScreen.set_alpha(opacity)
        window.blit(blackScreen, (0,0))
        opacity += 0.01
        pg.display.update()
    
def main_Menu(fullscreen, difficulty, graphic_Setting, controls, title):
    # Initial setup
    pg.init()
    windowWidth = 800
    windowLength = 600
    if fullscreen:
        window = pg.display.set_mode((windowWidth, windowLength), pg.FULLSCREEN|pg.HWSURFACE|pg.DOUBLEBUF)
    else:
        window = pg.display.set_mode((windowWidth, windowLength), pg.HWSURFACE|pg.DOUBLEBUF)
    pg.mouse.set_visible(True)
    pg.display.set_caption('FLASH')
    
    # States of whether or not each screen is supposed to be displayed
    menu = True
    game = True
    help = False
    help_HowToPlay = False
    help_Controls = False
    options = False
    graphics = False
    keybinds = False
    alreadyFullscreen = fullscreen
    helpP2 = False
    credits = False
    
    # Unticked and Ticked images being stored in variables for later in the graphics menu
    tickbox = "FLASH_Unticked.png"
    tickbox_Highlighted = "FLASH_UntickedHighlighted.png"
    
    # Default game settings
    #===========================================================================
    # difficulty = 1 #0 = Easy, 1 = Normal, 2 = Hard
    # graphic_Setting = 1 #0 = Low, 1 = Medium, 2 = High
    # controls = 0 #0 =  Mouse, 1 = Keyboard
    #===========================================================================
    
    # Sets the window's icon image
    programIcon = pg.image.load('FLASH_MenuAssets/FLASH_Icon.png')
    pg.display.set_icon(programIcon)
    
    # Setup for the two main fonts used
    #===============================================================================
    # mainFont = pg.font.Font("FLASH_8BITWONDER.TTF", 24)
    # subFont = pg.font.Font("FLASH_8BITWONDER.TTF", 12)
    #===============================================================================
    
    # Loops until the game ends
    # Loops until the game ends
    while game:
        if fullscreen and not alreadyFullscreen:
            window = pg.display.set_mode((windowWidth, windowLength), pg.FULLSCREEN|pg.HWSURFACE|pg.DOUBLEBUF)
            alreadyFullscreen = True
        elif not fullscreen and alreadyFullscreen:
            window = pg.display.set_mode((windowWidth, windowLength), pg.HWSURFACE|pg.DOUBLEBUF)
            alreadyFullscreen = False
        # Shows company title
        if title:
            open_Screen(window)
            title = False
    
        if menu:
            # These except "show_Title" will be here every screen
            # Just displays the background and states each button on the screen in a list
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_MenuBackground.png", window)
            show_Title("FLASH_MenuAssets/FLASH_Logos/FLASH_Logo.png", (275, 100), (255, 179), window)
            # Order of arguments goes like: Button Image, Highlighted Button Image, Position, and Dimensions
            main_Menu_Options = [Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Start.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_StartHighlighted.png", (40, 300), (100, 50), window),
                                 Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Help.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_HelpHighlighted.png", (40, 400), (100, 50), window),
                                 Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Exit.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_ExitHighlighted.png", (40, 500), (100, 50), window),
                                 Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Options.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_OptionsHighlighted.png", (745, 545), (50, 50), window),
                                 Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Credits.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_CreditsHighlighted.png", (10,10), (100, 50), window)]
    
        # This format will be seen every screen as well
        # Keeps updating the menu as long as it's supposed to
        while menu:
            menuTime = pg.time.get_ticks() / 1000
            
            # Grabs events being projected to PyGame
            for event in pg.event.get():
                # This tells Python to do a checklist for every option in the list of buttons
                for option in main_Menu_Options:
                    # Detects if the mouse is over the button
                    if option.rect.collidepoint(pg.mouse.get_pos()):
                        option.mouseOver = True
                        # These two lines just update the button's images
                        option.highlight()
                        option.display(window)
    
                        # These are self-explanatory, FLASH_" " is whatever the button is
                        # For example, below is the start button
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Start.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    return [difficulty, graphic_Setting, controls, fullscreen, menuTime]
    
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Help.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    # This will happen for most of the buttons
                                    # Just switching the states of each screen to determine if each screen is supposed to show
                                    menu = False
                                    show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_MenuBackground.png", window)
                                    help = True

                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Exit.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    # Quits the game
                                    pg.quit()
                                    sys.exit()
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Options.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    menu = False
                                    graphics = True
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Credits.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    credits = True
                                    menu = False
                    else:
                        # If the program doesn't detect that the mouse is over the button, it'll reset back to its unhighlighted image
                        option.mouseOver = False
                    option.highlight()
                    option.display(window)
                pg.display.update()
            # This will appear every screen, just quits the game when the user presses X on the window
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
    
        pg.display.update()
    
        # First Help page
        if help:
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_HowToPlayScreen.png", window)
            helpOptions = [Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", (10, 10), (100, 50), window),
                           Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Next.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_NextHighlighted.png", (690, 10), (100, 50), window)]

        while help:

            for event in pg.event.get():
    
                for option in helpOptions:
    
                    if option.rect.collidepoint(pg.mouse.get_pos()):
                        option.mouseOver = True
                        option.highlight()
                        option.display(window)
                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    help = False
                                    menu = True

                        if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Next.png":
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    helpP2 = True
                                    help = False
                    else:
                        option.mouseOver = False
                    option.highlight()
                    option.display(window)
                pg.display.update()

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # A new option, not shown in the main menu loop
            # Will exit back to the previous screen when user presses escape.
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    help = False
                    menu = True

            # Second Help Page
            if helpP2:
                show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_HowToPlayControls.png", window)
                helpOptions = [Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", (10, 10), (100, 50), window)]

            while helpP2:

                for event in pg.event.get():

                    for option in helpOptions:

                        if option.rect.collidepoint(pg.mouse.get_pos()):
                            option.mouseOver = True
                            option.highlight()
                            option.display(window)
                            if option.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png":
                                if event.type == pg.MOUSEBUTTONDOWN:
                                    if event.button == 1:
                                        helpP2 = False
                                        menu = True
                        else:
                            option.mouseOver = False
                        option.highlight()
                        option.display(window)
                    pg.display.update()

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        helpP2 = False
                        help = True
    
    
        # Graphics screen
        if graphics:
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_MenuBackground.png", window)
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_SettingsMenu.png", window)
            graphicsBack = Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", (10, 10), (100, 50), window)
    
        while graphics:
            # Below is a list of rules
            # According to each of the game's settings like Difficulty and Graphics,
            # It will switch the images for each buttons, with the selected setting being highlighted
            if fullscreen == True:
                tickbox = "FLASH_MenuAssets/FLASH_Buttons/FLASH_TickedBox.png"
                tickbox_Highlighted = "FLASH_MenuAssets/FLASH_Buttons/FLASH_TickedHighlighted.png"
                #===============================================================
                # if not alreadyFullscreen:
                #     window = pg.display.set_mode((windowWidth, windowLength), pg.FULLSCREEN|pg.HWSURFACE|pg.DOUBLEBUF)
                #     alreadyFullscreen = True
                #===============================================================
            if fullscreen == False:
                tickbox = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Unticked.png"
                tickbox_Highlighted = "FLASH_MenuAssets/FLASH_Buttons/FLASH_UntickedHighlighted.png"
                #===============================================================
                # if alreadyFullscreen:
                #     window = pg.display.set_mode((windowWidth, windowLength), pg.HWSURFACE|pg.DOUBLEBUF)
                #     alreadyFullscreen = False
                #===============================================================
            if controls == 0:
                mouseButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_MouseHighlighted.png"
                keyboardButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Keyboard.png"
            if controls == 1:
                mouseButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Mouse.png"
                keyboardButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_KeyboardHighlighted.png"
    
            if graphic_Setting == 0:
                lowButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_LowHighlighted.png"
                mediumButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Medium.png"
                highButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_High.png"
            if graphic_Setting == 1:
                lowButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Low.png"
                mediumButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_MediumHighlighted.png"
                highButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_High.png"
            if graphic_Setting == 2:
                lowButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Low.png"
                mediumButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Medium.png"
                highButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_HighHighlighted.png"
    
            if difficulty == 0:
                easyButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_EasyHighlighted.png"
                normalButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Normal.png"
                hardButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Hard.png"
            if difficulty == 1:
                easyButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Easy.png"
                normalButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_NormalHighlighted.png"
                hardButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Hard.png"
            if difficulty == 2:
                easyButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Easy.png"
                normalButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_Normal.png"
                hardButton = "FLASH_MenuAssets/FLASH_Buttons/FLASH_HardHighlighted.png"
            # The list of buttons are places here in the while loop so that they stay highlighted when switched.
            graphics_Menu_Options = [Option(tickbox, tickbox_Highlighted, (610, 400), (32,32), window),
                                     Option(mouseButton, mouseButton, (500, 100), (100, 50), window),
                                     Option(keyboardButton, keyboardButton, (625, 100), (100, 50), window),
                                     Option(lowButton, lowButton, (400, 200), (100, 50), window),
                                     Option(mediumButton, mediumButton, (525, 200), (100, 50), window),
                                     Option(highButton, highButton, (650, 200), (100, 50), window),
                                     Option(easyButton, easyButton, (400, 300), (100, 50), window),
                                     Option(normalButton, normalButton, (525, 300), (100, 50), window),
                                     Option(hardButton, hardButton, (650, 300), (100, 50), window)
                                     ]
            pg.display.update()
    
    
            # Back to our typical list of lines
            for event in pg.event.get():
                if graphicsBack.rect.collidepoint(pg.mouse.get_pos()):
                    # The only highlighted button is our back button.
                    graphicsBack.mouseOver = True
                    graphicsBack.highlight()
                    graphicsBack.display(window)
                    if graphicsBack.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png":
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                graphics = False
                                menu = True
                    
                else:
                    graphicsBack.mouseOver = False
                
                graphicsBack.highlight()
                graphicsBack.display(window)
                for option in graphics_Menu_Options:
                    if option.rect.collidepoint(pg.mouse.get_pos()):
                        option.mouseOver = True
                        option.highlight()
                        option.display(window)
                        # List of rules for when a user clicks one of the settings options, it will change the global variable to the selected option.
                        if option.img1 == tickbox:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    if fullscreen:
                                        fullscreen = False
                                        pg.display.toggle_fullscreen()
                                    else:
                                        fullscreen = True
                                        pg.display.toggle_fullscreen()
                        if option.img1 == easyButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    difficulty = 0
                        if option.img1 == normalButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    difficulty = 1
                        if option.img1 == hardButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    difficulty = 2
                        if option.img1 == lowButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    graphic_Setting = 0
                        if option.img1 == mediumButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    graphic_Setting = 1
                        if option.img1 == highButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    graphic_Setting = 2
                        if option.img1 == mouseButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    controls = 0
                        if option.img1 == keyboardButton:
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    controls = 1
                    else:
                        option.mouseOver = False
                        option.highlight()
                        option.display(window)
                    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    graphics = False
                    menu = True
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            pg.display.update()
    
        # Credits screen
        if credits:
            show_Background("FLASH_MenuAssets/FLASH_Backgrounds/FLASH_CreditsScreen.png", window)
            pg.display.update()
            backCredits = Option("FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png", "FLASH_MenuAssets/FLASH_Buttons/FLASH_BackHighlighted.png", (10, 10), (100, 50), window)
    
        while credits:
    
            for event in pg.event.get():
                if backCredits.rect.collidepoint(pg.mouse.get_pos()):
                    # The only highlighted button is our back button.
                    backCredits.mouseOver = True
                    backCredits.highlight()
                    backCredits.display(window)
                    if backCredits.img1 == "FLASH_MenuAssets/FLASH_Buttons/FLASH_Back.png":
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                credits = False
                                menu = True
                    
                else:
                    backCredits.mouseOver = False
                
                backCredits.highlight()
                backCredits.display(window)
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        credits = False
                        menu = True
    
    return [difficulty, graphic_Setting, controls, fullscreen, menuTime]

def settings_Change(settings):
    if settings[0] == 0:
        ps.difficulty = 'easy'
    elif settings[0] == 1:
        ps.difficulty = 'normal'
    elif settings[0] == 2:
        ps.difficulty = 'hard'
    
    if settings[1] == 0:
        ps.screenIterator = 8
        ps.rayIncrementor = 0.08
    elif settings[1] == 1:
        ps.screenIterator = 5
        ps.rayIncrementor = 0.05
    elif settings[1] == 2:
        ps.screenIterator = 1
        ps.rayIncrementor = 0.02
    
    if settings[2] == 0:
        ps.mouseFlag = True
    elif settings[2] == 1:
        ps.mouseFlag = False
    
    ps.gameFullscreen = settings[3]
