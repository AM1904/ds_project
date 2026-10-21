from node import Node


class Queue:
    def __init__(self, label: str = "Queue"):
        self._front = None
        self._rear = None
        self._size = 0
        self.label = label

    def enqueue(self, data) -> None:
        new_node = Node(data)
        if self.is_empty():
            self._front = new_node
            self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            print(f"  [{self.label}] Queue underflow -- nothing to dequeue.")
            return None
        data = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return data

    def front(self):
        if self.is_empty():
            print(f"  [{self.label}] Queue is empty -- nothing at front.")
            return None
        return self._front.data

    def is_empty(self) -> bool:
        return self._front is None

    def get_size(self) -> int:
        return self._size

    def display(self) -> None:
        if self.is_empty():
            print(f"  [{self.label}] (empty queue)")
            return
        print(f"  [{self.label}] FRONT ->")
        current = self._front
        idx = 1
        while current:
            print(f"    {idx}. {current.data}")
            current = current.next
            idx += 1
        print(f"  [{self.label}] <- REAR  (size = {self._size})")
