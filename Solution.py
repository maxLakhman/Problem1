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
        graph_size = len(graph)
        list_clients = self.info["list_clients"]
        bandwidths = self.info["bandwidths"]
        is_rural = self.info["is_rural"]
        rural_list = list()
        non_rural_list = list()
        priorities = {node: 0 for node in list_clients}
        paths = {node: list() for node in list_clients}
        weights = {node: 1 for node in graph}
        bandwidthused = {node: 0 for node in graph}
        change = False
        nochanges = False
        loop = 0

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

        #Loops until valid paths are found
        while not nochanges:
            #Calculate paths using Dijkstra's Algorithm and BFS
            unvisited = deque()
            unvisited.append(isp)
            previous = {node: -1 for node in graph}
            while unvisited:
                current = unvisited.popleft()
                #Checks if all nodes are full
                numfull = 0
                if current != isp:
                    for neighbor in graph[previous[current]]:
                        if weights[neighbor] == float('inf'):
                            numfull += 1
                    #if they are then there are no valid paths and bandwidth must be increased
                    if numfull == len(graph[previous[current]]):
                        for neighbor in graph[previous[current]]:
                            weights[neighbor] = 1
                            bandwidths[neighbor] += 1
                for neighbor in graph[current]:
                    if previous[neighbor] == -1 and weights[current] == 1 and neighbor != isp:
                        previous[neighbor] = current
                        unvisited.append(neighbor)
            for client in list_clients:
                if len(paths[client]) < 2:
                    path = []
                    current_node = client
                    while current_node != -1:
                        path.append(current_node)
                        if current_node != client:
                            bandwidthused[current_node] += 1
                        current_node = previous[current_node]
                    path.reverse()
                    paths[client] = path
            #Checks if bandwidth has been exceeded
            for node in bandwidthused:
                if bandwidthused[node] > bandwidths[node]:
                    index = 0
                    while bandwidthused[node] > bandwidths[node] and index < len(priority_list):
                        client = priority_list[index]
                        if node != client and node in paths[client]:
                            change = True
                            for item in paths[client]:
                                if item != client:
                                    bandwidthused[item] -= 1
                            paths[client] = []
                        index += 1
                    weights[node] = float('inf')
            #Checks if all paths are valid
            totalpaths = 0
            for path in paths:
                if len(paths[path]) > 1:
                    totalpaths += 1
            if totalpaths == len(list_clients):
                nochanges = True
            else:
                nochanges = False
            loop += 1
        print(paths)
        return (paths, bandwidths, priorities)
