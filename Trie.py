from tkinter import END

class Node :
    def __init__(self , dWord , flag ):
        self.data = dWord
        self.Rc = None
        self.Lc = None
        self.next = None
        self.flag = flag
        self.address = []

class MyTrie :
    def __init__(self ,fileOpen ):
        self.root = Node("" ,0 )
        self.listfileSearch = []
        self.fileOpen = fileOpen
        self. wordNum = 0
        self.delList = []

    def insertChild(self , word ,address ):
        #add node
        count =1
        end =0 ;
        current = self.root
        for c in word.lower() :
            if (count == len(word)) :
                end = 1 ;
            if(current.Lc is None) :
                current.Lc = Node(c,end )
                if (end ==1 ):
                    current.Lc.address.append(address)
                current = current.Lc
            elif (current.Rc is None) and (c != current.Lc.data) :
                current.Rc = Node(c, end)
                if (end ==1 ) :
                   current.Rc.address.append(address)
                current.Lc.next= current.Rc
                current = current.Rc
            else :
                cur2= current.Lc
                x= 0
                while(cur2 is not None ) :
                    if(cur2.data == c) :
                        x=1
                        if not address in cur2.address :
                            if (end ==1 ) :
                              cur2.address.append(address)
                        current = cur2
                        break
                    cur2 = cur2.next
                if x ==0 :
                    c= Node (c,end)
                    current.Rc.next = c
                    current.Rc = c
                    current = c
            count +=1
    def visit (self, reroot , ch  , listShow ,filename , p):

        if reroot is not None  :
            ch= ch + reroot.data
            if(reroot.flag == 1) :
                if p==1 and reroot.address :
                    #for print all of tree nodes
                    s = ch + ' -> '

                    for a in reroot.address :
                        s = s + "  " + a
                    self.fileOpen.writeList(listShow , s)
                    self.wordNum +=1
                elif p==2 :
                    #for updating list
                    counter =0
                    for a in reroot.address :
                        if a ==filename  :
                            reroot.address.pop(counter)
                            if len(reroot.address) == 0:
                                reroot.flag = 0
                            break
                        counter +=1
            current = reroot.Lc
            while (current is not None):
                self.visit(current, ch , listShow, filename ,p)
                current = current.next
    def  reSearchW (self , reroot , word , realW , p , listShow , filename  ) :
        # search word recursive
        ch= word[0]
        if ch == reroot.data :
            if p ==2 :
                self.delList.append(reroot)
            if not word[1:]:
                if p==1 :
                    first = 0
                    str =""
                    for a in reroot.address :
                        if first ==1 :
                            str = str + " , " + a
                        else:
                            first =1
                            str= a
                    self.fileOpen.writeList(listShow , str)
                    self.listfileSearch = reroot.address
                    return reroot
                elif p==2 :
                    counter = 0
                    for f in reroot.address:
                        if f == filename:
                            reroot.address.pop(counter)
                            if len(reroot.address)==0 :
                              #  reroot.flag = 0
                                for d in self.delList[::-1] :
                                    if (d.Lc is None):
                                        del d
                                    elif (d.Lc is not None) :
                                        d.flag = 0
                                        break
                                for d in self.delList :
                                    for a in d.address :
                                        if a ==filename :
                                            del a
                                            break
                                del self.delList[:]
                            break
                        counter += 1
                    del reroot
                else:
                    self.listfileSearch = reroot.address
                    return reroot
            else :
                current = reroot.Lc
                while current is not None :
                    if(current.data == word[1]) :
                        return self.reSearchW( current ,word[1:] , realW , p, listShow , filename)
                    current = current.next
        self.listfileSearch = []
        return

    def  searchOneWord (self ,word  , p ,listShow) :

        char = word[0]
        current = self.root.Lc
        while current is not None :
            if char == current.data :
                 return self.reSearchW(current , word  , word , p , listShow , "" )
            current = current.next

    def isStopWord(self, word, stopwords):
        if not word.isalpha():
            return True
        for w in stopwords:
            if w.lower() == word.lower():
                return True
        return False
    def searchOneLine(self, line , stopword , listShow):
        # search line with function search word and then return th intersect of lists
        first = 1
        list1 = []
        for w in line.split():
            if (not self.isStopWord(w, stopword)):
                if first == 1:
                    self.searchOneWord(w ,0 , listShow)
                    list1 = self.listfileSearch
                    first = 0
                else:
                    self.searchOneWord(w , 0, listShow)
                    list2 = self.listfileSearch
                    list1 = list(set(list1).intersection(list2))
        str = "answer : "
        for a in list1:
            str = str + "  " + a
        self.fileOpen.writeList(listShow, str)

    def deleteNode(self, word, filename , listShow):
        char = word[0]
        current = self.root.Lc
        while current is not None:
            if char == current.data:
                self.reSearchW(current, word, word, 2, listShow , filename)
            current = current.next
        return
    def updeateNode (self,filename , listshow ) :
        self.visit(self.root , "" , listshow , filename ,2 )
