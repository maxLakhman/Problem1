class Revenue:

    def __init__(self):
        """
        constructor
        """
        # list of complaining clients
        self.complaints = []

    def pen_0(self, client, optimal, alpha, pmt):
        """
         calculates how much each client pays
         :param client: an client object
         :param optimal: the delay on the optimal solution
         :param alpha: the client's tolerence
         :param pmt: how much the client owes
         :return: pmt, unless the client leaves in whichcase, 0
         """
        if client.delay > alpha * optimal:
            self.complaints.append(client)
            return 0
        return pmt

    def pen_1(self, law_suit, rho, client_list):
        """
         calculates the effects of the law suit
         :param law_suit: the amount owed if the lawsuit is brought up
         :param rho: how likely one is to end up in a lawsuit
         :param client_list: list of clients
         :return: 0 if the lawsuit isnt brought up, otherwise the negative amount of the lawsuit
         """
        if len(self.complaints) >= int(rho * len(client_list)):
            return -law_suit
        return 0

    def pen_2(self, rho_fcc, is_fcc, penalty):
        """
        determines wehter or not the fcc comes to get you
        :param rho_fcc: the fcc's tolerance
        :param is_fcc: mapping from client IDs to whether they are a part of FCC's batch
        :param penalty: the penalty paid if they catch you
        :return: 0 if you arent caught, otherwise the negative of the amount of the FCC fine
        """
        count = 0
        for client in self.complaints:
            if is_fcc[client.id]:
                count += 1

        # This calculates the number of clients that will complain to the FCC
        # if their internet is slow
        num_fcc = sum(1 for x in is_fcc.values() if x == 1)
        if count >= int(num_fcc * rho_fcc):
            return -penalty
        return 0

    def pen_bandwidth(self, updated: dict, original: dict, update_cost: int):
        # These refer to the same object if bandwidths haven't been updated
        # todo: verify the above is correct
        if updated is original:
            return 0
        cost = 0
        for node, bandwidth in original.items():
            diff = updated[node] - bandwidth
            if diff > 0:
                cost += diff*update_cost
        return -cost

    def revenue(self, client_list, alphas, betas, optimal_dict, payments, lawsuit, rho_lawsuit, fcc_fine, rho_fcc, is_fcc,
                pen_1, pen_2, updated_bandwidths, original_bandwidths, update_cost, problem):
        """
        determines overall revenue
         
        :param client_list: list of client objects
        :param alphas: mapping of clients to their alpha values
        :param betas: mapping of clients to their beta values
        :param optimal_dict: mapping of clients to their optimal delays
        :param payments: mapping of clients to their payment values
        :param lawsuit: lawsuit cost
        :param rho_lawsuit: lawsuit factor
        :param rho_fcc: fcc factor
        :param is_fcc: mapping of nodes to either 0 or 1
        :param fcc_fine: fcc penalty
        :param pen_1: if the lawsuit should be taken into account
        :param pen_2: if the fcc should be taken into account
        :param updated_bandwidths mapping of nodes to new bandwidths as set by the solution
        :param original_bandwidths mapping of nodes to original bandwidths as provided by the problem
        :param cost to upgrade the bandwidth by 1

        :return: the total revenue
        """
        rev = 0

        for client in client_list:

            curr_revenue = self.pen_0(
                client, optimal_dict[client.id], alphas[client.id], payments[client.id])
            if problem == 5 and not curr_revenue:
                # for problem 5 if a single client had their packet delayed, zero out the revenue
                return 0
            rev += curr_revenue

            if (pen_1 or pen_2) and curr_revenue != 0:
                if (client.delay > betas[client.id] * optimal_dict[client.id]):
                    self.complaints.append(client)

        if pen_1:
            rev += self.pen_1(lawsuit, rho_lawsuit, client_list)

        if pen_2:
            rev += self.pen_2(rho_fcc, is_fcc, fcc_fine)

        if updated_bandwidths:
            rev += self.pen_bandwidth(updated_bandwidths,
                                      original_bandwidths, update_cost)

        return rev
