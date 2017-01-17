class Element () :
    def __init__(self , word ):
        self.word = word
        self.address = []
class Hash () :
    def __init__(self , fileOpen):
        self.fileOpen = fileOpen
        self.hashList = []
        self.hashSize =150
        self.wordNum =0
        self.intersect = 0
        self.listfileSearch =[]

        for  i in range(self.hashSize) :
            k = []
            self.hashList.append(k)

    def insertChild(self , word ,address ) :
        k = self.hashFunction(word)

        for h in self.hashList[k] :
            w = h.word
            if w == word :
                if not address ==  h.address[len(h.address)-1]  :
                    h.address.append(address)
                return
        e = Element(word)
        e.address.append(address)
        self.hashList[k].append(e)

    def visit(self, listShow , filename , p ):
        for i in self.hashList :
            if len(i) == 1:
                self.intersect += 1
        for l in self.hashList :
            for e in l :
                if p== 1 :
                    s = e.word + " -> "
                    for a in e.address:
                        s = s + " " + a
                    self.fileOpen.writeList(listShow, s)
                    self.wordNum += 1
                elif p==2 :
                    if len(e.address) == 1 :
                        del e
                    else :
                        for  a in range(len(e.address)) :
                            if e.address[a]== filename :
                               del e.address[a]


    def searchOneWord(self, word ,p , listShow):
        k = self.hashFunction(word)
        for h in self.hashList[k]:
            w = h.word
            if w == word:
                if p==1 :
                    first = 1
                    s = ""
                    for a in h.address:
                        if first == 1:
                            s = a
                            first = 2
                        else:
                            s = s + " . " + a
                    self.fileOpen.writeList(listShow, s)
                elif p==0 :
                    self.listfileSearch = h.address
                return
    def isStopWord(self, word, stopwords):
        if not word.isalpha():
            return True
        for w in stopwords:
            if w.lower() == word.lower():
                return True
        return False
    def searchOneLine(self, line, stopword, listShow):
        first = 1
        list1 = []
        for w in line.split():
            if (not self.isStopWord(w, stopword)):
                if first == 1:
                    self.searchOneWord(w,0, listShow)
                    list1 = self.listfileSearch
                    first = 0
                else:
                    self.searchOneWord(w,0, listShow)
                    list2 = self.listfileSearch
                    list1 = list(set(list1).intersection(list2))
        str = "answer : "
        for a in list1:
            str = str + "  " + a
        self.fileOpen.writeList(listShow, str)


    def deleteNode (self , word , filename , listShow) :
        k = self.hashFunction(word)
        for h in self.hashList[k]:
            w = h.word
            if w == word:
                if len(h.address)==1  :
                    del h
                    break
                else :
                    for a in range(len(h.address)) :
                        if h.address[a] == filename :
                            del h.address[a]
                            break
    def updeateNode(self, filename, listShow):
        self.visit(listShow , filename , 2)
    def asciiFold(self , word):
        if len(word)==0 :
            return 0
        if len(word)==1 :
            return ord(word[0])
        if len(word)==2 :
            a = ord(word[0])
            b = ord(word[1])
            s = str(a) + str(b)
            return int(s)
        if len(word)==3 :
            a = ord(word[0])
            b = ord(word[1])
            s = str(a) + str(b)
            return int(s) + self.asciiFold(word[2])
        if len(word)>=4 :
            a = ord(word[0])
            b = ord(word[1])
            c = ord(word[2])
            d = ord(word[3])
            s1 = str(a) + str(b)
            s2 = str(d) + str(c)
            return int(s1) + int (s2) + self.asciiFold(word[4:])
    def hashFunction (self , word) :
        return self.asciiFold(word) % self.hashSize

