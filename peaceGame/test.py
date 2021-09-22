from queue import PriorityQueue

def ufc():
    pqueue = PriorityQueue()
    pqueue.put((2, ("node1", [0, 1]))) #priority, node, path
    pqueue.put((3, ("node2",[0,1,2])))
    a, b = pqueue.get()
    print(a)
    print(b)
    b1 = b[1]
    b0 = b[0]
    print (b0, b1)

    

# def ucs(G, v):
#     visited = set()                  # set of visited nodes
#     q = queue.PriorityQueue()        # we store vertices in the (priority) queue as tuples 
#                                      # (f, n, path), with
#                                      # f: the cumulative cost,
#                                      # n: the current node,
#                                      # path: the path that led to the expansion of the current node
#     q.put((0, startNode, [startNode]))               # add the starting node, this has zero *cumulative* cost 
#                                      # and it's path contains only itself.

#     while not q.empty():             # while the queue is nonempty
#         cost, current_node, path = q.get()
#         visited.add(current_node)    # mark node visited on expansion,
#                                      # only now we know we are on the cheapest path to
#                                      # the current node.

#         if current_node.is_goal:     # if the current node is a goal
#             return path              # return its path
#         else:
#             for edge in in current_node.out_edges:
#                 child = edge.to()
#                 if child not in visited:
#                     q.put((current_node_priority + edge.weight, child, path + [child]))
if __name__ == "__main__":
    ufc()