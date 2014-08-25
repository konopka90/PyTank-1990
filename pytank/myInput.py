# -*- coding: utf-8 -*-

from sdl2 import *

def isKeyDown(events, button):
    
    for event in events:				
        if event.type == SDL_KEYDOWN:
            if event.key.keysym.sym == button:
                return True
    return False