from gamevars import *
from sdl2 import *
from video import *
from myInput import *
from sdl2.sdlmixer import *
from level_types import *

import wx

class Direction:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

class TankType:
    PLAYER_1 = 1
    PLAYER_2 = 2
    ENEMY_1 = 3
    ENEMY_2 = 4
    ENEMY_3 = 5
    ENEMY_4 = 6
    
class TankState:
    SPAWN = 0
    SPAWN_PROTECTION = 1
    NORMAL = 2
    DESTROY = 3

class Tank:
    
    _type = 0
    _direction = Direction.UP
    _lastDirection = Direction.UP
    _textureMapping = {}
    _isMoving = False
    _counter = 0
    _animation = 0
    
    x = 0
    y = 0
    
    xGrid = 0
    yGrid = 0
    
    upgrade = 1
    
    def __init__(self, tankType, level):
        
        self._level = level
        self._type = tankType        
        self._state = TankState.NORMAL

        self._shotSound = Mix_LoadWAV('pytank/data/shot.wav')
        self.sound = wx.Sound('pytank/data/drive.wav')
        
        self._textureMapping[TankType.PLAYER_1] = Video.Renderer.loadTexture('player1.png')
        self._textureMapping[TankType.PLAYER_2] = Video.Renderer.loadTexture('player2.png')
        self._textureMapping[TankType.ENEMY_1] = Video.Renderer.loadTexture('enemy1.png')
        self._textureMapping[TankType.ENEMY_2] = Video.Renderer.loadTexture('enemy2.png')
        self._textureMapping[TankType.ENEMY_3] = Video.Renderer.loadTexture('enemy3.png')
        self._textureMapping[TankType.ENEMY_4] = Video.Renderer.loadTexture('enemy4.png')
        
        self.setGridPosition(9,24)
    
    def getPosition(self):
        return [self.x, self.y]
        
    # Parameters are render position (not grid position)
    def setPosition(self,x,y):
        self.x = x
        self.y = y
        res = self._castToGridPosition(x,y)
        self.xGrid = res[0]
        self.yGrid = res[1]
        
    def setGridPosition(self,x,y):
        self.xGrid = x
        self.yGrid = y
        self.x = GameVars.FRAME_WIDTH + x * (GameVars.TANK_WIDTH / 2)
        self.y = GameVars.FRAME_WIDTH + y * (GameVars.TANK_WIDTH / 2)
        
        
    def setDirection(self,direction):
        self._lastDirection = self._direction
        self._direction = direction
        
    def run(self,events):
        
        self._isMoving = False
        collisionX = 0
        collisionY = 0
        collisionX_2 = 0
        collisionY_2 = 0
        dx = 1
        direction = None
               
        
        if isKeyDown(events, GameVars.BUTTON_A):
            Mix_PlayChannel(2, self._shotSound, 0)
            pass
        if isKeyDownGame(GameVars.BUTTON_LEFT):
            direction = Direction.LEFT
            collisionX = -1 
            collisionX_2 = -1 
            collisionY_2 = GameVars.TANK_WIDTH - 1
            #self.setDirection(Direction.LEFT)
            #self._isMoving = True
            #self.setPosition(pos[0] - dx, pos[1])
            pass
        
        elif isKeyDownGame(GameVars.BUTTON_UP):
            direction = Direction.UP
            collisionY = -1
            collisionX_2 = GameVars.TANK_WIDTH - 1
            collisionY_2 = -1
            #self.setDirection(Direction.UP)
            #self._isMoving = True
            #self.setPosition(pos[0], pos[1] - dx)
            pass
        
        elif isKeyDownGame(GameVars.BUTTON_RIGHT):
            direction = Direction.RIGHT
            collisionX = GameVars.TANK_WIDTH
            collisionX_2 = GameVars.TANK_WIDTH
            collisionY_2 = GameVars.TANK_WIDTH - 1
            #self.setDirection(Direction.RIGHT)
            #self._isMoving = True
            #self.setPosition(pos[0] + dx, pos[1])
            pass
        
        elif isKeyDownGame(GameVars.BUTTON_DOWN):
            direction = Direction.DOWN
            collisionY = GameVars.TANK_WIDTH
            collisionX_2 = GameVars.TANK_WIDTH - 1
            collisionY_2 = GameVars.TANK_WIDTH 
            #self.setDirection(Direction.DOWN)
            #self._isMoving = True
            #self.setPosition(pos[0], pos[1] + dx)
            pass
        
        if direction is not self._direction and direction is not None:
            res = self._castToGridPosition(self.x, self.y)
            x = res[0]
            y = res[1]
            self.setGridPosition(x,y)
                    
        if direction is not None:
           self.setDirection(direction)
           self._isMoving = True
           
        pos = self.getPosition()
        collision = self.isCollision(self.x + collisionX, self.y + collisionY)
        collision2 = self.isCollision(self.x + collisionX_2, self.y + collisionY_2)
        
        if collision is False and collision2 is False:
            if direction is Direction.LEFT:
                self.setPosition(pos[0] - dx, pos[1])
            elif direction is Direction.UP:
                self.setPosition(pos[0], pos[1] - dx)
            elif direction is Direction.RIGHT:
                self.setPosition(pos[0] + dx, pos[1])
            elif direction is Direction.DOWN:
                self.setPosition(pos[0], pos[1] + dx)
                
                
        # Make animation
        if self._isMoving:
            
            self._counter = self._counter + 1
            if self._counter >= 3:
                self._counter = 0
                self._animation = (self._animation + 1) % 2
                
            #self.sound.Play(wx.SOUND_ASYNC)
           # Mix_Volume(GameVars.CHANNEL_DRIVE, MIX_MAX_VOLUME)
            #Mix_Resume(GameVars.CHANNEL_DRIVE)
        #else:
           # Mix_Pause(GameVars.CHANNEL_DRIVE)
           # Mix_Volume(GameVars.CHANNEL_DRIVE, 0)
            
                
        
        pass    
    
    def isCollision(self,x, y):
        res = self._castToGridPosition(x,y)
        x = res[0] 
        y = res[1] 
        
        if x >= GameVars.NUM_GRID_X or y >= GameVars.NUM_GRID_Y:
            return True
            
        chunk = self._level[y][x]
        if chunk is BlockType.EMPTY or chunk is BlockType.FAST or chunk is BlockType.BUSH:
            return False
        
        return True

        
    def _castToGridPosition(self, x, y):
        x = int((x - GameVars.FRAME_WIDTH) / (GameVars.TANK_WIDTH / 2))
        y = int((y - GameVars.FRAME_WIDTH) / (GameVars.TANK_WIDTH / 2))
        return [x,y]
            
    def render(self):
        
        # Compute y in texture depending on direction
        # Order: LEFT, UP, RIGHT, DOWN
        
        if self._state == TankState.SPAWN:
            pass
        elif self._state == TankState.NORMAL:
            
            x = 0
            y = self._direction * GameVars.TANK_WIDTH
        
            # Compute y depending on upgrade
            
            if self._type == TankType.PLAYER_1 or self._type == TankType.PLAYER_2:
                y = y + (self.upgrade - 1) * 4 * GameVars.TANK_WIDTH
                
            # Compute x depending on animation
            if self._animation == 1:
                x = GameVars.TANK_WIDTH
            
            Video.Renderer.render(self._textureMapping[self._type],self.x, self.y, SDL_Rect(x,y,GameVars.TANK_WIDTH,GameVars.TANK_WIDTH))
        pass
        