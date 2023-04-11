import sys
import pickle
import copy
from Utility import Utility
from Solution import Solution
from Simulator import Simulator
from Revenue import Revenue
from Traversals import bfs_path


class Driver:

    def __init__(self):
        if len(sys.argv) < 2:
            print("Please provide the testcase filepath as a command line argument")
            return
        self.problem = 2
        filename = sys.argv[1]
        utility = Utility(self.problem)
        input = utility.read_file(filename)
        info = utility.read_info(filename + "-info")
        input_copy = copy.deepcopy(input)
        info_copy = copy.deepcopy(info)
        s = Solution(self.problem, input.isp, input.graph, info)
        (paths, bandwidths, priorities) = s.output_paths()
        revenue = 0
        info_copy["shortest_delays"] = bfs_path(
            input_copy.graph, input_copy.isp, info_copy["list_clients"])
        info_copy["shortest_delays"] = {
            k: len(v)-1 for k, v in info_copy["shortest_delays"].items()}
        if not paths:
            pass
        else:
            revenue = self.run_helper(
                input_copy, info_copy, paths, bandwidths, priorities)

        print("Your Solution")
        print("=============================================")
        print("Revenue: " + str(revenue))

    def run_helper(self, input, info, paths, updated_bandwidths=None, priorities=None):

        simulator = Simulator()

        list_clients = info['list_clients']
        bandwidths = info['bandwidths'] if not updated_bandwidths else updated_bandwidths
        alphas = info['alphas']
        betas = None if 'betas' not in info else info['betas']
        shortest_delays = info['shortest_delays']
        payments = info['payments']

        is_rural = None if 'is_rural' not in info else info['is_rural']
        is_fcc = None if 'is_fcc' not in info else info['is_fcc']
        rho_lawsuit = 1 if 'rho1' not in info else info['rho1']
        lawsuit = 0 if 'lawsuit' not in info else info['lawsuit']
        rho_fcc = 1 if 'rho2' not in info else info['rho2']
        fcc_fine = 0 if 'fcc_fine' not in info else info['fcc_fine']
        cost_bandwidth = 0 if 'cost_bandwidth' not in info else info['cost_bandwidth']

        simulator.run(input.graph, input.isp, list_clients,
                      paths, bandwidths, priorities, is_rural)

        client_delays = simulator.get_delays(list_clients)

        apply_pen_1 = apply_pen_2 = False

        if 3 <= self.problem <= 4:
            apply_pen_1 = True
            apply_pen_2 = True

        revenue = Revenue().revenue([client_object for client_object in simulator.get_clients(list_clients).values()], alphas, betas, shortest_delays,
                                    payments, lawsuit, rho_lawsuit, fcc_fine, rho_fcc, is_fcc, apply_pen_1, apply_pen_2, bandwidths, info["bandwidths"], cost_bandwidth, self.problem)

        return revenue


Driver()
