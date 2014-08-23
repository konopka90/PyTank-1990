import sdl2
import sdl2.ext

class GameState(object):
    
    MENU_ANIMATION_START = 1
    MENU_ANIMATION = 2
    MENU = 3
    STAGE_SELECT = 4
    STAGE_SHOW_NUMBER = 5
    STAGE = 6
    STAGE_SCORE = 7
    PAUSE = 8

class Game:

    WIDTH = 256
    HEIGHT = 240
    DELAY = 10
    
    def __init__(self, window):
        self._window = window
        self._surface = window.get_surface()
        self._factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        self._spriterenderer = self._factory.create_sprite_render_system(window)

        self._gameState = GameState.MENU_ANIMATION_START
    
    def run(self, events):
        
        sdl2.ext.fill(self._surface, 0)
        
        if(self._gameState == GameState.MENU_ANIMATION_START):
            self._menuAnimation = self._factory.from_image('pytank/data/menu_animation.bmp')
            self._menuAnimationCounter = Game.HEIGHT
            self._gameState = GameState.MENU_ANIMATION
  
        if(self._gameState == GameState.MENU_ANIMATION):
            sdl2.ext.line(self._surface, sdl2.ext.Color(0,0,0),(1,2,200,200))
            self._spriterenderer.render(self._menuAnimation,0,self._menuAnimationCounter)
            self._menuAnimationCounter = self._menuAnimationCounter - 1
            if(self._menuAnimationCounter == 0):
                self._menuSprite = self._menuAnimation
                self._gameState = GameState.MENU
                
        if(self._gameState == GameState.MENU):
            self._spriterenderer.render(self._menuSprite)
        
        sdl2.SDL_Delay(Game.DELAY)
        
				