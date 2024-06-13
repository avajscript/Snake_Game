class Node:
    def __init__(self):
        self.prev = None
        self.next = None

    def has_next(self):
        return self.next is not None

    def has_prev(self):
        return self.prev is not None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.cur = None
        self.size = 0

    def print_nodes(self):
        current = self.head
        while current:
            print(f"x: ${current.x}, y {current.y}")
            current = current.next
    def insert_start(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
            self.head.next = None
            self.head.prev = None
            self.cur = self.head
        else:
            self.head.prev = node
            node.next = self.head
            node.prev = None
            self.head = node

        self.size += 1

    def insert_end(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
            self.head.next = None
            self.head.prev = None
            self.cur = self.head
        else:
            self.tail.next = node
            node.prev = self.tail
            node.next = None
            self.tail = node

        self.size += 1

    def get_node(self, node):
        cur_node = node.head
        found = False
        while True:
            if cur_node == node:
                found = True
                break
            if not cur_node.has_next():
                break
            cur_node = cur_node.next

        return cur_node if found is True else False


    def get_node_by_index(self, index):
        if index == 0:
            return self.head
        elif index > self.size:
            return None

        cur_node = self.head
        i = 0
        while i < index:
            i += 1
            cur_node = cur_node.next

        return cur_node







