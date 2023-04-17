from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info
        
    def output_paths(self):
        isp = self.isp
        graph = self.graph
        list_clients = self.info["list_clients"]
        bandwidthlist = self.info["bandwidths"]
        bandwidthnum = {node: 0 for node in graph.keys()}
        tolerances = self.info["alphas"]
        paths, bandwidths, priorities = {}, {}, {}
        graph_size = len(graph)
        priors = [-1]*graph_size
        search_queue = deque()
        pathsfound = {node: False for node in list_clients}
        layerfull = {}
        allpathsfound = False
        sortednodes = sorted(list_clients, key=lambda x: tolerances[x], reverse=True)
        numpaths = 0
        while(not allpathsfound):
            search_queue.append(isp)
            while search_queue:
                node = search_queue.popleft()
                for neighbor in graph[node]:
                    if (priors[neighbor] == -1 and bandwidthnum[node] < bandwidthlist[node] and neighbor != isp):
                        priors[neighbor] = node
                        search_queue.append(neighbor)
            bandwidthnum = {node: 0 for node in graph.keys()}
            for client in list_clients:
                if(not pathsfound[client]):
                    path = []
                    current_node = client
                    while (current_node != -1):
                        path.append(current_node)
                        if(current_node != client):
                            bandwidthnum[current_node] += 1
                        current_node = priors[current_node]
                    path = path[::-1]
                    paths[client] = path
                    pathsfound[client] = True
                    numpaths += 1
                else:
                    for item in paths[client]:
                        if(item != client):
                            bandwidthnum[item] += 1
            for node in bandwidthnum:
                if bandwidthnum[node] > bandwidthlist[node]:
                    for client in sortednodes:
                        if node in paths[client] and node != client:
                            for item in paths[client]:
                                if item != node:
                                    bandwidthnum[item] -= 1
                            pathsfound[client] = False
                            numpaths -= 1
                            paths[client] = []
                            bandwidthnum[node] -= 1
                        bandwidthnum[isp] = sum([bandwidthnum[node] for node in graph[isp]])
                        if bandwidthnum[node] <= bandwidthlist[node]:
                            break
            if(numpaths == len(list_clients)):
                allpathsfound = True
            else:
                priors = [-1]*graph_size           
        return (paths, bandwidths, priorities)