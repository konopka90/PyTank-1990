# -*- coding: utf-8 -*-
from video import *
from colors import *
from sdl2.sdlimage import *
from sdl2 import *
from gameVars import *

class Editor:
            
    RECT_WIDTH = 16        
    GRID_WIDTH = 16

        
    def __init__(self,video):
        self._video = video
        self._cursor = video.loadTexture("pytank/data/cursor.png")
        self._cursorCounter = 0
        self._drawCursor = True
        self._cursorX = 0
        self._cursorY = 0
       
        self.NUM_GRIDS_X = (GameVars.WIDTH - Editor.RECT_WIDTH * 2) / Editor.GRID_WIDTH
        self.NUM_GRIDS_Y = (GameVars.HEIGHT - Editor.RECT_WIDTH * 2) / Editor.GRID_WIDTH
        
    def run(self, events):
    
        self._video.clear()
        
        # Draw rect

        RECT_WIDTH = Editor.RECT_WIDTH
        
        self._video.drawRect(Colors.GRAY,0,0,RECT_WIDTH,GameVars.HEIGHT)     
        self._video.drawRect(Colors.GRAY,GameVars.WIDTH - RECT_WIDTH,0,RECT_WIDTH,GameVars.HEIGHT)     
        self._video.drawRect(Colors.GRAY,0,0,GameVars.WIDTH,RECT_WIDTH)     
        self._video.drawRect(Colors.GRAY,0,GameVars.HEIGHT - RECT_WIDTH,GameVars.WIDTH,RECT_WIDTH)  
        
        self._blinkCursor()
        returnToMenu = self._handleEvents(events)
        
        return returnToMenu
        
    def _blinkCursor(self):
        
        if self._cursorCounter % 30 == 0:
            self._drawCursor = not self._drawCursor
            
        if self._drawCursor:
            self._video.render(self._cursor, Editor.RECT_WIDTH + self._cursorX*Editor.GRID_WIDTH, Editor.RECT_WIDTH + self._cursorY*Editor.GRID_WIDTH)    
        
        self._cursorCounter = self._cursorCounter + 1
        
        
    # Returns True if we want to return to menu
    def _handleEvents(self, events):
        for event in events:				
                    if event.type == SDL_KEYDOWN:
                        if event.key.keysym.sym == GameVars.BUTTON_LEFT:
                            self._cursorX = max(self._cursorX - 1, 0)
                        if event.key.keysym.sym == GameVars.BUTTON_RIGHT:
                            self._cursorX = min(self._cursorX + 1, self.NUM_GRIDS_X - 1)
                        if event.key.keysym.sym == GameVars.BUTTON_UP:
                            self._cursorY = max(self._cursorY - 1, 0)
                        if event.key.keysym.sym == GameVars.BUTTON_DOWN:
                            self._cursorY = min(self._cursorY + 1, self.NUM_GRIDS_Y - 1)
                        if event.key.keysym.sym == GameVars.BUTTON_START:
                            return True
                            
        return False
                            
                        