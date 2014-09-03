# -*- coding: utf-8 -*-

import ctypes
import sdl2

from sdl2 import *
from gamevars import *
from sdl2.keyboard import *

keyboardArray = []    
    
def getKeyboardState():
    """ Returns a list with the current SDL keyboard state,
    which is updated on SDL_PumpEvents. """
    global keyboardArray
    numkeys = ctypes.c_int()
    keystate = sdl2.keyboard.SDL_GetKeyboardState(ctypes.byref(numkeys))
    ptr_t = ctypes.POINTER(ctypes.c_uint8 * numkeys.value)        
    keyboardArray = ctypes.cast(keystate, ptr_t)[0]
    
def isKeyDown(events, button):
    
    for event in events:				
        if event.type == SDL_KEYDOWN:
            if event.key.keysym.sym == button:
                return True
    return False
    
def isKeyUp(events, button):
    
    for event in events:				
        if event.type == SDL_KEYUP:
            if event.key.keysym.sym == button:
                return True
    return False


def translateToScancode(button):
    if button == GameVars.BUTTON_A:
        return SDL_SCANCODE_A
    if button == GameVars.BUTTON_B: 
        return SDL_SCANCODE_Z
    if button == GameVars.BUTTON_DOWN:
        return SDL_SCANCODE_DOWN
    if button == GameVars.BUTTON_LEFT:
        return SDL_SCANCODE_LEFT
    if button == GameVars.BUTTON_UP:
        return SDL_SCANCODE_UP
    if button == GameVars.BUTTON_RIGHT:
        return SDL_SCANCODE_RIGHT
    if button == GameVars.BUTTON_SELECT:
        return SDL_SCANCODE_S
    if button == GameVars.BUTTON_START:
        return SDL_SCANCODE_RETURN
        
        

# This time variable is SCANCODE    
def isKeyDownGame(button):
    code = translateToScancode(button)
    return keyboardArray[code] == 1
    
    
def isKeyUpGame(button):
    code = translateToScancode(button)
    return keyboardArray[code] == 0