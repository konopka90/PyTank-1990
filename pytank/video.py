from sdl2 import *
from sdl2.ext import *
from sdl2.sdlimage import *
from gameVars import *
from ctypes import c_long, pointer
from colors import *

class Video:
    def __init__(self, window, w, h):
        self._window = window
        self._renderer = SDL_CreateRenderer(self._window.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_TARGETTEXTURE);
        self._buffer = SDL_CreateTexture(self._renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, w, h);
        self.CHARACTER_WIDTH = 8
        
        # Assets        
        
        self._blackFont = self.loadTexture("pytank/data/font.png")
        self._whiteFont = self.loadTexture("pytank/data/font_white.png")
        self._blackDigits = self.loadTexture("pytank/data/digits.png")
        self._whiteDigits = self.loadTexture("pytank/data/digits_white.png")
        self._digits = self.loadTexture("pytank/data/digits.png")

        
        
    def renderStart(self):
    
        # Clear renderer
        
        SDL_SetRenderTarget(self._renderer, self._buffer);
        SDL_RenderClear(self._renderer);

    def renderStop(self):
    
        # Present renderer
        
        SDL_SetRenderTarget(self._renderer, None)
        SDL_RenderCopy(self._renderer, self._buffer, None, None, 0, None, 0);
        SDL_RenderPresent(self._renderer); 
          
    def clear(self, color = Color(0,0,0)):
        
        SDL_SetRenderDrawColor(self._renderer,color.r,color.g,color.b, 255);
        SDL_RenderClear(self._renderer);
        
    def drawRect(self,color,x,y,w,h):
    
        r = SDL_Rect(x, y, w, h) 
        SDL_SetRenderDrawColor(self._renderer, color.r,color.g, color.b,255) 
        SDL_RenderFillRect(self._renderer, r) 
        
    def render(self, texture, x, y, src = SDL_Rect(-1,-1,-1,-1)):
    
        # Setup
    
        _w = pointer(c_long(0))
        _h = pointer(c_long(0))
        dst = SDL_Rect(x, y)
        
        SDL_QueryTexture(texture, None, None, _w, _h);
    
        dst.w = _w.contents.value
        dst.h = _h.contents.value
        
        if src.x != -1:
            dst.w = src.w
            dst.h = src.h
        else:
            src = None
            
        # Render to the texture
            
        SDL_SetRenderTarget(self._renderer, self._buffer);
        SDL_RenderCopy(self._renderer, texture, src, dst);
        SDL_SetRenderTarget(self._renderer, None);
        
    def renderText(self, text, color, x, y):

    
        SDL_SetRenderTarget(self._renderer, self._buffer);
        
        dst = SDL_Rect(x, y, 9, 8)
        src = SDL_Rect(0,0,self.CHARACTER_WIDTH ,8)
        text = text.upper()
        counter = 0                        
                
                
        for c in text:
            if str(c).isalpha():
                
                # Do math                
                
                ref = ord('A')
                current = ord(c)
                diff = current - ref

                # Set source and destination                
                # Fucking 9 pixels in first char d(-_-)b
                src.x = 9 + diff * self.CHARACTER_WIDTH;
                dst.x = x + counter*(self.CHARACTER_WIDTH + 1)
                
                if color == Colors.WHITE_ENUM:
                    SDL_RenderCopy(self._renderer, self._whiteFont, src, dst);
                else:
                    SDL_RenderCopy(self._renderer, self._blackFont, src, dst);
                    
                
                pass
            else:
                if str(c).isdigit():
                    ref = ord('0')
                    current = ord(c)
                    diff = current - ref
                    
                    src.x = diff * self.CHARACTER_WIDTH;
                    dst.x = x + counter*(self.CHARACTER_WIDTH + 2)
                    
                    if color == Colors.WHITE_ENUM:
                        SDL_RenderCopy(self._renderer, self._whiteDigits, src, dst);
                    else:
                        SDL_RenderCopy(self._renderer, self._blackDigits, src, dst);
                    
                    pass
                else:
                    
                    if c == ' ':
                        pass
                    
                    pass
                
            counter = counter + 1
            pass
        
        
        SDL_SetRenderTarget(self._renderer, None);

        pass
        
    def loadTexture(self, path):
        surface = IMG_Load(path)
        texture = SDL_CreateTextureFromSurface(self._renderer, surface);
        return texture


        