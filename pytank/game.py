from sdl2 import *
from sdl2.ext import *
from video import *

class GameState(object):
    
    MENU_ANIMATION_START = 1
    MENU_ANIMATION = 2
    MENU = 3
    STAGE_SELECT_ANIMATION = 4
    STAGE_SELECT = 5
    STAGE = 6
    STAGE_SCORE = 7
    PAUSE = 8
    
BUTTON_SELECT = SDLK_a
BUTTON_A = SDLK_SPACE


class Game:

    TITLE = "PyTank 1990"
    WIDTH = 256
    HEIGHT = 240
    DELAY = 10
    
    def __init__(self, window):
        self._window = window
        
        # Render stuff
        
        self._surface = window.get_surface()
        self._video = Video(window, Game.WIDTH, Game.HEIGHT)
                
        # Game stuff
        
        self._gameState = GameState.MENU_ANIMATION_START
        self._menuSelectorCounter = 0
        self._menuSelectorArray = [ 0 , 13 ]
        self._menuSelectorHeight = [ 0 , 16 , 32]
        self._menuAction = 0
        

        
        
    def run(self, events):
        
        self._video.renderStart()
        
        # Game logic
        
        # Menu animation
        
        if(self._gameState == GameState.MENU_ANIMATION_START):
            self._menuTexture = self._video.loadTexture('pytank/data/menu.bmp')
            self._menuSelector = self._video.loadTexture('pytank/data/menu_selector.bmp')
            self._menuAnimationCounter = Game.HEIGHT
            self._gameState = GameState.MENU_ANIMATION
  
        if(self._gameState == GameState.MENU_ANIMATION):
        
            self._video.render(self._menuTexture, 0, self._menuAnimationCounter)
            self._menuAnimationCounter = self._menuAnimationCounter - 1
            self._menuAction = 0

            for event in events:				
                if event.type == SDL_KEYDOWN:
                    if event.key.keysym.sym == BUTTON_SELECT:
                        self._gameState = GameState.MENU
                        break
            
            if(self._menuAnimationCounter == 0):
                self._gameState = GameState.MENU
            
        else:
            
            # Show Menu
        
            if(self._gameState == GameState.MENU):
                self._menuSelectorCounter = self._menuSelectorCounter + 1
                self._video.render(self._menuTexture,0,0)
                
                
                for event in events:				
                    if event.type == SDL_KEYDOWN:
                        if event.key.keysym.sym == BUTTON_SELECT:
                            self._menuAction = self._menuAction + 1
                        if event.key.keysym.sym == BUTTON_A:
                            self._gameState = GameState.STAGE_SELECT_ANIMATION
                            self._selectStageAnimationCounter = 0
                            break
                
                x = self._menuSelectorArray[self._menuSelectorCounter % 2]
                y = self._menuSelectorHeight[self._menuAction % 3]
                
                self._video.render(self._menuSelector,65,133 + y,SDL_Rect(x,0,13,13))
            
        
        # Show 'select stage' animation
        
        if(self._gameState == GameState.STAGE_SELECT_ANIMATION):
            self._video.clear()
            self._video.drawRect(Color(128,128,128), 0,0,Game.WIDTH,self._selectStageAnimationCounter)
            self._video.drawRect(Color(128,128,128), 0,Game.HEIGHT - self._selectStageAnimationCounter,Game.WIDTH,self._selectStageAnimationCounter)
            self._selectStageAnimationCounter = self._selectStageAnimationCounter + 3
            
            if self._selectStageAnimationCounter > Game.WIDTH / 2:
                self._gameState = GameState.STAGE_SELECT
         
        if(self._gameState == GameState.STAGE_SELECT):
            self._video.clear(128,128,128)
         
        self._video.renderStop()
        
        SDL_Delay(Game.DELAY)
				