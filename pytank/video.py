from sdl2 import *
from ctypes import c_long, pointer

class Video:
    def __init__(self, window, w, h):
        self._window = window
        self._renderer = SDL_CreateRenderer(self._window.window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_TARGETTEXTURE);
        self._buffer = SDL_CreateTexture(self._renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, w, h);
                  
    def renderStart(self):
    
        # Clear renderer
        
        SDL_SetRenderTarget(self._renderer, self._buffer);
        SDL_RenderClear(self._renderer);

    def renderStop(self):
    
        # Present renderer
        
        SDL_SetRenderTarget(self._renderer, None)
        SDL_RenderCopy(self._renderer, self._buffer, None, None, 0, None, 0);
        SDL_RenderPresent(self._renderer); 
          
    def clear(self, r = 0,g = 0 ,b = 0):
        
        SDL_SetRenderDrawColor(self._renderer,r,g,b, 255);
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
        
    def loadTexture(self, path):
        surface = SDL_LoadBMP(path);
        texture = SDL_CreateTextureFromSurface(self._renderer, surface);
        return texture


        