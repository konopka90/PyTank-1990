from editor_element import *

class BlockType:
    EMPTY = 0
    WATER = 1
    FAST = 2
    BUSH = 3
    BRICK = 4
    METAL = 5
    EAGLE = 6
    EAGLE_RENDER = 7

class Level:

    # Defaults

    DEFAULT_SIZE_X = 26
    DEFAULT_SIZE_Y = 26

    # Vars

    matrix = 0
    
    _sizeX = 0
    _sizeY = 0
    
    def __init__(self):
        self.__init__(self.DEFAULT_SIZE_X, self.DEFAULT_SIZE_Y)
    
    def __init__(self, sizeX, sizeY):
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