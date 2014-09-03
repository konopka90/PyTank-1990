from editor_element import *
from gamevars import *
from colors import *
from tank import *
from level_types import *

class Level:

    # Defaults

    DEFAULT_SIZE_X = 26
    DEFAULT_SIZE_Y = 26

    # Vars

    matrix = 0
    
    _sizeX = 0
    _sizeY = 0
    
            
        

    
    def __init__(self, mode, sizeX = DEFAULT_SIZE_X, sizeY = DEFAULT_SIZE_Y):
        
        self._mode = mode
        
        self._bush = Video.Renderer.loadTexture("bush.png")
        self._eagle = Video.Renderer.loadTexture("eagle.png")
        self._brick = Video.Renderer.loadTexture("brick.png")
        self._fast = Video.Renderer.loadTexture("fast.png")
        self._water = Video.Renderer.loadTexture("water.png")
        self._metal = Video.Renderer.loadTexture("metal_brick.png")
        
        self._driveSound = Mix_LoadWAV('pytank/data/drive.wav')
        
        self._sizeX = sizeX
        self._sizeY = sizeY
        self.matrix = [] 
                                                        
        for i in range (0, sizeY):                               
            new = []                       
            for j in range (0, sizeX):            
                new.append(BlockType.EMPTY)             
            self.matrix.append(new) 
            
        # Initial bricks
            
        x = sizeX / 2 - 1# mid
        self.matrix[sizeY-1][x - 1] = BlockType.BRICK
        self.matrix[sizeY-2][x - 1] = BlockType.BRICK
        self.matrix[sizeY-3][x - 1] = BlockType.BRICK
        
        self.matrix[sizeY-1][x + 2] = BlockType.BRICK
        self.matrix[sizeY-2][x + 2] = BlockType.BRICK
        self.matrix[sizeY-3][x + 2] = BlockType.BRICK
        
        self.matrix[sizeY-3][x + 1] = BlockType.BRICK
        self.matrix[sizeY-3][x] = BlockType.BRICK

        # Eagle
        
        self.matrix[sizeY-2][x] = BlockType.EAGLE_RENDER
        self.matrix[sizeY-2][x + 1] = BlockType.EAGLE
        self.matrix[sizeY-1][x + 1] = BlockType.EAGLE
        self.matrix[sizeY-1][x] = BlockType.EAGLE
        
        # Start sounds
        
        #Mix_Volume(GameVars.CHANNEL_DRIVE, 0)
       
        Mix_PlayChannel(GameVars.CHANNEL_DRIVE, self._driveSound, -1)
        Mix_Pause(GameVars.CHANNEL_DRIVE)
        
    def run(self, events):
        
        if self._mode == LevelMode.GAME:
            self._player1.run(events)
        
        self.render()
        
    def render(self):
                 
        FRAME_WIDTH = GameVars.FRAME_WIDTH
        
        # Draw background

        Video.Renderer.clear(Colors.BLACK)

        # Draw level items that should be drew before tanks

        level = self.matrix
        currentY = FRAME_WIDTH
        for y in range(0,GameVars.NUM_GRID_Y):
            currentX = FRAME_WIDTH
            for x in range(0,GameVars.NUM_GRID_X):
                item = level[y][x]
                if item is BlockType.FAST:
                    self._renderBlock(item, currentX, currentY) 
                    
                currentX = currentX + GameVars.LEVEL_GRID_WIDTH
                     
            currentY = currentY + GameVars.LEVEL_GRID_WIDTH

        

        # Draw tanks
        if self._mode == LevelMode.GAME:
            self._player1.render()


        # Draw level items

        currentY = FRAME_WIDTH
        for y in range(0,GameVars.NUM_GRID_Y):
            currentX = FRAME_WIDTH
            for x in range(0,GameVars.NUM_GRID_X):
                item = level[y][x]
                if item is not BlockType.FAST:
                    self._renderBlock(item, currentX, currentY) 
                    
                currentX = currentX + GameVars.LEVEL_GRID_WIDTH
                     
            currentY = currentY + GameVars.LEVEL_GRID_WIDTH
            
                
        self._renderGrid()        
        
        # Draw frame

        
        
        Video.Renderer.drawRect(Colors.GRAY,0,0,FRAME_WIDTH,GameVars.HEIGHT)     
        Video.Renderer.drawRect(Colors.GRAY,GameVars.WIDTH - FRAME_WIDTH - 16,0,FRAME_WIDTH * 2,GameVars.HEIGHT)     
        Video.Renderer.drawRect(Colors.GRAY,0,0,GameVars.WIDTH,FRAME_WIDTH)     
        Video.Renderer.drawRect(Colors.GRAY,0,GameVars.HEIGHT - FRAME_WIDTH,GameVars.WIDTH,FRAME_WIDTH)
            
    
    def _renderBlock(self, item, x, y):
    
        if item == BlockType.WATER:
            Video.Renderer.render(self._water, x, y)
        elif item == BlockType.FAST:
            Video.Renderer.render(self._fast, x, y)
        elif item == BlockType.BUSH:
            Video.Renderer.render(self._bush, x, y)
        elif item == BlockType.BRICK:
            Video.Renderer.render(self._brick, x, y)
        elif item == BlockType.METAL:
            Video.Renderer.render(self._metal, x, y)
        elif item == BlockType.EAGLE_RENDER:
            Video.Renderer.render(self._eagle, x, y) 
            
    def _renderGrid(self):
        
        x = 0
        y = 0
        # Draw horizontal lines
        for y in xrange(GameVars.FRAME_WIDTH,GameVars.HEIGHT - GameVars.FRAME_WIDTH, GameVars.FRAME_WIDTH):
            Video.Renderer.drawRect(Colors.WHITE,x,y,GameVars.WIDTH,1)     
            
        # Draw vert lines
        y = 0
        for x in xrange(GameVars.FRAME_WIDTH,GameVars.HEIGHT - GameVars.FRAME_WIDTH, GameVars.FRAME_WIDTH):
            Video.Renderer.drawRect(Colors.WHITE,x,y,1,GameVars.HEIGHT)     
        
    # Takes EditorElement
    def getBlockMatrix(self, element):
        table = []
        row = []
        row.append(0)
        row.append(0)
        table.append(row)
        table.append(row)
        
        # Insert element
        if element == EditorElement.EMPTY:
            table = [
                        [BlockType.EMPTY, BlockType.EMPTY],
                        [BlockType.EMPTY, BlockType.EMPTY]
                     ] 
        elif element == EditorElement.HALF_BRICK_LEFT:
            table = [
                        [BlockType.BRICK, BlockType.EMPTY],
                        [BlockType.BRICK, BlockType.EMPTY]
                     ] 
        elif element == EditorElement.HALF_BRICK_TOP:
            table = [
                        [BlockType.BRICK, BlockType.BRICK],
                        [BlockType.EMPTY, BlockType.EMPTY]
                     ] 
        elif element == EditorElement.HALF_BRICK_RIGHT:
            table = [
                        [BlockType.EMPTY, BlockType.BRICK],
                        [BlockType.EMPTY, BlockType.BRICK]
                     ] 
        elif element == EditorElement.HALF_BRICK_BOTTOM:
            table = [
                        [BlockType.EMPTY, BlockType.EMPTY],
                        [BlockType.BRICK, BlockType.BRICK]
                     ] 
        elif element == EditorElement.BRICK:
            table = [
                        [BlockType.BRICK, BlockType.BRICK],
                        [BlockType.BRICK, BlockType.BRICK]
                     ] 
        elif element == EditorElement.BUSH:
            table = [
                        [BlockType.BUSH, BlockType.BUSH],
                        [BlockType.BUSH, BlockType.BUSH]
                     ] 
        elif element == EditorElement.FAST:
            table = [
                        [BlockType.FAST, BlockType.FAST],
                        [BlockType.FAST, BlockType.FAST]
                     ]            
        elif element == EditorElement.WATER:
            table = [
                        [BlockType.WATER, BlockType.WATER],
                        [BlockType.WATER, BlockType.WATER]
                     ]           
        elif element == EditorElement.METAL:
            table = [
                        [BlockType.METAL, BlockType.METAL],
                        [BlockType.METAL, BlockType.METAL]
                     ]     
        elif element == EditorElement.HALF_METAL_LEFT:
            table = [
                        [BlockType.METAL, BlockType.EMPTY],
                        [BlockType.METAL, BlockType.EMPTY]
                     ]                
        elif element == EditorElement.HALF_METAL_TOP:
            table = [
                        [BlockType.METAL, BlockType.METAL],
                        [BlockType.EMPTY, BlockType.EMPTY]
                     ]                  
        elif element == EditorElement.HALF_METAL_RIGHT:
            table = [
                        [BlockType.EMPTY, BlockType.METAL],
                        [BlockType.EMPTY, BlockType.METAL]
                     ]  
        elif element == EditorElement.HALF_METAL_BOTTOM:
            table = [
                        [BlockType.EMPTY, BlockType.EMPTY],
                        [BlockType.METAL, BlockType.METAL]
                     ] 
                     
        return table 
        
    def save(self, letter, number):
        
        filename = "pytank/levels/" + str(letter) + str(number) + ".txt"

        with open(filename, 'w') as f:
            for y in range(0,self._sizeY):
                for x in range(0,self._sizeX):
                    f.write(str(self.matrix[y][x]))
                f.write('\n')
                
    def load(self, letter, number):
        
        x = 0
        y = 0
        filename = "pytank/levels/" + str(letter) + str(number) + ".txt"
        with open(filename, 'r') as f:
            for line in f:
                x = 0
                for i in range(0,len(line)):

                    if line[i] != '\n':
                        value = int(line[i])
                        self.matrix[y][x] = value
                        x = x + 1
                y = y + 1
                
        self._player1 = Tank(TankType.PLAYER_1, self.matrix)
                