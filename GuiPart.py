import tkinter.filedialog
from tkinter import *

from tkinter.scrolledtext import ScrolledText

import FileOpener
import os
import MyStack

class GUI :

    def __init__(self , fileopen=FileOpener.fileOpener() ):

        self.command =[]
        self.cIndex = 0
        self.cEnd = 0

        self.fileopen = fileopen

        self.path = None
        self.root = tkinter.Tk()
        self.frame = Frame(self.root)
        self.frame.pack()

        self.frame1 = Frame(self.frame)
        self.frame1.pack()

        self.frame2 = Frame(self.frame)
        self.frame2.pack(side=BOTTOM)

        self.frame8 = Frame(self.frame1)
        self.frame8.pack(side=BOTTOM)

        self.frame3 = Frame(self.frame1)
        self.frame3.pack()

        self.frame4 = Frame(self.frame8)
        self.frame4.pack(side=LEFT)

        self.frame5 = Frame(self.frame2)
        self.frame5.pack()

        self.frame6 = Frame(self.frame2)
        self.frame6.pack(side=BOTTOM)

        self.frame7 = Frame(self.frame8)
        self.frame7.pack(side=RIGHT)

        self.frame9 = Frame(self.frame6)
        self.frame9.pack(side=LEFT)

        self.frame10 = Frame(self.frame6)
        self.frame10.pack(side=RIGHT)

        self.guiMake()
        self.root.mainloop()


    def close_window(self):
        self.root.destroy()

    def buildTree (self) :
        if self.var.get()==1 or (self.var.get()==2) or (self.var.get()==3) or (self.var.get()==4) :
            self.fileopen.openDir(self.path, self.getTreeType() , self.scrolltext )

    def showChooseFile (self) :
        #currdir = "\home\mahtab\Documents\docs"
        currdir = os.getcwd()
        self.path = tkinter.filedialog.askdirectory(parent=self.root, initialdir=currdir, title='Please select a directory' )
        print("fresh path :" , self.path)
        if len(self.path)>0 :
            self.set_text("")
            self.set_text(self.path)
        return


    def set_text(self , text):
       self.E1.insert(0,text)
       return
    def getPath (self) :
        return self.E1.get()
    def getTreeType (self ):
        return self.var.get()
    def commandIndex(self, str):
        words = str.lower().split()
        if words[0] is not None and words[1] is not None:
            if words[0] == "add":
                self.fileopen.addFile(words[1] , self.getTreeType() , self.scrolltext , 1)
            if words[0] == "del":
                self.fileopen.deleteFile(self.scrolltext , self.getTreeType() , words[1])
            if words[0] == "update":
                self.fileopen.updateFile(words[1] , self.getTreeType() , self.scrolltext)
            if words[0] == "list":
                if words[1] == "-w":
                    self.fileopen.listAllWord(self.getTreeType() , self.scrolltext )
                if words[1] == "-l":
                    self.fileopen.listTreeFile(self.scrolltext)
                if words[1] == "-f":
                    self.fileopen.listfile(self.scrolltext)
            if words[0] == "search":

                if words[1] == "-s":
                    t= len(words)
                    str =""
                    for i in range(2 , t):
                        if i ==2 :
                            w = words[2]
                            e = len(w)
                            str = w[1:e]
                        elif i == t-1 :
                            w= words[t-1]
                            e =len(w)
                            str += w[0:e-1]
                        else :
                            str += words[i]
                        str += " "
                    print("str  : " , str )
                    self.fileopen.searchLine(str , self.getTreeType() , self.scrolltext)
                if words[1] == "-w":
                    w = words[2]
                    e = len(w) - 1
                    self.fileopen.searchWord(w[1 : e] , self.getTreeType() , self.scrolltext)
        else :
            print("err")

    def arrowkeyUp (self ,event  ) :

        if self.cIndex>0 :
            print("up")
            self.cIndex -= 1
            self.E2.delete(0, END)
            self.E2.insert(0, self.command[self.cIndex])

    def arrowkeyDown (self , event) :

        if self.cIndex < self.cEnd and len(self.command) > self.cIndex :
            print("down")
            self.cIndex+=1
            self.E2.delete(0,END)
            self.E2.insert(0,self.command[self.cIndex])
    def writeList (self ,event) :
        self.scrolltext.insert(END ,">>"+self.E2.get() + "\n")
        self.command.append(self.E2.get())
        self.cIndex +=1
        self.cEnd = self.cIndex
        self.scrolltext.update_idletasks()
        self.commandIndex(self.E2.get())
        self.E2.delete(0, 'end')
        return

    def guiMake (self) :
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        print("h , w: " , width , height)
     #   h =  height/16
     #   w = width / 16
        self.label1 = Label(self.frame1, text="\nPlease enter folder adress or use browse button\n", height=4, font=17)
        self.label1.pack()

        self.E1 = Entry(self.frame1, bd=3, width=120, font=10)
        self.E1.pack(side=LEFT)

        self.redbutton = Button(self.frame1, text="Browse", font=10, command=self.showChooseFile)
        self.redbutton.pack()

        self.scrolltext = ScrolledText(self.frame4 , font=10 ,width =118 , height = 30 )
        self.scrolltext.pack(side=LEFT, fill=BOTH)

        self.var = IntVar()
        self.R1 = Radiobutton(self.frame8, text="TST", variable=self.var, value=1, font=20)
        self.R1.pack(anchor=W)

        self.R2 = Radiobutton(self.frame8, text="BST", variable=self.var, value=2, font=20)
        self.R2.pack(anchor=W)

        self.R3 = Radiobutton(self.frame8, text="Trie", variable=self.var, value=3, font=20)
        self.R3.pack(anchor=W)

        self.R4 = Radiobutton(self.frame8, text="Hash", variable=self.var, value=4, font=20)
        self.R4.pack(anchor=W)

        self.label3 = Label(self.frame5, text="\nPlease enter your command:", height=4, font=17)
        self.label3.pack()

        self.E2 = Entry(self.frame5, bd=3, width=110, font=10 )
        self.E2.pack(side=BOTTOM)
        self.E2.bind('<Return>', self.writeList)
        self.E2.bind('<Up>' , self.arrowkeyUp)
        self.E2.bind('<Down>' , self.arrowkeyDown)

        self.redbutton1 = Button(self.frame9, text="Build", font=10 , command = self.buildTree)
        self.redbutton1.pack(side=LEFT)

        self.redbutton2 = Button(self.frame9, text="Reset", font=10)
        self.redbutton2.pack(side=RIGHT)

        self.redbutton3 = Button(self.frame10, text="Help", font=10)
        self.redbutton3.pack(side=LEFT)

        self.redbutton4 = Button(self.frame10, text="Exit", font=10  ,command = self.close_window)

        self.redbutton4.pack(side=RIGHT)
        return


