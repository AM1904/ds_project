from node import Node


class Stack:
    def __init__(self, label: str = "Stack"):
        self._top = None
        self._size = 0
        self.label = label

    def push(self, data) -> None:
        new_node = Node(data)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self):
        if self.is_empty():
            print(f"  [{self.label}] Stack underflow -- nothing to pop.")
            return None
        data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return data

    def peek(self):
        if self.is_empty():
            print(f"  [{self.label}] Stack is empty -- nothing to peek.")
            return None
        return self._top.data

    def is_empty(self) -> bool:
        return self._top is None

    def get_size(self) -> int:
        return self._size

    def display(self) -> None:
        if self.is_empty():
            print(f"  [{self.label}] (empty stack)")
            return
        print(f"  [{self.label}] TOP v")
        current = self._top
        idx = 1
        while current:
            print(f"    {idx}. {current.data}")
            current = current.next
            idx += 1
        print(f"  [{self.label}] BOTTOM  (size = {self._size})")
