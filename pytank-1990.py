import sys
import sdl2
import sdl2.ext
from pytank.game import *

# Main loop

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("PyTank 1990", size=(Game.WIDTH, Game.HEIGHT)) #, position=None, flags=sdl2.SDL_WINDOW_FULLSCREEN)
    window.show()
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
        window.refresh()
    return 0

if __name__ == "__main__":
    sys.exit(run())
