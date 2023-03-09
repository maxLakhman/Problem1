class Node:

    """
    Parent class for the router and the client
    """

    def __init__(self, identifier, bandwidth=float("inf"), neighbors = set()):

        self.id = identifier
        self.bandwidth = bandwidth
        self.neighbors = neighbors

    def __repr__(self):
        # For use with pdb
        return "{}(ID: {}, bandwidth: {})".format(self.__class__.__name__, self.id, self.bandwidth)


class Client(Node):

    def __init__(self, identifier, path, packet, bandwidth, neighbors, is_rural=False):

        # Initialize the node's bandwidth
        super(Client, self).__init__(identifier, bandwidth, neighbors)

        # Incremented after every simulation iteration
        self.delay = 0

        # Optimal delay as determined by the optimal solution
        self.delay_optimal = 1

        # Path determined by student from ISP to this client
        self.path = path

        # Reference to the packet destined for it
        self.packet = packet

        # Whether this client is located in a rural area
        self.is_rural = is_rural

        # Whether the client has received its packet
        self.has_received = False

    def __repr__(self):
        return "{}(ID: {}, bandwidth: {}, path: {}, packet: {}, is_rural: {}, has_received: {})".format(self.__class__.__name__, self.id, self.bandwidth, self.path, self.packet, self.is_rural, self.has_received)


class Packet:

    """
    Packet object, not actually "forwarded" in the technical sense of the word
    but its location variable helps keep track of how far along in its path it is
    """

    def __init__(self, client, path, priority=0):

        # Client id, not the instance itself
        self.client = client

        # Incremented at every simulator iteration, keeps track of how long
        # the packet has been in transit
        self.delay = 0

        # Unlike the delay, only incremented if the packet was actually forwarded
        self.location = 0

        #TODO: try removing
        # Might not need this since we sort the clients initally, but for the sake of completeness
        self.priority = priority

        # List of nodes in the path determined by the student,
        # first node being the ISP and last node usually being the client but possibly another node,
        # in which case the solution is not optimal
        self.path = path

    def __repr__(self):

        # For use with pdb
        return "{} (Client: {}, Delay: {}, Location: {}, Priority: {}, Path: {})".format(self.__class__.__name__, self.client, self.delay, self.location, self.priority, self.path)
