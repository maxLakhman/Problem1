from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys
import math

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        graph = self.graph
        isp = self.isp
        list_clients = self.info["list_clients"]
        simulator = Simulator()
        bfspaths = simulator.local_bfs_path(graph, isp, list_clients)
        originalbandwidths = self.info["bandwidths"]
        bandwidths = originalbandwidths.copy()
        bandwidthused = {node: 0 for node in graph.keys()}
        tolerancea = self.info["alphas"]
        toleranceb = self.info["betas"]
        payments = self.info["payments"]
        plawsuit = self.info["rho1"]
        pfcc = self.info["rho2"]
        fccval = self.info["is_fcc"]
        fcclist = list()
        for item in fccval:
            if fccval[item] == 1:
                fcclist.append(item)
        costlawsuit = self.info["lawsuit"]
        costfcc = self.info["fcc_fine"]
        costbandwidth = self.info["cost_bandwidth"]
        priors = [-1] * len(graph)
        paths, priorities = {}, {}
        #BFS
        search_queue = deque()
        search_queue.append(isp)
        while search_queue:
            node = search_queue.popleft()
            for neighbor in graph[node]:
                if (priors[neighbor] == -1 and neighbor != isp):
                    priors[neighbor] = node
                    search_queue.append(neighbor)
        #Calculate paths
        for client in list_clients:
            path = []
            current_node = client
            while (current_node != -1):
                path.append(current_node)
                if(current_node != client):
                    bandwidthused[current_node] += 1
                current_node = priors[current_node]
            path = path[::-1]
            paths[client] = path
        #Figure out potential max delay for each client
        maxdelay = {client: 0 for client in list_clients}
        ticks = {node: math.ceil(bandwidthused[node] / bandwidths[node]) for node in graph.keys()}
        sortedclients = sorted(list_clients, key = lambda x: payments[x], reverse=True)
        #Increase bandwidth for nodes that need it
        for client in sortedclients:
            maxdelay[client] = 0
            for item in paths[client]:
                maxdelay[client] += ticks[item]
            for item in paths[client]:
                if maxdelay[client] * toleranceb[client] >= len(bfspaths[client]) and ticks[item] > 1 and item != client:
                    bandwidths[item] += 1
                    ticks[item] = math.ceil(bandwidthused[item] / bandwidths[item])
        return (paths, bandwidths, priorities)
