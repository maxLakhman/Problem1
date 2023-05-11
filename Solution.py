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
        #Initialize graph variables
        graph = self.graph
        isp = self.isp
        list_clients = self.info["list_clients"]
        bandwidths = self.info["bandwidths"]
        is_rural = self.info["is_rural"]
        toleranceb = self.info["betas"]
        simulator = Simulator()
        bfs_paths = simulator.local_bfs_path(graph, isp, list_clients)
        rural_list = list()
        non_rural_list = list()
        priorities = {node: 0 for node in list_clients}
        paths = {node: list() for node in list_clients}
        bandwidthused = {node: 0 for node in graph}
        payments = self.info["payments"]
        priors = [-1] * len(graph)

        #Determine priority
        priority = 0
        for client in list_clients:
            if is_rural[client]:
                rural_list.append(client)
            else:
                non_rural_list.append(client)
        priority_list = list()
        for client in non_rural_list:
            priorities[client] = priority
            priority += 1
            priority_list.append(client)
        priority_list.reverse()
        for client in rural_list:
            priorities[client] = priority
            priority += 1
            priority_list.append(client)
        priority_list.reverse()

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
        maxdelay = {client: 0 for client in non_rural_list}
        ticks = {node: math.ceil(bandwidthused[node] / bandwidths[node]) for node in graph.keys()}
        sortedclients = sorted(rural_list, key = lambda x: payments[x], reverse=True)
        #Increase bandwidth for nodes that need it
        for client in sortedclients:
            maxdelay[client] = 0
            for item in paths[client]:
                maxdelay[client] += ticks[item]
            for item in paths[client]:
                if maxdelay[client] * toleranceb[client] >= len(bfs_paths[client]) and ticks[item] > 1 and item != client:
                    bandwidths[item] += 1
                    ticks[item] = math.ceil(bandwidthused[item] / bandwidths[item])
        return (paths, bandwidths, priorities)
