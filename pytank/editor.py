# -*- coding: utf-8 -*-
from video import *
from colors import *
from sdl2.sdlimage import *
from sdl2 import *
from gameVars import *


class Editor:
            
    RECT_WIDTH = 16        
    GRID_WIDTH = 16

    STATE_SELECT_ACTION = 1
    STATE_NEW = 2
    STATE_EDIT = 3
    STATE_SAVE = 4
    STATE_LOAD = 5
    
        
    def __init__(self,video):
        self._video = video
        
        # Assets        
        
        self._cursor = video.loadTexture("pytank/data/cursor.png")
        self._bush = video.loadTexture("pytank/data/bush.png")
        self._eagle = video.loadTexture("pytank/data/eagle.png")
        self._brick = video.loadTexture("pytank/data/brick.png")
        self._fast = video.loadTexture("pytank/data/fast.png")
        self._water = video.loadTexture("pytank/data/water.png")
        self._metal_brick = video.loadTexture("pytank/data/metal_brick.png")
        self._menuSelector = self._video.loadTexture('pytank/data/menu_selector.bmp')  

        
        # Variables        
        
        self._cursorCounter = 0
        self._drawCursor = True
        self._cursorX = 0
        self._cursorY = 0
        self._state = self.STATE_SELECT_ACTION
    
        self._menuSelectorCounter = 0
        self._menuSelectorArray = [ 0 , 13 ]
        self._menuSelectorHeight = [ 0 , 16 , 32, 48, 64]
        self._menuAction = 0
       
       
        self.NUM_GRIDS_X = (GameVars.WIDTH - Editor.RECT_WIDTH * 2) / Editor.GRID_WIDTH
        self.NUM_GRIDS_Y = (GameVars.HEIGHT - Editor.RECT_WIDTH * 2) / Editor.GRID_WIDTH
        
    def run(self, events):
    
        renderer = self._video
        renderer.clear()
        
        
        if self._state == self.STATE_SELECT_ACTION:


            for event in events:				
                if event.type == SDL_KEYDOWN:
                    if event.key.keysym.sym == GameVars.BUTTON_SELECT:
                        self._menuAction = (self._menuAction + 1) % len(self._menuSelectorHeight)
                    if event.key.keysym.sym == GameVars.BUTTON_A and self._menuAction == 4:
                        return True
                    if event.key.keysym.sym == GameVars.BUTTON_A and self._menuAction == 1:
                        self._state = self.STATE_NEW

            xs = 60
            ys = 80
            diff = 16
            
            renderer.clear(Colors.BLACK)
            renderer.renderText("Edit current level",Colors.WHITE_ENUM,xs,ys)
            renderer.renderText("New level",Colors.WHITE_ENUM,xs,ys+diff)
            renderer.renderText("Save level",Colors.WHITE_ENUM,xs,ys+diff*2)
            renderer.renderText("Load level",Colors.WHITE_ENUM,xs,ys+diff*3)
            renderer.renderText("Go to menu",Colors.WHITE_ENUM,xs,ys+diff*4)
            
            # Draw selector            
            
            x = self._menuSelectorArray[self._menuSelectorCounter % 2]
            y = self._menuSelectorHeight[self._menuAction]
            
                
            renderer.render(self._menuSelector,xs - 24, ys+y - 3,SDL_Rect(x,0,13,13))
            
            self._menuSelectorCounter = self._menuSelectorCounter + 1
            
        if self._state == self.STATE_NEW:
            self._state = self.STATE_EDIT
            
        if self._state == self.STATE_EDIT:
        
        
            # Draw rect
    
            RECT_WIDTH = Editor.RECT_WIDTH
            
            renderer.drawRect(Colors.GRAY,0,0,RECT_WIDTH,GameVars.HEIGHT)     
            renderer.drawRect(Colors.GRAY,GameVars.WIDTH - RECT_WIDTH,0,RECT_WIDTH,GameVars.HEIGHT)     
            renderer.drawRect(Colors.GRAY,0,0,GameVars.WIDTH,RECT_WIDTH)     
            renderer.drawRect(Colors.GRAY,0,GameVars.HEIGHT - RECT_WIDTH,GameVars.WIDTH,RECT_WIDTH)  
            
            self._blinkCursor()
            self._handleEvents(events)
        
    def _blinkCursor(self):
        
        if self._cursorCounter % 30 == 0:
            self._drawCursor = not self._drawCursor
            
        if self._drawCursor:
            self._video.render(self._cursor, Editor.RECT_WIDTH + self._cursorX*Editor.GRID_WIDTH, Editor.RECT_WIDTH + self._cursorY*Editor.GRID_WIDTH)    
        
        self._cursorCounter = self._cursorCounter + 1
        
        
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
                            self._state = self.STATE_SELECT_ACTION
                            
                        