from enum import Enum

class Info(Enum):
    '''
    The number represents the indexing of the corresponding value
    in the testcases info files for eg. the first integer in a line
    representing a particular node represents whether it is a client or not
    '''
    IS_CLIENT = 0
    BANDWIDTHS = 1
    ALPHAS = 2
    PAYMENTS = 3
    BETAS = 4
    IS_FCC = 5
    IS_RURAL = 6
