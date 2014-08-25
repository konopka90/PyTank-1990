from sdl2 import *
from sdl2.ext import *
from sdl2.sdlmixer import *
from video import *
from editor import *
from colors import *
import gameVars
import myInput

class GameState(object):
    
    MENU_ANIMATION_START = 1
    MENU_ANIMATION = 2
    MENU = 3
    STAGE_SELECT_ANIMATION = 4
    STAGE_SELECT = 5
    STAGE_START = 6
    STAGE = 7
    STAGE_SCORE = 8
    PAUSE = 9
    EDITOR = 10
    


class Game:


    
    def __init__(self, window):
        self._window = window
        
        # Render stuff
        
        self._surface = window.get_surface()
        self._video = Video(window, GameVars.WIDTH, GameVars.HEIGHT)
                
        # Game stuff
        
        self._gameState = GameState.MENU_ANIMATION_START
        self._menuSelectorCounter = 0
        self._menuSelectorArray = [ 0 , 13 ]
        self._menuSelectorHeight = [ 0 , 16 , 32]
        self._menuAction = 0
        self._editor = Editor(self._video)
        
        # Assets
        self._soundIntro = Mix_LoadMUS("pytank/data/intro.ogg")
        
        
    def run(self, events):
        
        self._video.renderStart()
        
        # Game logic
        
        # Menu animation
        
        if(self._gameState == GameState.MENU_ANIMATION_START):
            self._menuTexture = self._video.loadTexture('pytank/data/menu.bmp')
            self._menuSelector = self._video.loadTexture('pytank/data/menu_selector.bmp')
            self._menuAnimationCounter = GameVars.HEIGHT
            self._gameState = GameState.MENU_ANIMATION
            
  
        if(self._gameState == GameState.MENU_ANIMATION):
        
            self._video.render(self._menuTexture, 0, self._menuAnimationCounter)
            self._menuAnimationCounter = self._menuAnimationCounter - 1
            self._menuAction = 0

            for event in events:				
                if event.type == SDL_KEYDOWN:
                    if event.key.keysym.sym == GameVars.BUTTON_SELECT:
                        self._gameState = GameState.MENU
                        break
            
            if(self._menuAnimationCounter == 0):
                self._gameState = GameState.MENU
            
        else:
            
            # Show Menu
        
            if(self._gameState == GameState.MENU):
                self._menuSelectorCounter = self._menuSelectorCounter + 1
                self._video.render(self._menuTexture,0,0)
                self._video.renderText("00",Colors.WHITE_ENUM,60,24)
                self._video.renderText("20000",Colors.WHITE_ENUM,130,24)
                
                if myInput.isKeyDown(events, GameVars.BUTTON_SELECT):
                    self._menuAction = (self._menuAction + 1) % 3
                if myInput.isKeyDown(events, GameVars.BUTTON_A):
                    if self._menuAction < 2:                            
                        self._gameState = GameState.STAGE_SELECT_ANIMATION
                        self._selectStageAnimationCounter = 0
                    if self._menuAction == 2:
                        self._gameState = GameState.EDITOR
                    
                
                x = self._menuSelectorArray[self._menuSelectorCounter % 2]
                y = self._menuSelectorHeight[self._menuAction]
                
                
                self._video.render(self._menuSelector,65,133 + y,SDL_Rect(x,0,13,13))
            
            # Show Editor
            else:
                if(self._gameState == GameState.EDITOR):
                    finished = self._editor.run(events)
                    if finished:
                        self._gameState = GameState.MENU
                
        
        
        # Show 'select stage' animation
        
        if(self._gameState == GameState.STAGE_SELECT_ANIMATION):
            self._video.clear()
            self._video.drawRect(Color(128,128,128), 0,0,GameVars.WIDTH,self._selectStageAnimationCounter)
            self._video.drawRect(Color(128,128,128), 0,GameVars.HEIGHT - self._selectStageAnimationCounter,GameVars.WIDTH,self._selectStageAnimationCounter)
            self._selectStageAnimationCounter = self._selectStageAnimationCounter + 3
            
            if self._selectStageAnimationCounter > GameVars.WIDTH / 2:
                self._gameState = GameState.STAGE_SELECT
         
        if(self._gameState == GameState.STAGE_SELECT):
            self._video.clear(Colors.BLACK)
            self._gameState = GameState.STAGE_START
            
        if(self._gameState == GameState.STAGE_START):
            if Mix_PlayMusic(self._soundIntro, 0) == -1:
                print(Mix_GetError())
            self._gameState = GameState.STAGE
        
        if(self._gameState == GameState.STAGE):
            pass
            
         
        self._video.renderStop()
        
        SDL_Delay(GameVars.DELAY)
				