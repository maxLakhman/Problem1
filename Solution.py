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
        pathsthatusenode = {node: list() for node in graph.keys()}
        for client in list_clients:
            path = []
            current_node = client
            while (current_node != -1):
                path.append(current_node)
                if(current_node != client):
                    bandwidthused[current_node] += 1
                    pathsthatusenode[current_node].append(client)
                current_node = priors[current_node]
            path = path[::-1]
            paths[client] = path
        #Figure out delay for each client
        complaintlist = list()
        delay = {client: 0 for client in list_clients}
        currentcycle = {node: 1 for node in graph.keys()}
        for path in paths:
            for item in paths[path]:
                if(item != path):
                    delay[path] += currentcycle[item]
                    if ((bandwidthused[item] - currentcycle[item]) % bandwidths[item] == 0):
                        currentcycle[item] += 1
        print(delay)
        #Find who will complain
        complaintthreshold = {client: len(bfspaths[client]) * toleranceb[client] for client in list_clients}
        for client in delay:
            if delay[client] > complaintthreshold[client]:
                complaintlist.append(client)
        complaintlistsorted = sorted(complaintlist, key=lambda x: payments[x], reverse = True)
        #Increase bandwidth for full nodes and for clients (lawsuit)
        if len(complaintlist) >= len(list_clients) * plawsuit:
            for client in complaintlistsorted:
                i = 0
                while delay[client] >= complaintthreshold[client] and i < len(paths[client]):
                    if bandwidthused[paths[client][i]] > bandwidths[paths[client][i]] and paths[client][i] != client:
                        bandwidths[paths[client][i]] += 1
                        delay[client] -= 1
                    i += 1
                complaintlist.remove(client)
        #Now calculated for fcc
        if len(complaintlist) >= len(fcclist) * pfcc:
            for client in complaintlistsorted:
                i = 0
                while delay[client] >= complaintthreshold[client] and i < len(paths[client]):
                    if bandwidthused[paths[client][i]] > bandwidths[paths[client][i]] and paths[client][i] != client:
                        bandwidths[paths[client][i]] += 1
                        delay[client] -= 1
                    i += 1
                complaintlist.remove(client)
        return (paths, bandwidths, priorities)
