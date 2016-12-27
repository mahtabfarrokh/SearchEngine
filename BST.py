class Node :
    def __init__(self , dWord ):
        self.data = dWord
        self.Rc = None
        self.Lc = None
class BinarySearchTree :
    def __init__(self , fileOpen ):
        self.root = None
        self.listfileSearch = []
        self.ps = 0 ;
        self.fileOpen = fileOpen
        self.wordNum =0

    def insertChild(self, reroot , node):
        # add node
        if self.root is None :
            #add root
            self.root = node
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
            else :
                if reroot.Rc is None :
                    reroot.Rc = node
                else :
                    self.insertChild(reroot.Rc , node)

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