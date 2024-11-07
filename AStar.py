from tkinter import Tk
from tkinter import ttk
from Node import Node, NodeType, RuntimeStatus
from VisualNode import VisualNode
import random
import threading
import time
from PrioritySet import PrioritySet



class AStar:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.nodes:list[Node] = []
        self.linked_visualizer = None
        self.heuristic = None

        self.start_node:Node = None
        self.end_node:Node = None

        self.__init_nodes__()
    
    def __init_nodes__(self):
        for r in range(self.num_rows):
            row_of_nodes = []
            for c in range(self.num_cols):
                node = Node(r, c)
                row_of_nodes.append(node)
            self.nodes.append(row_of_nodes)

    def set_heuristic_function(self, heuristic):
        self.heuristic = heuristic

    def get_unvisited_neighbors(self, node):
        row, col = node.row, node.col
        neighbors:list[Node] = []
        if row - 1 >= 0:
            neighbors.append(self.nodes[row-1][col])
        if row + 1 < self.num_rows:
            neighbors.append(self.nodes[row+1][col])
        if col - 1 >= 0:
            neighbors.append(self.nodes[row][col-1])
        if col + 1 < self.num_cols:
            neighbors.append(self.nodes[row][col+1])

        # print(f"Getting neighbors for ({row}, {col})")
        len = neighbors.__len__()
        i = 0
        while i < len:
            neighbor = neighbors[i]
            i += 1
            # print(f"({neighbor.row}, {neighbor.col}): Type = {neighbor.node_type}")
            if neighbor.node_type == NodeType.OBSTACLE or neighbor.runtime_status == RuntimeStatus.VISITED:
                neighbors.remove(neighbor)
                i -= 1
                len -= 1

        return neighbors
    
    def trace_back_path(self):
        path:list[Node] = []
        node = self.end_node
        print(f"({node.prev_node.row}, {node.prev_node.col})")
        while node.prev_node != None:
            path.append(node.prev_node)
            node = node.prev_node
            node.set_selected()
        return path
    
    def run_aStar(self):
        COST = 10
        explored_nodes = PrioritySet()
        explored_nodes.push(self.start_node)
        while True:
            currentNode = explored_nodes.pop()
            currentNode.set_visited()
            print(f"Current Node: {currentNode} at ({currentNode.row}, {currentNode.col}) with Cost: {currentNode.g_cost}")
            if currentNode == self.end_node:
                self.trace_back_path()
                print("Done with A*")
                break
            neighbors = self.get_unvisited_neighbors(currentNode)
            new_g_cost = currentNode.g_cost + COST
            print(f"\t\tNew Cost: {new_g_cost}")
            for neighbor in neighbors:
                print(f"\tNeighbor: {neighbor} at ({neighbor.row}, {neighbor.col})")
                h_cost = self.heuristic(neighbor, self.end_node)
                neighbor.set_h_cost((h_cost))

                if new_g_cost < neighbor.g_cost:
                    neighbor.set_g_cost(new_g_cost, currentNode)
                    print(f"\t\tSetting new Cost: {neighbor.g_cost}")
                else:
                    print(f"\t\tAlready set Cost: {neighbor.g_cost}")
                neighbor.set_explored()
                explored_nodes.push(neighbor)
                
            time.sleep(0.1)
        if self.linked_visualizer:
            pass #There will be seperate code for if there is a visualizer or not. If there is a visualizer, the "loop" has to come from the 
        else:
            pass
        pass #TODO: Implement A* in this function
    
    def set_as_obstacle(self, row, col):
        self.nodes[row][col].set_node_type(NodeType.OBSTACLE)

    def set_as_start(self, row, col):
        self.nodes[row][col].set_node_type(NodeType.START)
        self.nodes[row][col].set_g_cost(0, None)
        self.start_node = self.nodes[row][col]

    def set_as_destination(self, row, col):
        self.nodes[row][col].set_node_type(NodeType.DESTINATION)
        self.end_node = self.nodes[row][col]

    def set_as_explored(self, row, col):
        self.nodes[row][col].set_runtime_status(RuntimeStatus.EXPLORED)

    def set_as_visited(self, row, col):
        self.nodes[row][col].set_runtime_status(RuntimeStatus.VISITED)

    def link_visualizer(self, visualizer):
        self.linked_visualizer = visualizer
        self.linked_visualizer.link(self)


class AStarVisualizer:
    def __init__(self):
        self.visual_nodes = []
        self.linked_aStar = None
        self.__init_visuals__()

    def __init_visuals__(self):
        root = Tk()
        root.title("A* Visualizer")
        self.root = root #Store root as instance variable
        frame_full = ttk.Frame(root, padding=10)
        frame_full.grid()

        frame_top = ttk.Frame(frame_full, padding=10)
        frame_top.grid(row=0, column=0)
        self.frame_map = frame_top #Create instance variable so this can be populated with the map when the visualizer is linked

        frame_bottom = ttk.Frame(frame_full, padding=10)
        frame_bottom.grid(row=1, column=0)
        #Frame bottom will have buttons for running A*, resetting the grid, etc.

        button_runAStar = ttk.Button(frame_bottom, text="Run A*")
        button_runAStar.grid(row=0, column=0)
        def start_aStar():
            self.aStar_thread = threading.Thread(target=self.linked_aStar.run_aStar)
            self.aStar_thread.daemon = True
            self.aStar_thread.start()
        button_runAStar.config(command=start_aStar)

    def link(self, linked_aStar: AStar):
        self.linked_aStar = linked_aStar

        #Build the visual representation based on the linked A*
        num_rows = linked_aStar.num_rows
        num_cols = linked_aStar.num_cols

        for r in range(num_rows):
            row_of_visual_nodes = []
            for c in range(num_cols):
                visual_node = VisualNode(self.frame_map)
                row_of_visual_nodes.append(visual_node) #Add the visual node to an internal 2D array of VisualNodes
                visual_node.grid(row=r, column=c)
                self.linked_aStar.nodes[r][c].link(visual_node) #Link the node to its visual_node counterpart
            self.visual_nodes.append(row_of_visual_nodes)

    def test_after_function(self):
        print("Running after")
        r = random.randint(0, 9)
        c = random.randint(0, 9)

        self.linked_aStar.nodes[r][c].set_node_type(RuntimeStatus.VISITED)
        self.root.after(1000, self.test_after_function)
    
    def show(self):
        self.root.mainloop()
        



# class AStarVisualizer:
#     def __init__(self, numRows, numCols, start:tuple=None, end:tuple=None):
#         self.buttonRefs:VisualNode = [] #Contains references to each button in the grid
#         self.nodes:Node = [[]]
#         self.numRows = numRows
#         self.numCols = numCols
        

#     #Button Event Handler Function
#     def onClick(self, obj: Button, row, col):
#         self.isObstacle[row][col] = not self.isObstacle[row][col]
#         currentColor = obj.cget("bg")
#         newColor = "blue" if currentColor == "white" else "white"
#         obj.config(bg=newColor)
        

#     def on_drag_motion(self, event):
#         # print("Dragging")

#         button = event.widget.winfo_containing(event.x_root, event.y_root)

#         if button:
#             button.config(bg="blue")
#             for r in range(self.buttonRefs.__len__()):
#                 for c in range(self.buttonRefs[0].__len__()):
#                     if self.buttonRefs[r][c] == button:
#                         self.isObstacle[r][c] = True


#     def toggleButton(self, button=None, row=None, col=None):
#         if button:
#             for r in range(self.buttonRefs.__len__()):
#                 for c in range(self.buttonRefs[0].__len__()):
#                     if self.buttonRefs[r][c] == button:
#                         row = r
#                         col = c
#         elif row and col:
#             button = self.buttonRefs[row][col]

#         self.isObstacle[row][col] = not self.isObstacle[row][col]
#         newColor = "blue" if self.isObstacle[row][col] == True else "white"
#         button.config(bg=newColor)

#     def clearGrid(self):
#         for r in range(self.buttonRefs.__len__()):
#                 for c in range(self.buttonRefs[0].__len__()):
#                         self.buttonRefs[r][c].config(bg="white")
#                         self.isObstacle[r][c] = False

#     def setObstacle(self, row, column):
#         if( ( isinstance(row, list) or isinstance(row, np.ndarray) ) and ( isinstance(column, list) or isinstance(column, np.ndarray)) ):
#             for i in range(row.__len__()):
#                 r, c = row[i], column[i]
#                 self.nodes[r][c].set_node_type(NodeType.OBSTACLE)
#         else:
#             print(self.nodes[row][column])
#             self.nodes[row][column].set_node_type(NodeType.OBSTACLE)

                

#     def createVisual(self):
#         root = Tk()
#         root.title("Synthetic Data Generation")
#         frameFull = ttk.Frame(root, padding=10)
#         frameFull.grid()
#         frameTop = ttk.Frame(frameFull, padding=10)
#         frameTop.grid(row=0, column=0)
#         self.isObstacle = []
#         self.buttonRefs = []
#         for row in range(self.numRows):
#             buttonRowRefs = []
#             buttonRowVals = []
#             nodesRow = []
#             for column in range(self.numCols):
#                 node = Node()
#                 nodesRow.append(node)
#                 visualNode = VisualNode(parent_node=frameTop)
#                 node.link(visualNode)
#                 visualNode.add_cost_text()

#                 visualNode.grid(row=row, column=column)
#                 # button.config(bg="white")
#                 visualNode.config(command=lambda obj=visualNode, r=row, c=column: self.onClick(obj, r, c))
#                 buttonRowVals.append(False)
#                 buttonRowRefs.append(visualNode)
#             self.isObstacle.append(buttonRowVals)
#             self.buttonRefs.append(buttonRowRefs)
#             self.nodes.append(nodesRow)

#         frameBottom = ttk.Frame(frameFull, padding=10)
#         frameBottom.grid(row=1, column=0)

#         visualNode = Button(frameBottom, text="Save as Tensor")
#         visualNode.grid(row=0, column=0)

#         frameFull.pack()
#         self.root = root

#     def show(self):
#         self.root.mainloop()



        

# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)
if __name__ == "__main__":
    # generator = AStarVisualizer(numRows=10, numCols=10)
    # generator.setObstacle(5, 5)
    # generator.createVisual()
    # # generator.loadTensor()
    # generator.show()

    # # generator.setObstacle(5, 5)


    a_star = AStar(10, 10)
    a_star.set_as_obstacle(0, 0)
    a_star.set_as_obstacle(9, 9)
    a_star.set_as_start(1, 1)
    a_star.set_as_destination(4, 3)

    a_star_visualizer = AStarVisualizer()
    a_star_visualizer.link(a_star)
    a_star_visualizer.show()
