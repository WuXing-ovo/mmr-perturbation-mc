import numpy as np
import matplotlib.pyplot as plt

class SimulationState:
    def __init__(self, N, alpha, delta_mu=1.0) -> None:
        # Initialize Hidden MMR and Visible MMR
        self.H = np.array(np.random.normal(0, 1, size=N))
        self.V: np.ndarray = self.H.copy()

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
    index = np.random.permutation(len(V))
    idx_1 = index[0::2]
    idx_2 = index[1::2]
    return idx_1, idx_2

def rating_updater(V, results, idx_1, idx_2, beta, K):
    """Update rating for 1v1 Elo"""
    V_1 = V[idx_1]
    V_2 = V[idx_2]
    P_sys = 1 / (1 + np.exp(beta * (V_2 - V_1)))
    Delta = K * (results - P_sys)
    V[idx_1] += Delta
    V[idx_2] -= Delta


total_epochs = 500
N = 10000
alpha = 0.2
delta_mu = 1.5
beta = 1.0
K = 0.05

profile = SimulationState(N, alpha, delta_mu=delta_mu)
mse_history = np.zeros(total_epochs)

for epoch in range(total_epochs):
    print(profile.get_MSE())
    mse_history[epoch] = profile.get_MSE()
    idx_1, idx_2 = matchmaker(profile.V)
    results = estimator(profile.H[idx_1], profile.H[idx_2], beta)
    rating_updater(profile.V, results, idx_1, idx_2, beta, K)

