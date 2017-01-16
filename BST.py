import Word
class Node :
    def __init__(self , dWord ):
        self.data = dWord
        self.Rc = None
        self.Lc = None
        self.HR = 0
        self.HL =0
class BinarySearchTree :
    def __init__(self , fileOpen ):
        self.root = None
        self.listfileSearch = []
        self.ps = 0
        self.fileOpen = fileOpen
        self.wordNum =0
        self.levelNode =[]

    def insertChild(self, reroot , node):
        # add node
        print("node :", node.data.data)
        if self.root is None :
            #add root
            self.root = node
            self.AVL()
            return
        if reroot.data.data.lower() == node.data.data.lower() :
            for i in reroot.data.listFile :
                if i==node.data.listFile[0] :
                    return
            reroot.data.listFile.append(node.data.listFile[0])
            return
        else :
            if reroot.data.data > node.data.data :
                if reroot.Lc is None :
                    reroot.Lc = node
                else :
                    self.insertChild(reroot.Lc , node)
                self.AVL()
            else :
                if reroot.Rc is None :
                    reroot.Rc = node
                else :
                    self.insertChild(reroot.Rc , node)
                self.AVL()

    def in_order_print(self , root  ,listShow , filename , p):
        if not root or root.data.data is None  :
            return
        self.in_order_print(root.Lc , listShow, filename , p)
        if p==1 and  root.data.listFile  :
            #for print node
            s = root.data.data + " -> "
            for a in root.data.listFile:
                s = s + "  " + a
            self.fileOpen.writeList(listShow, s)
            self.wordNum +=1
        elif p==2 :
            #for update node file
            counter = 0
            for f in root.data.listFile:
                if f == filename:
                    root.data.listFile.pop(counter)
                    break
                counter += 1
        self.in_order_print(root.Rc , listShow, filename , p)
    def searchOneWord (self ,reroot , word , p , listShow , filename ) :
        # search word recursive
        if reroot is None or reroot.data.data is None :
            self.listfileSearch = []
            self.fileOpen.writeList(listShow, "can't find ")
            return None
        if reroot.data.data.lower() == word.lower() :
           if p==1 :
               #print result of search
               str = ""
               first =0
               for a in reroot.data.listFile:
                   if first == 1:
                       str = str + " , " + a
                   else:
                       first = 1
                       str = a
               self.fileOpen.writeList(listShow , str)
           elif p==2 :
               #delete filename from node
               counter = 0
               for f in reroot.data.listFile:
                   if f == filename:
                       reroot.data.listFile.pop(counter)
                       if len(reroot.data.listFile) ==0 :
                           del reroot
                           self.AVL()
                       break
                   counter += 1
           else :
               self.listfileSearch = reroot.data.listFile
               return reroot
        else :
            if reroot.data.data.lower() < word.lower() :
                return self.searchOneWord(reroot.Rc , word , p ,listShow , filename)
            else :
                return self.searchOneWord(reroot.Lc , word ,p , listShow , filename)
    def isStopWord (self ,word , stopwords) :
        if not word.isalpha():
            return True
        for w in stopwords :
            if w.lower() == word.lower() :
                return True
        return False
    def searchOneLine(self, line , stopword , listShow):
        #search line with function search word and then return th intersect of lists
        first =1
        list1= []
        for w in line.split() :
            if(not self.isStopWord(w,stopword) ) :
                if first ==1 :
                    self.searchOneWord(self.root, w , 0 , listShow , "")
                    list1 = self.listfileSearch
                    first =0
                else :
                    self.searchOneWord(self.root, w , 0, listShow , "")
                    list2 =  self.listfileSearch
                    list1 = list (set(list1).intersection(list2) )
        str = "answer : "
        for a in list1:
            str = str + "  " + a
        self.fileOpen.writeList(listShow, str)
    def deleteNode (self , word , filename , listShow) :
        self.searchOneWord(self.root , word , 2 , listShow , filename)

    def updeateNode(self, filename, listShow):
        self.in_order_print(self.root, listShow , filename , 2)
    def visitLevelOrder (self ) :
        current = self.root
        self.levelNode.clear()
        self.levelNode.append(current)
        i=0
        while(i< len(self.levelNode)) :
            current = self.levelNode[i]
            if(current.Lc is not None) :
                self.levelNode.append(current.Lc)
            if(current.Rc is not None) :
                self.levelNode.append(current.Rc)
            if ((current.Lc is None)and (current.Rc is None) )or current is None:
                self.levelNode.pop(i)
            else :
                i+=1
        self.levelNode.reverse()
    def setHeight (self , node) :
        if (node is None) :
            return 0
        node.HL = self.setHeight(node.Lc) +1
        node.HR = self.setHeight(node.Rc) +1
        return max(node.HL , node.HR)
    def LL_AVL (self , node) :
         print("LL")
         rotate = node #root
         wNode = Word.myWord(rotate.data.data, *rotate.data.listFile)
         nn = Node(wNode)
         nn.Rc = rotate.Rc
         rotate3 = node.Lc  #Will be root

         if (node.Lc.Rc is not None) :
             nn.Lc = node.Lc.Rc
         node.Lc = rotate3.Lc
         node.data = rotate3.data
         node.Rc = nn

    def RR_AVL(self, node):
        print("RR")
        rotate = node  # root
        wNode = Word.myWord(rotate.data.data, *rotate.data.listFile)
        nn = Node(wNode)
        nn.Lc = rotate.Lc
        rotate3 = node.Rc  # Will be root
        if (node.Rc.Lc is not None):
            rotate2 = node.Rc.Lc
            nn.Rc = rotate2
        node.Rc = rotate3.Rc
        node.data = rotate3.data
        node.Lc = nn

    def LR_AVL (self , node) :
        print("LR")
        rotate1 = node.Lc
        rotate = node.Lc.Rc
        wNode = Word.myWord(rotate1.data.data, *rotate1.data.listFile)
        nn = Node(wNode)
        nn.Lc = rotate1.Lc
        if(node.Lc.Rc.Lc is not None ) :
            nn.Rc = node.Lc.Rc.Lc
        node.Lc.data = rotate.data
        node.Lc.Rc = rotate.Rc
        node.Lc.Lc = nn
        self.LL_AVL(node)

    def RL_AVL (self , node) :
        print("RL")
        rotate1 = node.Rc
        rotate = node.Rc.Lc
        wNode = Word.myWord(rotate1.data.data, *rotate1.data.listFile)
        nn = Node(wNode)
        nn.Rc = rotate1.Rc
        if (node.Rc.Lc.Rc is not None):
            nn.Lc = node.Rc.Lc.Rc
        node.Rc.data = rotate.data
        node.Rc.Lc = rotate.Lc
        node.Rc.Rc = nn
        self.RR_AVL(node)

    def AVL (self) :
        self.setHeight(self.root)
        self.visitLevelOrder()
        if len(self.levelNode)!=0 :
            for node in self.levelNode :
                k = node.HL - node.HR
                if (abs(k) >= 2 ) :
                    if ((node.Lc is not None)and((node.Lc.Lc is not None)or(node.Lc.Rc is not None))) or \
                            ((node.Rc is not None) and ((node.Rc.Rc is not None) or (node.Rc.Lc is not None))):
                        if k > 0:
                            # L
                            h = node.Lc.HL - node.Lc.HR
                            self.avlNode = node
                            if h > 0:
                                self.LL_AVL(node)
                            else:
                                self.LR_AVL(node)
                        else:
                            h = node.Rc.HL - node.Rc.HR
                            if h > 0:
                                self.RL_AVL(node)
                            else:
                                self.RR_AVL(node)
