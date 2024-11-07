

class AStarVisualizer:
    def __init__(self, numRows, numCols, start:tuple=None, end:tuple=None):
        self.buttonRefs:VisualNode = [] #Contains references to each button in the grid
        self.nodes:Node = [[]]
        self.numRows = numRows
        self.numCols = numCols
        

    #Button Event Handler Function
    def onClick(self, obj: Button, row, col):
        self.isObstacle[row][col] = not self.isObstacle[row][col]
        currentColor = obj.cget("bg")
        newColor = "blue" if currentColor == "white" else "white"
        obj.config(bg=newColor)
        

    def on_drag_motion(self, event):
        # print("Dragging")

        button = event.widget.winfo_containing(event.x_root, event.y_root)

        if button:
            button.config(bg="blue")
            for r in range(self.buttonRefs.__len__()):
                for c in range(self.buttonRefs[0].__len__()):
                    if self.buttonRefs[r][c] == button:
                        self.isObstacle[r][c] = True


    def toggleButton(self, button=None, row=None, col=None):
        if button:
            for r in range(self.buttonRefs.__len__()):
                for c in range(self.buttonRefs[0].__len__()):
                    if self.buttonRefs[r][c] == button:
                        row = r
                        col = c
        elif row and col:
            button = self.buttonRefs[row][col]

        self.isObstacle[row][col] = not self.isObstacle[row][col]
        newColor = "blue" if self.isObstacle[row][col] == True else "white"
        button.config(bg=newColor)

    def clearGrid(self):
        for r in range(self.buttonRefs.__len__()):
                for c in range(self.buttonRefs[0].__len__()):
                        self.buttonRefs[r][c].config(bg="white")
                        self.isObstacle[r][c] = False

    def setObstacle(self, row, column):
        if( ( isinstance(row, list) or isinstance(row, np.ndarray) ) and ( isinstance(column, list) or isinstance(column, np.ndarray)) ):
            for i in range(row.__len__()):
                r, c = row[i], column[i]
                self.nodes[r][c].set_node_type(NodeType.OBSTACLE)
        else:
            print(self.nodes[row][column])
            self.nodes[row][column].set_node_type(NodeType.OBSTACLE)

                

    def createVisual(self):
        root = Tk()
        root.title("Synthetic Data Generation")
        frameFull = ttk.Frame(root, padding=10)
        frameFull.grid()
        frameTop = ttk.Frame(frameFull, padding=10)
        frameTop.grid(row=0, column=0)
        self.isObstacle = []
        self.buttonRefs = []
        for row in range(self.numRows):
            buttonRowRefs = []
            buttonRowVals = []
            nodesRow = []
            for column in range(self.numCols):
                node = Node()
                nodesRow.append(node)
                visualNode = VisualNode(parent_node=frameTop)
                node.link(visualNode)
                visualNode.add_cost_text()

                visualNode.grid(row=row, column=column)
                # button.config(bg="white")
                visualNode.config(command=lambda obj=visualNode, r=row, c=column: self.onClick(obj, r, c))
                buttonRowVals.append(False)
                buttonRowRefs.append(visualNode)
            self.isObstacle.append(buttonRowVals)
            self.buttonRefs.append(buttonRowRefs)
            self.nodes.append(nodesRow)

        frameBottom = ttk.Frame(frameFull, padding=10)
        frameBottom.grid(row=1, column=0)

        visualNode = Button(frameBottom, text="Save as Tensor")
        visualNode.grid(row=0, column=0)

        frameFull.pack()
        self.root = root

    def show(self):
        self.root.mainloop()