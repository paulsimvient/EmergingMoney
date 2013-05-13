import Tkinter
from Tkinter import *
import time

class log_window:
    def __init__(self,master):
        self.textframe = Tkinter.Frame(master)
        self.text = Text(self.textframe)
        self.text.pack()
        self.textframe.pack()
    def write(self,text):
        self.text.insert(END,text)

class some_func1: # This effectively waits 5 seconds then prints both lines at once
    def __init__(self,master):
        log.write("some text")
        time.sleep(5)
        log.write("some text")

class some_func2: # This prints the first object, waits 5 seconds, then prints the second
    def __init__(self,master):
        print "some text"
        time.sleep(1)
        print "some text"

if __name__ == '__main__':
    global log    
    root = Tk()
    log = log_window(root)
    root.after(100,some_func1, root)
    root.after(100,some_func2, root)
    root.mainloop()