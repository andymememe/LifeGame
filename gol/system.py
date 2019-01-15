import abc, random

class System(abc.ABC):
    @abc.abstractmethod
    def __init__(self, h, w):
        'Initialize'
        return NotImplemented
        
    @abc.abstractmethod
    def load(self, inp):
        'Load map'
        return NotImplemented
 
    @abc.abstractmethod
    def step(self):
        'Next step'
        return NotImplemented
    
    @abc.abstractmethod
    def reset(self):
        'Reset Map'
        return NotImplemented
    
    @abc.abstractmethod
    def _draw(self):
        'Draw Map as String'
        return NotImplemented

class GameOfLife(System):
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.map = [0] * (h * w)
        self.map_ori = list(self.map)
 
    def load(self, inp):
        if len(inp) == len(self.map):
            for i in range(len(inp)):
                self.map[i] = inp[i]
            self.map_ori = list(self.map)
            return self._draw()
        else:
            raise ValueError("Input size ({}) must be"
                             "the same as Map size ({})"
                             .format(len(inp), len(self.map)))

    def step(self):
        temp = list(self.map)
        
        for y in range(self.h):
            for x in range(self.w):
                idx = x + y * self.w
                alive = 0
                if x - 1 >= 0:
                    if temp[(x - 1) + y * self.w] == 1:
                        alive = alive + 1
                    if y - 1 >= 0:
                        if temp[(x - 1) + (y - 1) * self.w] == 1:
                            alive = alive + 1
                    if y + 1 < self.h:
                        if temp[(x - 1) + (y + 1) * self.w] == 1:
                            alive = alive + 1
                if x + 1 < self.w:
                    if temp[(x + 1) + y * self.w] == 1:
                        alive = alive + 1
                    if y - 1 >= 0:
                        if temp[(x + 1) + (y - 1) * self.w] == 1:
                            alive = alive + 1
                    if y + 1 < self.h:
                        if temp[(x + 1) + (y + 1) * self.w] == 1:
                            alive = alive + 1
                if y - 1 >= 0:
                    if temp[x + (y - 1) * self.w] == 1:
                        alive = alive + 1
                if y + 1 < self.h:
                    if temp[x + (y + 1) * self.w] == 1:
                        alive = alive + 1
                
                if temp[idx] == 1:
                    if alive < 2 or alive > 3:
                        self.map[idx] = 0
                elif temp[idx] == 0:
                    if alive == 3:
                        self.map[idx] = 1
        return self._draw()
        
    def reset(self):
        self.map = list(self.map_ori)
        return self._draw()
    
    def _draw(self):
        text = ''
        for y in range(self.h):
            for x in range(self.w):
                item = self.map[x + y * self.w]
                if item == 1:
                    text = text + '*'
                elif item == 0:
                    text = text + ' '
                if x < self.w - 1:
                    text = text + ' '
            if y < self.h - 1:
                text = text + '\n'
        return text
            
        
class LangtonAnt(System):
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.map = [0] * (h * w)
        self.map[random.randint(0, h * w)] = random.randint(4, 11)
        self.map_ori = list(self.map)
 
    def load(self, inp):
        if len(inp) == len(self.map):
            for i in range(len(inp)):
                self.map[i] = inp[i]
            self.map_ori = list(self.map)
            return self._draw()
        else:
            raise ValueError("Input size ({}) must be"
                             "the same as Map size ({})"
                             .format(len(inp), len(self.map)))

    def step(self):
        '''
        0: White
        1: Black
        White:
            4 :^
            5 :v
            6 :<
            7 :>
        Black:
            8 :^
            9 :v
            10:<
            11:>
        '''
        temp = list(self.map)
        
        for y in range(self.h):
            for x in range(self.w):
                idx = x + y * self.w
                if temp[idx] > 1:
                    if temp[idx] > 3 and temp[idx] < 8:
                        self.map[idx] = 1
                    elif temp[idx] > 7:
                        self.map[idx] = 0
                    
                    if ((temp[idx] % 4) == 0 and temp[idx] < 8) or\
                       ((temp[idx] % 4) == 1 and temp[idx] > 7):
                        if (x + 1) < self.w:
                            nxtI = idx + 1
                            self.map[nxtI] = (self.map[nxtI] + 1) * 4 + 3
                    elif ((temp[idx] % 4) == 1 and temp[idx] < 8) or\
                         ((temp[idx] % 4) == 0 and temp[idx] > 7):
                        if (x - 1) >= 0:
                            nxtI = idx - 1
                            self.map[nxtI] = (self.map[nxtI] + 1) * 4 + 2
                    elif ((temp[idx] % 4) == 2 and temp[idx] < 8) or\
                         ((temp[idx] % 4) == 3 and temp[idx] > 7):
                        if (y + 1) < self.h:
                            nxtI = idx - self.w
                            self.map[nxtI] = (self.map[nxtI] + 1) * 4
                    elif ((temp[idx] % 4) == 3 and temp[idx] < 8) or\
                         ((temp[idx] % 4) == 2 and temp[idx] > 7):
                        if (y - 1) >= -1:
                            nxtI = idx + self.w
                            self.map[nxtI] = (self.map[nxtI] + 1) * 4 + 1
                    return self._draw()
        return self._draw()
        
    def reset(self):
        self.map = list(self.map_ori)
        return self._draw()
    
    def _draw(self):
        text = ''
        for y in range(self.h):
            for x in range(self.w):
                item = self.map[x + y * self.w]
                if item == 0:
                    text = text + ' '
                elif item == 1:
                    text = text + '*'
                elif item > 1:
                    if (item % 4) == 0:
                        text = text + '^'
                    elif (item % 4) == 1:
                        text = text + 'v'
                    elif (item % 4) == 2:
                        text = text + '<'
                    elif (item % 4) == 3:
                        text = text + '>'
                if x < self.w - 1:
                    text = text + ' '
            if y < self.h - 1:
                text = text + '\n'
        return text