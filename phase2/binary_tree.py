# -*- coding: utf-8 -*-
"""
Phase 2: Hierarchical Structures - Binary Tree
Represents structured hierarchical academic data (e.g., Academic Program / Department Hierarchy)
and performs Tree Traversals (Inorder, Preorder, Postorder).
"""
from typing import Any, List, Optional


class TreeNode:
    """Node for structured hierarchical data storage."""
    def __init__(self, key: str, value: Any = None):
        self.key = key
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

    def __str__(self):
        val_str = f" ({self.value})" if self.value is not None else ""
        return f"[{self.key}{val_str}]"


class BinaryTree:
    """
    Binary Tree for hierarchical academic curriculum / departmental hierarchy storage.
    Supports Preorder, Inorder, and Postorder traversals.
    """
    def __init__(self, root_key: str = "Root", root_val: Any = None):
        self.root = TreeNode(root_key, root_val)

    def preorder(self, node: Optional[TreeNode] = None, result: Optional[List[str]] = None) -> List[str]:
        """
        Preorder Traversal: Root -> Left -> Right
        Use-case: Top-down hierarchical breakdown (e.g., Department -> Tracks -> Core Courses).
        """
        if result is None:
            result = []
        curr = node if node is not None else self.root
        if curr is None:
            return result

        result.append(f"{curr.key}: {curr.value}" if curr.value else str(curr.key))
        if curr.left:
            self.preorder(curr.left, result)
        if curr.right:
            self.preorder(curr.right, result)
        return result

    def inorder(self, node: Optional[TreeNode] = None, result: Optional[List[str]] = None) -> List[str]:
        """
        Inorder Traversal: Left -> Root -> Right
        Use-case: Symmetric structured inspection.
        """
        if result is None:
            result = []
        curr = node if node is not None else self.root
        if curr is None:
            return result

        if curr.left:
            self.inorder(curr.left, result)
        result.append(f"{curr.key}: {curr.value}" if curr.value else str(curr.key))
        if curr.right:
            self.inorder(curr.right, result)
        return result

    def postorder(self, node: Optional[TreeNode] = None, result: Optional[List[str]] = None) -> List[str]:
        """
        Postorder Traversal: Left -> Right -> Root
        Use-case: Bottom-up prerequisite resolution and resource deallocation.
        """
        if result is None:
            result = []
        curr = node if node is not None else self.root
        if curr is None:
            return result

        if curr.left:
            self.postorder(curr.left, result)
        if curr.right:
            self.postorder(curr.right, result)
        result.append(f"{curr.key}: {curr.value}" if curr.value else str(curr.key))
        return result

    def display(self, node: Optional[TreeNode] = None, prefix: str = "", is_left: bool = True) -> None:
        """Visual ASCII hierarchy display."""
        curr = node if node is not None else self.root
        if curr is None:
            return

        if curr.right:
            self.display(curr.right, prefix + ("|   " if is_left else "    "), False)

        connector = "\\-- " if is_left else "+-- "
        val_text = f" ({curr.value})" if curr.value else ""
        print(f"{prefix}{connector}{curr.key}{val_text}")

        if curr.left:
            self.display(curr.left, prefix + ("    " if is_left else "|   "), True)
