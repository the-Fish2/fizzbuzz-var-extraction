def depth_first_search(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)
    traversal_order = [start]

    for neighbor in graph[start]:
        if neighbor not in visited:
            traversal_order.extend(depth_first_search(graph, neighbor, visited))

    return traversal_order
