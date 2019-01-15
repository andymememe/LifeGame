import sys, random
import tkinter as tk
from tkinter.font import Font
from tkinter import filedialog
from gol.system import GameOfLife, LangtonAnt

class Application(tk.Frame):
    def __init__(self, master, system, fps=5):
        super().__init__(master)
        self.system = system
        self.delay_ms = int(1000 / fps)
        self.state = 0
        self.nstep = 0
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Frame
        ## Output Frame
        self.optFrame = tk.Frame(self)
        self.optFrame.pack(side=tk.TOP, fill=tk.BOTH)
        
        ## Count Frame
        self.cntFrame = tk.Frame(self)
        self.cntFrame.pack(side=tk.TOP, fill=tk.BOTH)
        
        ## Button Frame
        self.btnFrame = tk.Frame(self)
        self.btnFrame.pack(side=tk.TOP, fill=tk.BOTH)
        
        # Output
        labelFont = Font(family="consolas", size=12)
        self.map = tk.StringVar()
        self.opt = tk.Label(self.optFrame,
                            textvariable=self.map,
                            bg="white",
                            font=labelFont)
        self.map.set(self.system.reset())
        self.opt.pack()
        
        # Count
        self.cnt = tk.StringVar()
        self.count = tk.Label(self.cntFrame,
                              textvariable=self.cnt,
                              font=labelFont)
        self.cnt.set("Step: {}".format(self.nstep))
        self.count.pack(side=tk.BOTTOM)
        
        # Button
        ## Load Button
        self.loadBtn = tk.Button(self.btnFrame,
                                 text="Load",
                                 command=self.load,
                                 font=labelFont)
        self.loadBtn.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        
        ## Step Button
        self.stepBtn = tk.Button(self.btnFrame,
                                 text="Step",
                                 command=self.step,
                                 font=labelFont)
        self.stepBtn.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        
        ## Play Button
        self.stateTxt = tk.StringVar()
        self.playBtn = tk.Button(self.btnFrame,
                                 textvariable=self.stateTxt,
                                 command=self.play,
                                 font=labelFont)
        self.stateTxt.set("Play")
        self.playBtn.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        
        ## Reset Button
        self.resetBtn = tk.Button(self.btnFrame,
                                  text="Reset",
                                  command=self.reset,
                                  font=labelFont)
        self.resetBtn.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
    
    def load(self):
        filetypes = (("text file", "*.txt"),)
        filename = tk.filedialog.askopenfilename(initialdir="./Map",
                                                 title="Select map file",
                                                 filetypes=filetypes)
        inp = [0] * (self.system.h * self.system.w)
        try:
            with open(filename, 'r') as f:
                for line in f:
                    data = line.strip().split('\t')
                    x = int(data[0]) - 1
                    y = int(data[1]) - 1
                    if 'A' in line:
                        c = int(data[2])
                        if c < 4 or c > 11:
                            c = random.randint(4, 11)
                        inp[x + y * self.system.w] = c
                    else:
                        inp[x + y * self.system.w] = 1
            self.map.set(self.system.load(inp))
            self.nstep = 0
            self.cnt.set("Step: {}".format(self.nstep))
        except:
            print('Illegal input file!')
    
    def step(self):
        self.map.set(self.system.step())
        self.nstep = self.nstep + 1
        self.cnt.set("Step: {}".format(self.nstep))
    
    def play(self):
        if self.state == 0:
            self.state = 1
            self.stateTxt.set("Stop")
            self.loadBtn.config(state="disabled")
            self.stepBtn.config(state="disabled")
            self.resetBtn.config(state="disabled")
            
            self.opt.after(0, self._playTask)
        elif self.state == 1:
            self.state = 0
            self.stateTxt.set("Play")
            self.loadBtn.config(state="normal")
            self.stepBtn.config(state="normal")
            self.resetBtn.config(state="normal")
    
    def reset(self):
        self.map.set(self.system.reset())
        self.nstep = 0
        self.cnt.set("Step: {}".format(self.nstep))
    
    def _playTask(self):
        if self.state == 1:
            self.step()
            self.opt.after(self.delay_ms, self._playTask)
    
def main():
    if len(sys.argv) >= 2:
        opt_sys = sys.argv[1]
    else:
        opt_sys = 'gol'
    
    if opt_sys == 'gol':
        title = 'Game of Life'
        gameSys = GameOfLife(16, 16)
    elif opt_sys == 'ant':
        title = 'Langton\'s Ant'
        gameSys = LangtonAnt(16, 16)
    else:
        print('Unknown system {}, using Game of Life.'.format(opt_sys))
        title = 'Game of Life'
        gameSys = GameOfLife(16, 16)
    
    root = tk.Tk()
    root.title(title)
    root.geometry("512x450")
    root.resizable(0, 0)
    
    app = Application(root, gameSys)
    app.pack_propagate(0)
    app.pack(fill=tk.BOTH, expand=1)
    app.mainloop()

if __name__ == '__main__':
    main()