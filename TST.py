from tkinter import END


class Node :
    def __init__(self , char , endWord ):
        self.char = char
        self.Rc = None
        self.Lc = None
        self.mid = None
        self.word = endWord
        self.address = []

class MyTST :
    def __init__(self ,fileOpen):
        self.fileOpen = fileOpen
        self.listfileSearch = []
        self.root = Node ("" , [] )
        self.wordNum = 0
        self.delList = []

    def insertChild (self , node ,  word , address  , d )  :
        #add node recursive
        char = word[d]
        if (node is None) :
            node = Node(char, [])
            node.address.append(address)
        if node.char == "" :
            node.mid = self.insertChild(node.mid, word, address, d )
        elif char < node.char :
            node.Lc = self.insertChild(node.Lc , word , address , d)
        elif  char > node.char :
            node.Rc = self.insertChild(node.Rc , word , address , d)
        elif d < len(word)-1 :
            node.mid = self.insertChild(node.mid , word , address , d+1)
        else :
            node.word = word
            if not address in node.address :
                 node.address.append(address)
        return node

    def visit(self, reroot, ch , listShow , filename , p):

        if reroot is not None :
            if reroot.Lc is not None :
                self.visit(reroot.Lc , ch , listShow , filename , p)
            if reroot.Rc is not None:
                self.visit(reroot.Rc, ch , listShow, filename , p)
            if reroot.mid is not None :
                self.visit(reroot.mid , ch+reroot.char ,listShow , filename , p)
            if reroot.word:
                if p==1 :
                    #print all node
                    s = reroot.word
                    str2 = " -> "
                    s = s + str2
                    for a in reroot.address:
                        s = s + "  " + a
                    if  s.split() :
                        self.fileOpen.writeList(listShow, s)
                    self.wordNum +=1
                elif p==2 :
                    #update node
                    counter = 0
                    for f in reroot.address:
                        if f == filename:
                            reroot.address.pop(counter)
                            break
                        counter += 1
                    return

    def reSearchW(self, reroot, word , realW , p , filename  ,listShow):

        # search word recursive
        if not word  or reroot is None :
            self.listfileSearch = []
            self.fileOpen.writeList(listShow, "cant find")
            return
        if word[0] < reroot.char :
            return self.reSearchW(reroot.Lc , word , realW , p, filename , listShow)
        elif word[0] > reroot.char :
            return self.reSearchW(reroot.Rc , word , realW , p , filename , listShow)
        else :
            if reroot.word == realW :
                if p==2 :
                    self.delList.append(reroot)
                if p==1 :
                    str =""
                    first = 0
                    for a in reroot.address :
                        if first ==1 :
                            str = str + " , " + a
                        else:
                            first =1
                            str= a
                    self.fileOpen.writeList(listShow , str )
                    self.listfileSearch = reroot.address
                    return reroot
                elif p==2 :
                    counter = 0
                    for f in reroot.address :
                        if f == filename :
                            reroot.address.pop(counter)
                            if len(reroot.address) == 0:
                                for d in self.delList[::-1] :
                                    if (d.mid is None)and (d.Lc is None)and (d.Rc is None) :
                                        del d
                                    else :
                                        self.delList[-1].word = None
                                        break

                                for d in self.delList :
                                    for a in d.address :
                                        if a ==filename :
                                            del a
                                            break
                                del self.delList[:]
                            break
                        counter +=1
                else :
                    self.listfileSearch = reroot.address
                    return reroot
            else :
                return self.reSearchW(reroot.mid, word[1:], realW , p , filename , listShow)

    def searchOneWord(self , word ,p  ,listShow):
        #call search word function
        return self.reSearchW(self.root.mid , word , word ,p , "" , listShow)
    def isStopWord(self, word, stopwords):
        #chack stopword
        if not word.isalpha():
            return True
        for w in stopwords:
            if w.lower() == word.lower():
                return True
        return False
    def searchOneLine(self, line , stopword , listShow ):
        # search line with function search word and then return th intersect of lists
        first = 1
        list1 = []
        for w in line.split():
            if (not self.isStopWord(w, stopword)):
                if first == 1:
                    self.searchOneWord(w, 0 ,listShow)
                    list1 = self.listfileSearch
                    first = 0
                else:
                    self.searchOneWord(w,0, listShow)
                    list2 = self.listfileSearch
                    list1 = list(set(list1).intersection(list2))
        str = "answer : "
        for a in list1 :
            str = str + "  " + a
        self.fileOpen.writeList(listShow, str)

    def deleteNode(self, word, filename, listShow) :
        print("w : " , word )
        self.reSearchW(self.root.mid , word , word , 2 , filename , listShow)

    def updeateNode (self,filename , listshow ) :
        self.visit(self.root.mid , "" , listshow , filename ,2 )