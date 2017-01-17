from tkinter import END

import MyStack
import glob
import Word
import BST
import os
import  ntpath
import Trie
import TST
import fnmatch
import time
import hash
class fileOpener :
    def __init__(self):
        self.stack = MyStack.Stack()
        self.bst = BST.BinarySearchTree(self)
        self.trie = Trie.MyTrie(self)
        self.tst = TST.MyTST(self)
        self.hash = hash.Hash(self)
        self.address = None
        f = open(os.getcwd() + "/stopWord.txt", 'r')
        str = f.read(-1)
        self.stopW = str.split()
    def writeList(self, showList , str ) :
        showList.insert(END, str  )
        showList.insert(END, "\n")
        showList.update_idletasks()
    def readFile (self , filename , treeType , p):
        # open file and insert in tree
        if not p==0 :
            self.stack.push(ntpath.basename(filename))
        f = open(filename, 'r')
        str = f.read(-1)
        words = str.split()  # split word by space
        for w in words:
            if (not self.isStopWord(w)):
                if treeType == 2:
                    wNode = Word.myWord(w.lower(), ntpath.basename(filename))
                    self.bst.insertChild(self.bst.root, BST.Node(wNode))
                if treeType == 3:
                    self.trie.insertChild(w.lower(), ntpath.basename(filename))
                if treeType == 1:
                    self.tst.insertChild(self.tst.root, w.lower(), ntpath.basename(filename), 0)
                if treeType == 4 :
                    self.hash.insertChild(w.lower() ,ntpath.basename(filename) )
        f.close()
    def existFile(self , filename):
        for root, dirnames, filenames in os.walk(self.address):
            for file in fnmatch.filter(filenames, '*.txt'):
                if filename == file:
                    return True
        return False
    def addFile (self, filename ,treeType, showList , p):
        # add file
        if p== 0 :
            self.readFile(self.address + "/" + filename, treeType, p)
            return
        if filename in self.stack.items :
            self.writeList(showList , "err : already exists, you may want to update.")
            return
        check = self.existFile(filename)
        if check :
            self.readFile(self.address+"/"+filename , treeType , p)
            self.writeList(showList , filename+ " successfully added.")
        else:
            self.writeList(showList, "err : document not found.")
            return


    def openDir(self, str , treeType  , listShow) :
        #open directory recursively and build tree
        counter =0
        start_time = time.time()
        self.address = str
        self.stack.deleteStack()
        print("path : " + str)
        if treeType == 2:
            if self.bst.root is None:
                pass
            else :
                #delete last Bst !!!!!
                pass
      #  for filename in glob.iglob(str + '/**/*.txt', recursive=True):
        matches = []
        for root, dirnames, filenames in os.walk(str):

            for filename in fnmatch.filter(filenames, '*.txt'):
                matches.append(root + "/" + filename)
        for filename in matches:
            self.readFile(filename , treeType , 1 )
            counter +=1
            print("c : " , counter )
        self.writeList(listShow , "tree Built")
        print("openning file")
        print("--- %s seconds ---" % (time.time() - start_time))
        if (treeType== 2 ):
            self.bst.AVL()
        if (treeType==1 ):
            self.tst.AVL()
        return
    def deleteFile (self, showList , treeType , filename) :
        check = self.existFile(filename)
        if check :
            path  = self.address + "/" + filename
            f = open(path , 'r')
            str = f.read(-1)
            words = str.split()  # split word by space
            for w in words:
                if (not self.isStopWord(w)):
                    if treeType == 2:
                        self.bst.deleteNode(w.lower()  ,filename,showList )
                    if treeType == 3:
                        self.trie.deleteNode(w.lower() , filename , showList)
                    if treeType == 1:
                        self.tst.deleteNode(w.lower() , filename, showList)
                    if treeType ==4 :
                        self.hash.deleteNode(w.lower() , filename , showList)
            f.close()
            list = self.stack.items
            for i in range(0, len(list)) :
                if list[i] == filename :
                    del list[i]
                    break
            self.writeList(showList ,filename +" successfully removed from lists.")
        else :
            self.writeList(showList , "err: document not found.")
            return
    def updateFile(self , filename ,treeType , listShow ) :

        check = self.existFile(filename)
        if filename in self.stack.items:
            path = self.address + "/" + filename
            f = open(path, 'r')
            str = f.read(-1)
            words = str.split()  # split word by space
            for w in words:
                if (not self.isStopWord(w)):
                    if treeType == 2:
                        self.bst.updeateNode(filename , listShow)
                    if treeType == 3:
                        self.trie.updeateNode(filename , listShow)
                    if treeType == 1:
                        self.tst.updeateNode(filename , listShow)
            f.close()
            self.addFile(filename, treeType, listShow , 0 )
            self.writeList(listShow, filename + " successfully updated.")
        else:
            self.writeList(listShow, "err: document not found.")

    def isStopWord (self ,word ) :

        if not word.isalpha():
            return True

        for w in self.stopW :
            if w.lower() == word.lower() :
                return True
        return False
    def listfile (self , showList):
        #for python 3.5 :
      #  for filename in glob.iglob(self.address + '/**/*.txt', recursive=True):
       #     print(ntpath.basename(filename), " , " , end="" , flush=True)

        s = ""
        counter = 0
        for root, dirnames, filenames in os.walk(self.address):

            for filename in fnmatch.filter(filenames, '*.txt'):
                s = s + "  " + filename
                counter +=1
        self.writeList(showList , s)
        self.writeList(showList , "Number of all docs = " + str(counter))
    def listTreeFile(self , showList) :
        s = ""
        counter = 0
        for i in self.stack.items :
            s = s + "  " + i
            counter +=1
        self.writeList(showList , s)
        self.writeList(showList, "Number of listed docs = " + str(counter) )
    def listAllWord (self , treeType , listShow) :
        # command list -w
        start_time = time.time()
        if treeType==1 :
            self.tst.wordNum =0
            self.tst.visit(self.tst.root.mid , "" , listShow , "" , 1)
            self.writeList(listShow , "Number of words =" + str(self.tst.wordNum))
        if treeType==2 :
            self.bst.wordNum =0
            self.bst.in_order_print(self.bst.root , listShow ,"" , 1)
            self.writeList(listShow, "Number of words =" + str(self.bst.wordNum))
        if treeType==3 :
            self.trie.wordNum=0
            self.trie.visit(self.trie.root , "" , listShow , "" , 1 )
            self.writeList(listShow, "Number of words =" + str(self.trie.wordNum))
        if treeType==4 :
            self.hash.wordNum =0
            self.hash.visit(listShow ,"" ,1 )
            self.writeList(listShow, "Number of words =" + str(self.hash.wordNum))
        print("list -w")
        print("--- %s seconds ---" % (time.time() - start_time))
    def searchWord (self ,word , treeType , listShow) :
        #command search -w ""
        start_time = time.time()
        print("w : " , word)
        if treeType==1 :
            self.tst.searchOneWord(word , 1 , listShow)
        if treeType==2 :
            self.bst.searchOneWord(self.bst.root , word , 1 ,listShow ,"")
        if treeType==3 :
            self.trie.searchOneWord(word,1 ,listShow)
        if treeType ==4 :
            self.hash.searchOneWord(word ,1 , listShow)
        print ("time for search one word : ")
        millis = int(round(time.time() * 1000))
        millis2 =int (round ( start_time*1000))
        print("--- %s seconds ---" % (millis -millis2))
    def searchLine (self , line , treeType , listShow) :
        #command search -S ""
        start_time = time.time()
        if treeType==1 :
            self.tst.searchOneLine(line , self.stopW , listShow)
        if treeType==2 :
            self.bst.searchOneLine(line , self.stopW , listShow)
        if treeType==3 :
            self.trie.searchOneLine(line , self.stopW , listShow)
        if treeType==4 :
            self.hash.searchOneLine(line , self.stopW , listShow)
        print("time for search one line : ")
        millis = int(round(time.time() * 1000))
        millis2 = int(round(start_time * 1000))
        print("--- %s seconds ---" % (millis - millis2))