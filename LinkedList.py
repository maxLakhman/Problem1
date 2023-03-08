class Node:
    def __init__(self, id):
        self.id = id
        self.prev = None
        self.next = None

class LinkedList:

    def __init__(self, data = None):

        self.size = 0
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head

        if data:
            trav = self.head
            for item in data:
                self.append(item)

    def append(self, id):

        node = Node(id)
        node.next = self.tail
        node.prev = self.tail.prev

        node.prev.next = node
        node.next.prev = node
        self.size += 1

    def remove(self, id):

        trav = self.head
        while trav != None:
            trav = trav.next
            if trav.id == id:
                trav.prev.next = trav.next
                trav.next.prev = trav.prev
                del trav
                self.size -= 1
                return True
        return False

    def size(self):
        return self.size

    def begin(self):
        return self.head.next

    def end(self):
        return self.tail

