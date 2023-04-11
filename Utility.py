import re
from Graph import Graph
from Enums import Info


class Utility:

    def __init__(self, problem):
        self.problem = problem

    def read_file(self, input_file):
        isp = 0
        node = 0
        graph = {}

        # Reading and parsing the file
        with open(input_file, 'r') as file:
            isp = int(file.readline())
            for line in file:
                adjacency_list = [int(neighbor) for neighbor in line.split()]
                graph[node] = adjacency_list
                node += 1

        return Graph(isp, graph)

    def read_info(self, input_file):

        list_clients = []
        bandwidths = {}
        alphas = {}
        payments = {}
        betas = {}
        is_rurals = {}
        is_fccs = {}
        rho1 = None
        rho2 = None
        lawsuit = None
        fcc_fine = None
        cost_bandwidth = None

        with open(input_file, 'r') as file:

            if 3 <= self.problem <= 4:
                rho1 = float(file.readline())
                rho2 = float(file.readline())
                lawsuit = float(file.readline())
                fcc_fine = float(file.readline())

            if 3 <= self.problem <= 5:
                cost_bandwidth = float(file.readline())

            for i, line in enumerate(file.readlines()):

                info = line.split()
                if int(info[Info.IS_CLIENT.value]) == 1:

                    list_clients.append(i)
                    alpha_c = float(info[Info.ALPHAS.value])
                    alphas[i] = alpha_c if alpha_c >= 1 else float("inf")
                    payments[i] = float(info[Info.PAYMENTS.value])

                    if 3 <= self.problem <= 4:
                        beta = float(info[Info.BETAS.value])
                        betas[i] = beta if beta >= 1 else float("inf")
                        is_fccs[i] = int(info[Info.IS_FCC.value])

                    if self.problem == 4:
                        is_rurals[i] = int(info[Info.IS_RURAL.value])

                    # set the client's alpha to infinity if it's rural since it
                    # is not in a position to complain
                    if is_rurals and is_rurals[i] == 1:
                        alphas[i] = float("inf")

                bandwidth = int(info[Info.BANDWIDTHS.value])
                bandwidths[i] = bandwidth if bandwidth > 0 else float("inf")

        info = {}

        info["list_clients"] = list_clients
        info["bandwidths"] = bandwidths
        info["alphas"] = alphas
        info["payments"] = payments

        if betas:
            info["betas"] = betas
        if is_rurals:
            info["is_rural"] = is_rurals
        if is_fccs:
            info["is_fcc"] = is_fccs
        if rho1:
            info["rho1"] = rho1
        if rho2:
            info["rho2"] = rho2
        if lawsuit:
            info["lawsuit"] = lawsuit
        if fcc_fine:
            info["fcc_fine"] = fcc_fine
        if cost_bandwidth:
            info["cost_bandwidth"] = cost_bandwidth

        return info
