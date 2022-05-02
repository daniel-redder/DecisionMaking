from expected_value import expected_value
import numpy as np

class mdp():
    def __init__(self,n_states):

        n_states = n_states
        n_observ = n_states

        self.a = A = np.zeros( (n_states, n_observ) )
