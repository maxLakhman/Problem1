from collections import deque


def bfs_path(graph, isp, list_clients):
    paths = {}

    graph_size = len(graph)
    priors = [-1]*graph_size
    search_queue = deque()
    search_queue.append(isp)
    while search_queue:
        node = search_queue.popleft()
        for neighbor in graph[node]:
            if (priors[neighbor] == -1 and neighbor != isp):
                priors[neighbor] = node
                search_queue.append(neighbor)

    for client in list_clients:
        path = []
        current_node = client
        while (current_node != -1):
            path.append(current_node)
            current_node = priors[current_node]
        path = path[::-1]
        paths[client] = path

    return paths
