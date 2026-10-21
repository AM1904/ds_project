# -*- coding: utf-8 -*-
"""
Phase 2: Binary Search Tree (BST)
Enables efficient O(log n) data access, insertion, searching, and deletion
for timetable entities (e.g. Courses keyed by course_id).
"""
from typing import Any, List, Optional, Tuple


class BSTNode:
    """Node for a Binary Search Tree containing key and associated record."""
    def __init__(self, key: int, data: Any):
        self.key: int = key
        self.data: Any = data
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

    def __str__(self):
        return f"[Key: {self.key} | {self.data}]"


class BinarySearchTree:
    """
    Binary Search Tree for efficient course / record retrieval and ordering.
    In-order traversal of the BST yields records in perfectly sorted key order.
    """
    def __init__(self, entity_name: str = "Record"):
        self.root: Optional[BSTNode] = None
        self.entity_name = entity_name
        self._size = 0

    def get_size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.root is None

    def insert(self, key: int, data: Any) -> None:
        """Insert a key-record pair into the BST."""
        self.root = self._insert_node(self.root, key, data)
        self._size += 1

    def _insert_node(self, node: Optional[BSTNode], key: int, data: Any) -> BSTNode:
        if node is None:
            return BSTNode(key, data)
        if key < node.key:
            node.left = self._insert_node(node.left, key, data)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, data)
        else:
            # Overwrite existing data with identical key
            node.data = data
        return node

    def search(self, key: int) -> Tuple[Optional[Any], int]:
        """
        Search for a record by its key.
        Returns (data, comparison_count).
        Demonstrates O(log n) average efficiency vs O(n) linear search.
        """
        curr = self.root
        comparisons = 0
        while curr is not None:
            comparisons += 1
            if key == curr.key:
                return curr.data, comparisons
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None, comparisons

    def find_min(self, node: Optional[BSTNode] = None) -> Optional[BSTNode]:
        """Find the node with the minimum key."""
        curr = node if node is not None else self.root
        if curr is None:
            return None
        while curr.left is not None:
            curr = curr.left
        return curr

    def find_max(self, node: Optional[BSTNode] = None) -> Optional[BSTNode]:
        """Find the node with the maximum key."""
        curr = node if node is not None else self.root
        if curr is None:
            return None
        while curr.right is not None:
            curr = curr.right
        return curr

    def delete(self, key: int) -> bool:
        """Delete a record by key handling 0, 1, or 2 children cases."""
        if self.search(key)[0] is None:
            return False
        self.root = self._delete_node(self.root, key)
        self._size -= 1
        return True

    def _delete_node(self, node: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            # Node to delete found:
            # Case 1: No child (leaf)
            if node.left is None and node.right is None:
                return None
            # Case 2: One child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Case 3: Two children -> Replace with In-order Successor (min in right subtree)
            successor = self.find_min(node.right)
            node.key = successor.key
            node.data = successor.data
            node.right = self._delete_node(node.right, successor.key)
        return node

    def inorder_sorted(self, node: Optional[BSTNode] = None) -> List[Any]:
        """Returns records in naturally sorted key order."""
        result: List[Any] = []

        def _traverse(n: Optional[BSTNode]):
            if n is not None:
                _traverse(n.left)
                result.append(n.data)
                _traverse(n.right)

        _traverse(self.root if node is None else node)
        return result

    def display(self, node: Optional[BSTNode] = None, prefix: str = "", is_left: bool = True) -> None:
        """Visual tree printout using clean ASCII."""
        curr = node if node is not None else self.root
        if curr is None:
            return
        if curr.right:
            self.display(curr.right, prefix + ("|   " if is_left else "    "), False)
        connector = "\\-- " if is_left else "+-- "
        print(f"{prefix}{connector}Key {curr.key}: {curr.data}")
        if curr.left:
            self.display(curr.left, prefix + ("    " if is_left else "|   "), True)
