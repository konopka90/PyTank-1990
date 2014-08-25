# -*- coding: utf-8 -*-
from video import *
from colors import *
import gameVars
import myInput
import os, os.path

class ShowLevelsResult:

    def __init__(self, ok = False, cancel = False, letter = '', number = -1):
        self.OK = ok
        self.CANCEL = cancel
        self.letter = letter
        self.number = number
    
        
class ShowLevels:
    
    def __init__(self):
        self._loadMapCursorPosition = 0
        self._loadMapOffset = 0
        pass
    
    
    def run(self, events, renderer):
        renderer.clear(Colors.GRAY)
        levels = self._getLevels()
        numLevels = len(levels)
        
        x = 80
        origin_y = y = 5        
        yDiff = 12;        
        showMax = (GameVars.HEIGHT - y) / yDiff
        cursorMax = min(showMax, numLevels)
        
        
        result = ShowLevelsResult()        
        
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
            
            if levelNumber < len(levels):            
                levelName = levels[levelNumber]
                
                letter = levelName[0]
                number = int(levelName[1])
                
                result = ShowLevelsResult(True, False, letter,number)
            
        elif myInput.isKeyDown(events, GameVars.BUTTON_B):
            result = ShowLevelsResult(False,True,'', -1)           

        # Render levels
            
        levels = levels[self._loadMapOffset : len(levels)]
        counter = 0
        for name in levels:
            name = name.replace('.txt','')
            renderer.renderText("Stage " + name, Colors.BLACK_ENUM, x,y)
            y = y + yDiff
            counter = counter + 1
            if counter == showMax:
                break
            
        # Render cursor
            
        renderer.renderText(">", Colors.BLACK_ENUM, x - 20, origin_y + yDiff*self._loadMapCursorPosition)
    
        return result
    
    def _getLevels(self):
        return os.listdir('pytank/levels')
    