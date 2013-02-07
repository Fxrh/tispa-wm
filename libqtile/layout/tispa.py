from libqtile.layout.base import Layout
import dbus


class TispaLayout(Layout):
    def __init__(self, **config):
        Layout.__init__(self, **config)
        self.rows = 2;
        self.columns = 2;
        self.windows = [];
        self.toReplace = -1;
        
    def _calcPosForWin( self, pos, screen ):
        width = screen.width // self.columns
        height = screen.height // self.rows
        x = (pos % self.columns) * width
        y = (pos // self.columns) * height 
        return (x, y, width, height)
    
    def add( self, c ):
        self.windows.append(c)
    
    def remove( self, c ):
        self.windows.remove(c)
    
    def configure( self, c, screen ):
        pos = self.windows.index(c)
        if pos >= self.rows*self.columns:
            if self.toReplace == -1:
                c.kill()
                return
            else:
                c2 = self.windows[self.toReplace]
                self.windows[self.toReplace], self.windows[pos] = self.windows[pos], self.windows[self.toReplace]
                c2.kill()
                self.toReplace = -1
        (x, y, width, height) = self._calcPosForWin( pos, screen )
        c.place( x, y, width, height, 0, 0, False, True, True );
        c.unhide()

    def focus_first(self):
        return None

    def focus_next(self, win):
        return None

    def focus_last(self):
        return None

    def focus_prev(self, win):
        return None
        
    def killTop(self):
        if len(self.windows) != 0:
            self.windows[-1].kill()
    
    def setToReplace(self, num):
        if num < self.rows*self.columns:
            self.toReplace = num
            
        


        