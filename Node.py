import enum
import math
# from VisualNode import VisualNode

class NodeType(enum.Enum):
    FREE = enum.auto()
    OBSTACLE = enum.auto()
    START = enum.auto()
    DESTINATION = enum.auto()
    

class RuntimeStatus(enum.Enum):
    NONE = enum.auto()
    EXPLORED = enum.auto()
    VISITED = enum.auto()
    SELECTED = enum.auto()


class Node:
    def __init__(self, row, col):
        self.f_cost = math.inf #Sum of h cost and g cost
        self.h_cost = 0 #Estimated cost from current node to target node
        self.g_cost = math.inf #Cost from initial node to current node
        self.node_type: NodeType = NodeType.FREE
        self.runtime_status: RuntimeStatus = RuntimeStatus.NONE
        self.linked_visual_node = None
        self.prev_node = None


        self.row = row
        self.col = col

    def __lt__(self, other):
        return self.f_cost < other.f_cost        

    def update_f_cost(self):
        if self.g_cost == None:
            self.f_cost = self.h_cost
        else:
            self.f_cost = self.h_cost + self.g_cost
        self.update_linked_visual_node()
        self.add_cost_text() #Display the cost in the visualNode if you are updating the cost

    def set_h_cost(self, new_h_cost):
        self.h_cost = new_h_cost
        self.update_f_cost()
        self.update_linked_visual_node()
        self.add_cost_text() #Display the cost in the visualNode if you are updating the cost

    def set_g_cost(self, new_g_cost, prev_node):
        self.g_cost = new_g_cost
        self.prev_node = prev_node
        self.update_f_cost()
        self.update_linked_visual_node()
        self.add_cost_text() #Display the cost in the visualNode if you are updating the cost

    def set_node_type(self, node_type:NodeType):
        self.node_type = node_type
        self.update_linked_visual_node()
    
    def set_runtime_status(self, runtime_status:RuntimeStatus):
        self.runtime_status = runtime_status
        self.update_linked_visual_node()
    
    def set_visited(self):
        self.set_runtime_status(RuntimeStatus.VISITED)

    def set_explored(self):
        self.set_runtime_status(RuntimeStatus.EXPLORED)

    def set_selected(self):
        self.set_runtime_status(RuntimeStatus.SELECTED)

    def add_cost_text(self):
        if self.linked_visual_node:
            self.linked_visual_node.add_cost_text()

    def update_linked_visual_node(self):
        if self.linked_visual_node:
            self.linked_visual_node.update_visual()

    def link(self, linked_visual_node):
        self.linked_visual_node = linked_visual_node
        self.linked_visual_node.link_node(self)
        self.linked_visual_node.update_visual()
    
if __name__ == "__main__":
    n = Node()
    n.set_node_type(NodeType.OBSTACLE)
    print(n.node_type)

    n.set_h_cost(30)
    print(n.h_cost)
    print(n.f_cost)
