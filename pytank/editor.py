# -*- coding: utf-8 -*-
from video import *
from colors import *
from sdl2.sdlimage import *
from sdl2 import *
from gameVars import *
from level import *
from editor_element import *

import myInput
import os, os.path

    

class Editor:
            
    FRAME_WIDTH = 16        
    CURSOR_GRID_WIDTH = 16
    LEVEL_GRID_WIDTH = 8

    STATE_SELECT_ACTION = 1
    STATE_NEW = 2
    STATE_EDIT = 3
    STATE_SAVE = 4
    STATE_SAVE_START = 5
    STATE_LOAD_START = 6
    STATE_LOAD = 7
    
        
    def __init__(self,video):
        self._video = video
        
        # Assets        
        
        self._cursor = video.loadTexture("pytank/data/cursor.png")
        self._bush = video.loadTexture("pytank/data/bush.png")
        self._eagle = video.loadTexture("pytank/data/eagle.png")
        self._brick = video.loadTexture("pytank/data/brick.png")
        self._fast = video.loadTexture("pytank/data/fast.png")
        self._water = video.loadTexture("pytank/data/water.png")
        self._metal = video.loadTexture("pytank/data/metal_brick.png")
        self._menuSelector = self._video.loadTexture('pytank/data/menu_selector.bmp')  

        
        # Variables        
        
        self._cursorCounter = 0
        self._drawCursor = True
        self._cursorX = 0
        self._cursorY = 0
        self._state = self.STATE_SELECT_ACTION
        self._mapNumber = 0
        self._mapLetter = 'A'
        self._saveMapCursorPosition = 0
        self._loadMapCursorPosition = 0
        self._loadMapOffset = 0
    
        self._menuSelectorCounter = 0
        self._menuSelectorArray = [ 0 , 13 ]
        self._menuSelectorHeight = [ 0 , 16 , 32, 48, 64]
        self._menuAction = 0
        self._currentElement = EditorElement.EMPTY
       
        self.NUM_CURSOR_GRID_X = (GameVars.WIDTH - Editor.FRAME_WIDTH * 3) / Editor.CURSOR_GRID_WIDTH
        self.NUM_CURSOR_GRID_Y = (GameVars.HEIGHT - Editor.FRAME_WIDTH * 2) / Editor.CURSOR_GRID_WIDTH
        self.NUM_GRID_X = self.NUM_CURSOR_GRID_X * 2
        self.NUM_GRID_Y = self.NUM_CURSOR_GRID_Y * 2


        self._createNewLevel()
        
        
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
            

    def _createNewLevel(self):
        self._level = Level(self.NUM_GRID_X, self.NUM_GRID_Y)



    def _handleStateEdit(self, events):

            renderer = self._video
            
            # Draw frame
    
            FRAME_WIDTH = Editor.FRAME_WIDTH
            
            renderer.drawRect(Colors.GRAY,0,0,FRAME_WIDTH,GameVars.HEIGHT)     
            renderer.drawRect(Colors.GRAY,GameVars.WIDTH - FRAME_WIDTH - 16,0,FRAME_WIDTH * 2,GameVars.HEIGHT)     
            renderer.drawRect(Colors.GRAY,0,0,GameVars.WIDTH,FRAME_WIDTH)     
            renderer.drawRect(Colors.GRAY,0,GameVars.HEIGHT - FRAME_WIDTH,GameVars.WIDTH,FRAME_WIDTH)

            # Draw level items

            level = self._level.matrix
            currentY = self.FRAME_WIDTH
            for y in range(0,self.NUM_GRID_Y):
                currentX = self.FRAME_WIDTH
                for x in range(0,self.NUM_GRID_X):
                    ###### Check x,y or y,x
                    item = level[y][x]
                    self._renderBlock(item, currentX, currentY) 
                        
                    currentX = currentX + self.LEVEL_GRID_WIDTH
                         
                currentY = currentY + self.LEVEL_GRID_WIDTH
                
            # Draw current block information

            x = GameVars.WIDTH - Editor.FRAME_WIDTH
            y = 0                
            renderer.renderText("Current block:", Colors.BLACK_ENUM, 120, 4)
            table = self._level.getBlockMatrix(self._currentElement)   
            #renderer.drawRect(Colors.BLACK, x,y,Editor.FRAME_WIDTH,Editor.FRAME_WIDTH)
            self._renderBlock(table[0][0], x, y)
            self._renderBlock(table[0][1], x + self.LEVEL_GRID_WIDTH, y)
            self._renderBlock(table[1][0], x, y + self.LEVEL_GRID_WIDTH)
            self._renderBlock(table[1][1], x + self.LEVEL_GRID_WIDTH, y + self.LEVEL_GRID_WIDTH)
            
            self._blinkCursor()
            self._handleEvents(events)
            
    def _handleSaveLevel(self, events):

        y = GameVars.HEIGHT / 2 - 8
        
        renderer = self._video
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
        
        renderer = self._video
        renderer.clear(Colors.GRAY)
        levels = self._getLevels()#.sort()
        numLevels = len(levels)
        
        x = 80
        origin_y = y = 5        
        yDiff = 12;        
        showMax = (GameVars.HEIGHT - y) / yDiff
        cursorMax = min(showMax, numLevels)
        
        
        
        if myInput.isKeyDown(events, GameVars.BUTTON_DOWN):
            if self._loadMapCursorPosition < cursorMax - 1:
                self._loadMapCursorPosition = self._loadMapCursorPosition + 1
            else:
                if self._loadMapOffset < numLevels - cursorMax:
                    self._loadMapOffset = self._loadMapOffset + 1

        elif myInput.isKeyDown(events, GameVars.BUTTON_UP):
            if self._loadMapCursorPosition > 0:
                self._loadMapCursorPosition = self._loadMapCursorPosition - 1
            else:
                if self._loadMapOffset > 0:
                    self._loadMapOffset = self._loadMapOffset - 1
        elif myInput.isKeyDown(events, GameVars.BUTTON_A):
            levelNumber = self._loadMapCursorPosition + self._loadMapOffset
            levelName = levels[levelNumber]
            
            letter = levelName[0]
            number = int(levelName[1])
            self._level.load(letter, number)            
            self._state = self.STATE_EDIT
            
        elif myInput.isKeyDown(events, GameVars.BUTTON_B):
            self._state = self.STATE_SELECT_ACTION
            

        # Render levels
            
        levels = levels[self._loadMapOffset : len(levels)]
        counter = 0
        for name in levels:
            name = name.replace('.txt','')
            renderer.renderText("MAP " + name, Colors.BLACK_ENUM, x,y)
            y = y + yDiff
            counter = counter + 1
            if counter == showMax:
                break
            
        # Render cursor
            
        renderer.renderText(">", Colors.BLACK_ENUM, x - 20, origin_y + yDiff*self._loadMapCursorPosition)
            
        
    def _renderBlock(self, item, x, y):
        
        renderer = self._video
        
        if item == BlockType.WATER:
            renderer.render(self._water, x, y)
        elif item == BlockType.FAST:
            renderer.render(self._fast, x, y)
        elif item == BlockType.BUSH:
            renderer.render(self._bush, x, y)
        elif item == BlockType.BRICK:
            renderer.render(self._brick, x, y)
        elif item == BlockType.METAL:
            renderer.render(self._metal, x, y)
        elif item == BlockType.EAGLE_RENDER:
            renderer.render(self._eagle, x, y) 
            
    def _handleEvents(self, events):
        for event in events:				
                    if event.type == SDL_KEYDOWN:
                        if event.key.keysym.sym == GameVars.BUTTON_LEFT:
                            self._cursorX = max(self._cursorX - 1, 0)
                        if event.key.keysym.sym == GameVars.BUTTON_RIGHT:
                            self._cursorX = min(self._cursorX + 1, self.NUM_CURSOR_GRID_X - 1)
                        if event.key.keysym.sym == GameVars.BUTTON_UP:
                            self._cursorY = max(self._cursorY - 1, 0)
                        if event.key.keysym.sym == GameVars.BUTTON_DOWN:
                            self._cursorY = min(self._cursorY + 1, self.NUM_CURSOR_GRID_Y - 1)
                        if event.key.keysym.sym == GameVars.BUTTON_START:
                            self._state = self.STATE_SELECT_ACTION
                            self._menuAction = self._menuAction + 1
                        if event.key.keysym.sym == GameVars.BUTTON_A:

                            # TO DO !!!! (or not ? )
                            self._currentElement = (self._currentElement + 1) % EditorElement.COUNT
                            
                        if event.key.keysym.sym == GameVars.BUTTON_B:

                            # TO DO !!!! (or not ? )
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
            self._video.render(self._cursor, Editor.FRAME_WIDTH + self._cursorX*Editor.CURSOR_GRID_WIDTH, Editor.FRAME_WIDTH + self._cursorY*Editor.CURSOR_GRID_WIDTH)    
        
        self._cursorCounter = self._cursorCounter + 1


    def _numberOfLevels(self):
        return len([name for name in os.listdir('pytank/levels') if os.path.isfile(name)])
        
    def _getLevels(self):
        return os.listdir('pytank/levels')