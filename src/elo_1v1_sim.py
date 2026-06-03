import numpy as np

class SimulationState:
    def __init__(self, N, alpha, delta_mu=1) -> None:
        # Initialize Hidden MMR and Visible MMR
        self.H = np.random.normal(0, 1, size=N)
        self.V = self.H.copy()

        # Introduce anomalous players
        smurfs = self.V[N - int(alpha * N) : N - int(alpha / 2 * N)]
        boosted = self.V[N - int(alpha / 2 * N) : ]
        smurfs [:] -= delta_mu
        boosted [:] += delta_mu

    def get_MSE(self):
        """Return MSE"""
        return np.mean(np.square(self.H - self.V))

def estimator(H_1, H_2, beta):
    """Win/Loss Estimator, return 1 if H_1 wins, and return 0 if H_2 wins"""
    odds = 1 / (1 + np.exp(beta * (H_2 - H_1)))
    random_numbers = np.random.uniform(size=len(odds))
    results = random_numbers < odds
    return results.astype(int)

def matchmaker(V):
    """Matchmaking algorithm for 1v1 Elo"""
    index = np.argsort(V)
    idx_1 = index[0::2]
    idx_2 = index[1::2]
    return idx_1, idx_2
