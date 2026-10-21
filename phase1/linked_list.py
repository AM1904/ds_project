from node import Node


class LinkedList:
    def __init__(self, entity_label: str = "Record"):
        self.head = None
        self._size = 0
        self.entity_label = entity_label

    def _get_id(self, data) -> int:
        for attr in ("teacher_id", "course_id", "room_id", "slot_id"):
            if hasattr(data, attr):
                return getattr(data, attr)
        raise AttributeError(f"Cannot find an ID attribute on {type(data).__name__}")

    def is_empty(self) -> bool:
        return self.head is None

    def get_size(self) -> int:
        return self._size

    def insert_at_head(self, data) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
        print(f"  [INSERT HEAD] {self.entity_label} added at head -> ID {self._get_id(data)}")

    def insert_at_tail(self, data) -> None:
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1
        print(f"  [INSERT TAIL] {self.entity_label} added at tail -> ID {self._get_id(data)}")

    def insert_at_position(self, data, position: int) -> None:
        if position <= 1:
            self.insert_at_head(data)
            return

        new_node = Node(data)
        current = self.head
        step = 1

        while current.next and step < position - 1:
            current = current.next
            step += 1

        new_node.next = current.next
        current.next = new_node
        self._size += 1
        print(f"  [INSERT POS {position}] {self.entity_label} inserted -> ID {self._get_id(data)}")

    def delete_by_id(self, entity_id: int) -> bool:
        if self.is_empty():
            print(f"  [DELETE] List is empty -- nothing to delete.")
            return False

        if self._get_id(self.head.data) == entity_id:
            self.head = self.head.next
            self._size -= 1
            print(f"  [DELETE] {self.entity_label} ID {entity_id} removed from head.")
            return True

        current = self.head
        while current.next:
            if self._get_id(current.next.data) == entity_id:
                current.next = current.next.next
                self._size -= 1
                print(f"  [DELETE] {self.entity_label} ID {entity_id} removed.")
                return True
            current = current.next

        print(f"  [DELETE] {self.entity_label} ID {entity_id} not found.")
        return False

    def delete_at_position(self, position: int) -> bool:
        if self.is_empty() or position < 1 or position > self._size:
            print(f"  [DELETE POS] Invalid position {position} (list size: {self._size}).")
            return False

        if position == 1:
            removed_id = self._get_id(self.head.data)
            self.head = self.head.next
            self._size -= 1
            print(f"  [DELETE POS 1] {self.entity_label} ID {removed_id} removed.")
            return True

        current = self.head
        for _ in range(position - 2):
            current = current.next

        removed_id = self._get_id(current.next.data)
        current.next = current.next.next
        self._size -= 1
        print(f"  [DELETE POS {position}] {self.entity_label} ID {removed_id} removed.")
        return True

    def search(self, entity_id: int):
        current = self.head
        pos = 1
        while current:
            if self._get_id(current.data) == entity_id:
                print(f"  [SEARCH] Found {self.entity_label} ID {entity_id} at position {pos}.")
                return current.data
            current = current.next
            pos += 1
        print(f"  [SEARCH] {self.entity_label} ID {entity_id} not found.")
        return None

    def traverse(self) -> None:
        if self.is_empty():
            print(f"  (list is empty)")
            return

        current = self.head
        index = 1
        while current:
            print(f"  [{index}] {current.data}")
            current = current.next
            index += 1
        print(f"  -- Total: {self._size} {self.entity_label}(s)")
