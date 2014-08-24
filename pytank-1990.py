import sys
import sdl2
import sdl2.ext
import sdl2.sdlimage
import sdl2.sdlmixer
from pytank.gameVars import *
from pytank.game import *


# Main loop

def run():
    
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO);
    sdl2.sdlimage.IMG_Init(IMG_INIT_PNG);
    if Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 2, 4096) == -1:
         print(Mix_GetError())
         return -1
         
    Mix_AllocateChannels(0)
    
    window = sdl2.ext.Window(GameVars.TITLE, size=(GameVars.WIDTH, GameVars.HEIGHT), flags=sdl2.SDL_WINDOW_RESIZABLE)# | sdl2.SDL_WINDOW_FULLSCREEN) # <-- doesnt work properly :/ 
    window.show()
    
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
    
    sdl2.sdlimage.IMG_Quit(IMG_INIT_PNG)
    return 0

if __name__ == "__main__":
    sys.exit(run())
