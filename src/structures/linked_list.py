from typing import Any, Optional

class Node:
    def __init__(self, value: Any):
        self.value = value
        self.next: Optional['Node'] = None


class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.size = 0

    def append(self, value: Any):
        node = Node(value)
        if not self.head:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
                cur.next = node
        self.size += 1


    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out