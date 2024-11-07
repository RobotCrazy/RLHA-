from tkinter import *
from Node import Node, NodeType, RuntimeStatus
import sys


#Visual Representation of the nodes
class VisualNode(Button):
    def __init__(self, parent_node):
        super().__init__(master=parent_node, text="", width=7, height=3)
        self.linked_node = None
        self.disp_costs = False

    def link_node(self, linked_node: Node):
        self.linked_node = linked_node
        self.update_visual()
    
    def update_visual(self):
        if self.linked_node == None:
            print("ERROR: Visual Node has not been linked to a node", file=sys.stderr)
            return
        
        linked_node_type = self.linked_node.node_type
        linked_node_status = self.linked_node.runtime_status


        if linked_node_type == NodeType.OBSTACLE:
            self.config(bg="black")
        elif linked_node_type == NodeType.START:
            self.config(bg="red")
        elif linked_node_type == NodeType.DESTINATION:
            self.config(bg="green")
        elif linked_node_status == RuntimeStatus.EXPLORED:
            self.config(bg="yellow")
        elif linked_node_status == RuntimeStatus.VISITED:
            self.config(bg="aqua")
        elif linked_node_status == RuntimeStatus.SELECTED:
            self.config(bg="orange")
        elif linked_node_type == NodeType.FREE:
            self.config(bg="white")

        if self.disp_costs == True:
            self["text"] = f"F: {self.linked_node.f_cost}\nG: {self.linked_node.g_cost}\nH:{self.linked_node.h_cost}"
        else:
            self["text"] = ""

    def add_cost_text(self):
        self.disp_costs = True
        self.update_visual()





if __name__ =="__main__":
    for i in range(5):
        n = Node()
        v = VisualNode(linked_node=n)

        