import sys
import sdl2
import sdl2.ext
import sdl2.sdlimage
from pytank.gameVars import *
from pytank.game import *


# Main loop

def run():
    
    sdl2.ext.init()
    sdl2.sdlimage.IMG_Init(IMG_INIT_PNG);
    window = sdl2.ext.Window(GameVars.TITLE, size=(GameVars.WIDTH, GameVars.HEIGHT), flags=sdl2.SDL_WINDOW_RESIZABLE)# | sdl2.SDL_WINDOW_FULLSCREEN) # <-- doesnt work properly :/ 
    window.show()
    
    # Set display mode (doesnt work :<)
    
    mode = sdl2.SDL_DisplayMode()
    sdl2.SDL_GetDisplayMode(0,0,mode)
    mode.w = GameVars.WIDTH
    mode.h = GameVars.HEIGHT
    sdl2.SDL_SetWindowDisplayMode(window.window, mode)
    
    # Run game
    
    running = True
    game = Game(window)
    
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
				
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                    break
                    
        game.run(events)
    
    sdl2.sdlimage.IMG_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
