# -*- coding: utf-8 -*-
from video import *
from colors import *
from sdl2.sdlimage import *
from sdl2 import *
from gamevars import *
from level import *
from editor_element import *
from show_levels import *
from tank import *

import myInput
import os, os.path

    

class Editor:
            


    STATE_SELECT_ACTION = 1
    STATE_NEW = 2
    STATE_EDIT = 3
    STATE_SAVE = 4
    STATE_SAVE_START = 5
    STATE_LOAD_START = 6
    STATE_LOAD = 7
    
        
    def __init__(self):
        
        # Assets        
        
        self._cursor = Video.Renderer.loadTexture("cursor.png")
        self._menuSelector =  Video.Renderer.loadTexture('menu_selector.bmp')  

        
        # Variables        
        
        self._cursorCounter = 0
        self._drawCursor = True
        self._cursorX = 0
        self._cursorY = 0
        self._state = self.STATE_SELECT_ACTION
        self._mapNumber = 0
        self._mapLetter = 'A'
        self._saveMapCursorPosition = 0
        self._showLevels = ShowLevels()
    
        self._menuSelectorCounter = 0
        self._menuSelectorArray = [ 0 , 13 ]
        self._menuSelectorHeight = [ 0 , 16 , 32, 48, 64]
        self._menuAction = 0
        self._currentElement = EditorElement.EMPTY
        
        self._level = Level(LevelMode.EDIT, GameVars.NUM_GRID_X, GameVars.NUM_GRID_Y)
        
        self.tank = Tank(TankType.PLAYER_1, self._level)
        
        
        
    def run(self, events):
    
        self.tank.run(events)
        renderer = Video.Renderer
        renderer.clear()
        
        if self._state == self.STATE_SELECT_ACTION:


            for event in events:				
                if event.type == SDL_KEYDOWN:
                    if event.key.keysym.sym == GameVars.BUTTON_SELECT:
                        self._menuAction = (self._menuAction + 1) % len(self._menuSelectorHeight)
                    if event.key.keysym.sym == GameVars.BUTTON_A and self._menuAction == 4:
                        return True
                    if event.key.keysym.sym == GameVars.BUTTON_A and self._menuAction == 0:
                        self._state = self.STATE_EDIT
                    if event.key.keysym.sym == GameVars.BUTTON_A and self._menuAction == 1:
                        self._state = self.STATE_NEW
                    if event.key.keysym.sym == GameVars.BUTTON_A and self._menuAction == 2:
                        self._state = self.STATE_SAVE_START
                    if event.key.keysym.sym == GameVars.BUTTON_A and self._menuAction == 3:
                        self._state = self.STATE_LOAD_START
                        
            xs = 60
            ys = 80
            diff = 16
            
            renderer.clear(Colors.BLACK)
            renderer.renderText("Edit current stage",Colors.WHITE_ENUM,xs,ys)
            renderer.renderText("New stage",Colors.WHITE_ENUM,xs,ys+diff)
            renderer.renderText("Save stage",Colors.WHITE_ENUM,xs,ys+diff*2)
            renderer.renderText("Load stage",Colors.WHITE_ENUM,xs,ys+diff*3)
            renderer.renderText("Go to menu",Colors.WHITE_ENUM,xs,ys+diff*4)
            
            # Draw selector            
            
            x = self._menuSelectorArray[self._menuSelectorCounter % 2]
            y = self._menuSelectorHeight[self._menuAction]
            
                
            renderer.render(self._menuSelector,xs - 24, ys+y - 3,SDL_Rect(x,0,13,13))
            
            self._menuSelectorCounter = self._menuSelectorCounter + 1

        # New level
        
        if self._state == self.STATE_NEW:
            self._createNewLevel()
            self._state = self.STATE_EDIT
        
        # Level edition
        
        if self._state == self.STATE_EDIT:
            self._handleStateEdit(events)
            
        # Save level

        if self._state == self.STATE_SAVE_START:
            self._mapNumber = self._numberOfLevels() + 1
            self._state = self.STATE_SAVE            
            
        elif self._state == self.STATE_SAVE:
            self._handleSaveLevel(events)
            
        # Load level
        if self._state == self.STATE_LOAD_START:
            self._loadMapOffset = 0
            self._loadMapCursorPosition = 0
            self._state = self.STATE_LOAD
            
        elif self._state == self.STATE_LOAD:
            self._handleLoadLevel(events)
        

    def _handleStateEdit(self, events):

            self._level.render()
            
            # Draw current block information

            x = GameVars.WIDTH - GameVars.FRAME_WIDTH
            y = 0                
            Video.Renderer.renderText("Current block:", Colors.BLACK_ENUM, 120, 4)
            table = self._level.getBlockMatrix(self._currentElement)   
            self._level._renderBlock(table[0][0], x, y)
            self._level._renderBlock(table[0][1], x + GameVars.LEVEL_GRID_WIDTH, y)
            self._level._renderBlock(table[1][0], x, y + GameVars.LEVEL_GRID_WIDTH)
            self._level._renderBlock(table[1][1], x + GameVars.LEVEL_GRID_WIDTH, y + GameVars.LEVEL_GRID_WIDTH)
            
            self._blinkCursor()
            self._handleEvents(events)
            
    def _handleSaveLevel(self, events):

        y = GameVars.HEIGHT / 2 - 8
        
        renderer = Video.Renderer
        renderer.clear(Colors.GRAY)
        renderer.renderText("Save as", Colors.BLACK_ENUM, 50, y)
        
        # Underline     
        
        if myInput.isKeyDown(events, GameVars.BUTTON_RIGHT):
            self._saveMapCursorPosition = min(1, self._saveMapCursorPosition + 1)
            
        elif myInput.isKeyDown(events, GameVars.BUTTON_LEFT):
            self._saveMapCursorPosition = max(0, self._saveMapCursorPosition - 1)
            
        elif myInput.isKeyDown(events, GameVars.BUTTON_DOWN):
            if self._saveMapCursorPosition == 0:
                asInt = ord(self._mapLetter) + 1
                if asInt > ord('W'):
                    asInt = ord('A')
                self._mapLetter = chr(asInt)
            elif self._saveMapCursorPosition == 1:
                asInt = int(self._mapNumber) + 1
                if asInt > 50:
                    asInt = 1
                self._mapNumber = str(asInt)
                
        elif myInput.isKeyDown(events, GameVars.BUTTON_UP):
            if self._saveMapCursorPosition == 0:
                asInt = ord(self._mapLetter) - 1
                if asInt < ord('A'):
                    asInt = ord('W')
                self._mapLetter = chr(asInt)
            elif self._saveMapCursorPosition == 1:
                asInt = int(self._mapNumber) - 1
                if asInt < 1:
                    asInt = 50
                self._mapNumber = str(asInt)
                
        elif myInput.isKeyDown(events, GameVars.BUTTON_A):
            self._level.save(self._mapLetter, self._mapNumber)
            self._state = self.STATE_SELECT_ACTION
            
        elif myInput.isKeyDown(events, GameVars.BUTTON_B):
            self._state = self.STATE_SELECT_ACTION
            
            
        x = 150 + self._saveMapCursorPosition * (renderer.CHARACTER_WIDTH + 3)
        renderer.renderText(self._mapLetter + str(self._mapNumber), Colors.BLACK_ENUM, 150,y)
        renderer.renderText("_", Colors.BLACK_ENUM, x, y + 3)
        
    def _handleLoadLevel(self, events):
        
        renderer = Video.Renderer
        result = self._showLevels.run(events, renderer)
        
        if result.OK:
            letter = result.letter
            number = result.number
            self._level.load(letter, number)            
            self._state = self.STATE_EDIT
            
        elif result.CANCEL:
            self._state = self.STATE_SELECT_ACTION
            
            
    def _handleEvents(self, events):
        for event in events:				
                    if event.type == SDL_KEYDOWN:
                        if event.key.keysym.sym == GameVars.BUTTON_LEFT:
                            self._cursorX = max(self._cursorX - 1, 0)
                        if event.key.keysym.sym == GameVars.BUTTON_RIGHT:
                            self._cursorX = min(self._cursorX + 1, GameVars.NUM_CURSOR_GRID_X - 1)
                        if event.key.keysym.sym == GameVars.BUTTON_UP:
                            self._cursorY = max(self._cursorY - 1, 0)
                        if event.key.keysym.sym == GameVars.BUTTON_DOWN:
                            self._cursorY = min(self._cursorY + 1, GameVars.NUM_CURSOR_GRID_Y - 1)
                        if event.key.keysym.sym == GameVars.BUTTON_START:
                            self._state = self.STATE_SELECT_ACTION
                            self._menuAction = self._menuAction + 1
                        if event.key.keysym.sym == GameVars.BUTTON_A:
                            self._currentElement = (self._currentElement + 1) % EditorElement.COUNT
                            
                        if event.key.keysym.sym == GameVars.BUTTON_B:
                            self._currentElement = (self._currentElement - 1) % EditorElement.COUNT

                        if event.key.keysym.sym == GameVars.BUTTON_SELECT:

                            x = self._cursorX * 2
                            y = self._cursorY * 2
                            matrix = self._level.matrix

                            table = self._level.getBlockMatrix(self._currentElement)                                        
                            matrix[y][x] = table[0][0]
                            matrix[y][x+1] = table[0][1]
                            matrix[y+1][x] = table[1][0]
                            matrix[y+1][x+1] = table[1][1]
                            
                                
                                
                        
                            
    def _blinkCursor(self):
        
        if self._cursorCounter % 30 == 0:
            self._drawCursor = not self._drawCursor
            
        if self._drawCursor:
            Video.Renderer.render(self._cursor, GameVars.FRAME_WIDTH + self._cursorX*GameVars.CURSOR_GRID_WIDTH, GameVars.FRAME_WIDTH + self._cursorY*GameVars.CURSOR_GRID_WIDTH)    
        
        self._cursorCounter = self._cursorCounter + 1


    def _numberOfLevels(self):
        return len([name for name in os.listdir('pytank/levels') if os.path.isfile(name)])
        
    def _getLevels(self):
        return os.listdir('pytank/levels')