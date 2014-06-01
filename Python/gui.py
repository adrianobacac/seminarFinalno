import tkinter
import tkinter.scrolledtext as tkst
from tkinter.constants import DISABLED, FLAT, NORMAL
from algorithm import ACAlgo
from tkinter import Canvas, Scrollbar

class wordFrame(tkinter.Frame):
    def __init__(self, parent, masterParent, word, pos):
        tkinter.Frame.__init__(self, parent)
        self.grid()
        self.parent=parent
        self.masterParent=masterParent
        self.positions=pos
        self.currentPosition=0
        self.word=word
        
        
        
        self.labelWordValue = tkinter.StringVar()
        self.labelWordValue.set(word)
        labelWord = tkinter.Label(self, textvariable=self.labelWordValue,bg="white", width=21, anchor="w")
        labelWord.grid(column=0, row=0, columnspan=4, sticky='NW')
        
        self.labelWordCounter = tkinter.StringVar()        
        self.labelWordCounter.set("   "+str(self.currentPosition)+"/"+str(len(self.positions)))
        labelPosCounter = tkinter.Label(self, textvariable=self.labelWordCounter,width=13, bg="white", anchor="w")
        labelPosCounter.grid(column=0, row=1, sticky='NW')
        
        
        
        buttonPrevious = tkinter.Button(self, text="<",relief=FLAT, bg="white", bd=1, command=self.previousHighlight)
        buttonPrevious.grid(column=1, row=1)
        
        buttonCurrent = tkinter.Button(self, text="O",relief=FLAT, bg="white", bd=1, command=self.currentHighlight)
        buttonCurrent.grid(column=2, row=1)
        
        buttonNext = tkinter.Button(self, text=">",relief=FLAT, bg="white", bd=1, command=self.nextHighlight)
        buttonNext.grid(column=3, row=1)
        
    def addTags(self):
        for pos in self.positions:
            self.parent.master.textBox.tag_add(self.word+str(pos), "1.0+%d chars" %(pos-1), "1.0+%d chars" %(pos+len(self.word)-1))
    
    def removeHighLight(self):
        for pos in self.positions:
            self.masterParent.textBox.tag_config(self.word+str(pos), background="white")    
           
    def highlightWord(self):
        if(len(self.positions)==0):
            return
        self.masterParent.removeHighlights()
        for pos in self.positions:
            self.parent.master.textBox.tag_config(self.word+str(pos), background="yellow")    
        self.parent.master.textBox.tag_config(self.word+str(self.positions[self.currentPosition]), background="orange")    
        
    def focusCurrent(self):
        self.parent.master.textBox.mark_set("insert", "1.0+%d chars" % self.currentPosition)
        self.updateCounter()
        
    def previousHighlight(self, event=""):
        if(len(self.positions)==0):
            return
        self.currentPosition=(self.currentPosition-1);
        if self.currentPosition<0:
            self.currentPosition=len(self.positions)+self.currentPosition
        self.highlightWord()
        self.focusCurrent()
        
    def currentHighlight(self, event=""):
        if(len(self.positions)==0):
            return
        self.highlightWord()
        self.focusCurrent()
        
    def nextHighlight(self, event=""):
        if(len(self.positions)==0):
            return
        self.currentPosition=(self.currentPosition+1)%len(self.positions);
        self.highlightWord()
        self.focusCurrent()
    
    def getWord(self):
        return self.word   
    
    def updateCounter(self):
        if(len(self.positions)>0):
            pom=1
        else:
            pom=0
        self.labelWordCounter.set("   "+str(self.currentPosition+pom)+"/"+str(len(self.positions)))
        self.update_idletasks()
        
    def updatePositions(self, pos):
        self.positions = pos
        self.updateCounter()
        
class simpleGui(tkinter.Tk):
    
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        self.grid()
        self.config(bg="white")
        self.geometry("600x500")
        
        self.algo = ACAlgo()
        self.wordFrames=[]
        
        self.path=""
        self.lastCanvasIndex=0
        
        rowLine=0
        
        
        self.entryPath = tkinter.Entry(self, width=75)
        self.entryPath.grid(column=0, row=rowLine,columnspan=3, sticky='NEW')
        self.entryPath.bind("<Return>", self.setPath)
        
        buttonSetPath = tkinter.Button(self, text="Set path", width=21, height=1, command=self.setPath)
        buttonSetPath.grid(column=3, row=rowLine, sticky='EWN')
                
                
                
        rowLine=rowLine+1
        
        self.entry = tkinter.Entry(self, width=75)
        self.entry.grid(column=0, row=rowLine,columnspan=2, sticky='NEWS')
        self.entry.bind("<Return>", self.addWords)

        buttonAddWords = tkinter.Button(self, text="Add words", width=21,height=1, command=self.addWords)
        buttonAddWords.grid(column=3, row=rowLine, sticky='EWNS')
        
        
        
        rowLine=rowLine+1
        self.grid_rowconfigure(rowLine, weight=1)
        self.textBox = tkst.ScrolledText(self, width=20, height=10)
        self.textBox.grid(column=0, row=rowLine, columnspan=3, sticky='NWES')
        
        self.textBox.config(state=DISABLED)
        
       
        self.canvas= Canvas(master=self,width=150)
        self.vscroll = Scrollbar(self)
        
        self.vscroll.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vscroll.set) 

        self.canvas.grid( row=rowLine, column=3,  sticky='NES')
        self.vscroll.grid(padx=1,  pady=1, row=rowLine, column=4, sticky='NEWS')
        
        
        
        rowLine=rowLine+1
                
        buttonClearHighlight = tkinter.Button(self, text="Clear highlight", width=20, command=self.removeHighlightsBtn)
        buttonClearHighlight.grid(column=0, row=rowLine, sticky="WS")


        buttonDeleteWords = tkinter.Button(self, text="Delete words", width=20, command=self.resetAll)
        buttonDeleteWords.grid(column=3, row=rowLine, sticky="ES")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def setPath(self):
        try:
            open(self.entryPath.get())
        except:
            return
        self.path=self.entryPath.get()
        self.textBox.config(state=NORMAL)
        self.textBox.insert(tkinter.INSERT, open(self.path).read())
        self.textBox.config(state=DISABLED)
        
    def removeHighlights(self):
        for wordFrame in self.wordFrames:
            wordFrame.removeHighLight()

    def removeHighlightsBtn(self, entry=""):
        for wordFrame in self.wordFrames:
            wordFrame.removeHighLight()
        
        self.update_idletasks()
            
    def resetAll(self, entry=""):
        self.removeHighlights()
        self.algo.resetTree()
        self.lastCanvasIndex=0;
        self.wordFrames=[]
        self.canvas.delete("all")
        self.update_idletasks()
        
    def addWords(self, event=""):
        if(self.path==""):
            return
        if(self.entry.get().strip()==""):
            self.entry.delete(0,len(self.entry.get()))
            return
        self.resetAll()
        for word in self.entry.get().split(" "):
            if word.lower() not in self.algo.foundWords.keys() and word != "" and word!=None:
                
                self.algo.addWord(word)
                self.addToCanvas(word)
                
                
        self.entry.delete(0,len(self.entry.get()))
        
        self.algo.addFails()
        
        self.algo.readFile(self.path)
        self.updateCanvasPositions();

    def updateCanvasPositions(self):
        
        for word in self.wordFrames:
            self.wordFrames[self.wordFrames.index(word)].updatePositions(self.algo.foundWords[word.getWord().lower()])
            self.wordFrames[self.wordFrames.index(word)].addTags()
            
    def addToCanvas(self, word):
             
        frame=wordFrame(self.canvas, self, word, self.algo.foundWords[word.lower()])
        self.wordFrames.append(frame)
        self.canvas.create_window(0, 50+self.lastCanvasIndex*50,anchor="w", window=frame, height=50)
            
                
        self.canvas.config(scrollregion=(0,0,70+self.lastCanvasIndex*50,70+self.lastCanvasIndex*50))
        self.canvas.update_idletasks()
        self.update_idletasks()
        
        self.lastCanvasIndex=self.lastCanvasIndex+1;

if __name__ == "__main__":
    app = simpleGui(None)
    app.title("Aco-corasick algorithm")
    app.mainloop()
    
