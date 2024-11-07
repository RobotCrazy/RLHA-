from AStar import AStar, AStarVisualizer
import threading
import random
import time
from Node import Node, NodeType
# from heapq import heapify, heappush, heappop
from PrioritySet import PrioritySet
import math

a_star = AStar(10, 10)
a_star.set_as_obstacle(0, 0)
a_star.set_as_obstacle(9, 9)
a_star.set_as_start(1, 1)
a_star.set_as_destination(4, 3)
def straight_line_distance(start_node: Node, end_node:Node):
    return int(10 * math.sqrt( (end_node.row - start_node.row)**2 + (end_node.col - start_node.col)**2 ))
a_star.set_heuristic_function(straight_line_distance)
# a_star.nodes[5][5].set_selected()
# neighbors = a_star.get_unvisited_neighbors(a_star.nodes[0][1])
# for neighbor in neighbors:
#     print(f"({neighbor.row}, {neighbor.col})")

a_star_visualizer = AStarVisualizer()
a_star_visualizer.link(a_star)

a_star_visualizer.show()




# def startSecondaryThread():
#     while True:
#         r = random.randint(0, 9)
#         c = random.randint(0, 9)

#         a_star.set_as_destination(r, c)
#         time.sleep(1)
        

# thread2 = threading.Thread(target=startSecondaryThread); 
# thread2.daemon = True
 
# thread2.start() 
# a_star_visualizer.show()

# a_star_visualizer.show()



# ps = PrioritySet()
# n0 = Node(0, 0)
# n1 = Node(1, 1)
# n2 = Node(2, 2)
# n3 = Node(3, 3)
# n1.set_h_cost(55)
# n2.set_h_cost(30)
# n3.set_h_cost(40)

# ps.push(n1)
# ps.push(n2)
# ps.push(n3)


# n1.set_h_cost(5)
# # ps.push(n1)
# # heapify(heap)

# while not ps.is_empty():
#     print(ps.pop().f_cost)

# left_top_node = a_star.nodes[5][5]
# for n in a_star.get_neighbors(left_top_node):
    # print(f"({n.row}, {n.col})")

