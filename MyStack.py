class Stack():
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        return self.items.append(item)

    def pop(self):
        return self.items.pop()
    def getElements(self):
        return self.items
    def showStack(self):
        print(self.items)
    def deleteStack(self):
        self.items.clear()