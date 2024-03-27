class Node:
    """
    Represents a node in the search tree.
    """

    def __init__(self, state, parent=None, action=None):
        """
        Initialize a new node.
        """
        self.state = state
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        """
        Check if two nodes are equal.
        """
        return self.state == other.state

    def __hash__(self):
        """
        Hash the node for storing in a set or dictionary.
        """
        return hash(self.state)


class QueueFrontier:
    """
    Implements a queue for the frontier of the search.
    """

    def __init__(self):
        """
        Initialize an empty frontier.
        """
        self.frontier = []

    def add(self, node):
        """
        Add a node to the frontier.
        """
        self.frontier.append(node)

    def contains_state(self, state):
        """
        Check if the frontier contains a node with the given state.
        """
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """
        Check if the frontier is empty.
        """
        return len(self.frontier) == 0

    def remove(self):
        """
        Remove and return the node from the frontier.
        """
        if self.empty():
            raise Exception("Frontier is empty.")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
