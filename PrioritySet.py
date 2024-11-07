from heapq import heapify, heappush, heappop

#Similar to PriorityQueue but does not allow duplicates
class PrioritySet:
    def __init__(self):
        self.heap = []

    def push(self, element):
        if(self.heap.__contains__(element)):
            heapify(self.heap)
        else:
            heappush(self.heap, element)

    def pop(self):
        return heappop(self.heap)
    
    def heapify(self):
        heapify(self.heap)

    def is_empty(self):
        return self.heap.__len__() == 0