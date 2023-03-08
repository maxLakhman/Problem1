from Objects import Node, Client, Packet
from LinkedList import LinkedList
from collections import deque, defaultdict


class Simulator:

    def __init__(self):
        """
        Constructor, not very interesting
        """

    def validate_edge(self, node1, node2):
        return node1.id in node2.neighbors

    # Adding a copy of BFS here for convenience
    def local_bfs_path(self, graph, isp, list_clients):

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

    def run(self, graph, isp, list_clients, paths, bandwidths, priorities, is_rural):
        """
        Runs the simulation based on the paths provided by the student
        """

        # Creating shortest paths
        shortest_paths = self.local_bfs_path(graph, isp, list_clients)

        # Mapping from client id to their corresponding packet object
        packets = {c: Packet(c, paths[c]) for c in list_clients}

        # Mapping from the client id to the client object
        self.clients = {
            c: Client(c, paths[c], packets[c], bandwidths[c], set(graph[c]), is_rural[c] if is_rural else False) for c in list_clients}

        # Mapping from node id to the node object
        nodes = {u: Node(u, bandwidths[u], set(graph[u])) for u in graph}

        # List of all nodes that are clients, sorted by priority
        if priorities:
            list_clients = sorted(
                list_clients, key=lambda client: priorities[client], reverse=True)

        # Use this to keep track of the routers that actually forwarded packets
        active = set()

        list_clients = LinkedList(list_clients)

        # Iterate while at least one packet has not reached the end of its path yet
        while list_clients.size > 0:

            current = list_clients.begin()

            while current != list_clients.end():

                packet = packets[current.id]

                if not packet.path or packet.path[0] != isp:
                    receiving_client = self.clients[packet.client]
                    receiving_client.delay = float("inf")
                    list_clients.remove(current.id)
                    continue

                # The node that this client's packet is currently at
                current_node = nodes[packet.path[packet.location]]

                # Check if the current location is the end of the path
                if packet.location == len(packet.path) - 1:

                    # The last node may or may not be the client that the packet
                    # was intended for. If it is, set the appropriate variables
                    # Also checks to make sure the student path is not shorter then the shortest path
                    if current_node.id == packet.client and packet.location >= len(shortest_paths[packet.client])-1:
                        receiving_client = self.clients[packet.client]
                        receiving_client.delay = packet.delay
                    else:
                        receiving_client.delay = float("inf")
                    list_clients.remove(current.id)
                    current = current.next
                    continue

                # Packet hasn't reached yet, increment delay
                packet.delay += 1

                # Only forward packets if the bandwidth has not been exhausted yet
                if current_node.bandwidth > 0:
                    active.add(current_node)
                    current_node.bandwidth -= 1
                    packet.location += 1
                    if not self.validate_edge(current_node, nodes[packet.path[packet.location]]):
                        list_clients.remove(packet.client)
                        self.clients[packet.client].delay = float("inf")

                current = current.next

            # Reset the bandwidth for the next iteration
            for node in active:
                node.bandwidth = bandwidths[node.id]
            active.clear()

    def get_delays(self, list_clients):
        """
        Returns the delay experienced by each client after the simulation has
        run its course
        """
        return {client: self.clients[client].delay for client in list_clients}

    def get_clients(self, list_clients):
        '''
        :param list_clients: List of all the node IDs that represent clients
        :return: The client objects corresponding to each ID
        '''
        return {client: self.clients[client] for client in list_clients}
