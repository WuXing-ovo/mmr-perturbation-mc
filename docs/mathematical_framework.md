# A mathematical framework for MMR system analysis

*This document serves as a continuous development log rather than a finalized academic report.*

## Status

Figuring out suitable variables to measure the matchmaking system as a signle metric (like MSE) can not fully capture it.

## Players

### Definition of Players

For a system consisting of a population of $N$ players, each player $i$ is defined by a tuple of two scalar values:
$$
\text{Player}_{i}=\left(V_{i},H_{i}\right)
$$

- $H_{i}$(Hidden MMR / True Skill): This is the immutable ground truth of a player's ability (for static system). It is used to determine the outcome of a match and evaluate the stability of system.
- $V_{i}$(Visible MMR / Rank): This is the system's current estimation of a player. It is used by the matchmaking algorithm to find opponents.

### Initialization of Players

Consider a system with N players, and introduce a parameter $\alpha$ (where $\alpha \in [0,1]$), which represents the proportion of anomalous players.
For normal players ($S_{n}$), $H_{i}$ is drawn from Standard Normal Distribution, and $V_{i}$ is equal to $H_{i}$.
$$
H_{i} \sim \mathcal{N}(0,1)
$$
$$
V_{i}=H_{i}
$$
For anomalous players ($S_{a}$), the relation between $V$ and $H$ is explicitly broken. To simulate Smurfs and Boosted Accounts, set $H$ and $V$ with different $\mu$ is an easy way to initialize. Calculating the initial MSE with $MSE=\frac{1}{N\alpha}\sum\limits_{i\in S_{a}}(V_{i}-H_{i})^{2}$ is a good way to quantify the initial deviation. The choice of $\mu$ determines the initial deviation of the system.
To study the deviation of the overall MSE, we calculate it across all players, the parameter $t$ here is the number of steps.
$$
MSE(t)=\frac{1}{N}\sum\limits_{i=1}^{N}(V_{i}(t)-H_{i})^{2}
$$
If $\Delta \mu$ keeps same between two kinds of anomalous players (with deterministic offset), the initial MSE is equal to $\Delta \mu^{2}\cdot\alpha$.

## Win/Loss Estimator

This estimator is used to decide the outcome of a match in reality. To introduce nondeterminacy, the estimator consists of two parts, Bradley-Terry logistic function and a random number generator.
$$
P(i)=\frac{1}{1+e^{\beta(H_{j}-H_{i})}}
$$
$H_{i}$ and $H_{j}$ are true skills of players, and $\beta$ is adjusted uncertainty.
To translate the continuous probability into a discrete match outcome, the module generates a standard uniform random variable:
$$
U \sim \mathcal{U}(0,1)
$$
The outcome is then evaluated by this function
$$
\begin{cases}
U<P(i), \quad \text{Player i wins} \\
U\ge P(i), \quad \text{Player j wins} \\
\end{cases}
$$

## Matchmaking Algorithm

### 1v1 Elo

The input matchmaking pool is a vector contains the current visible rating of $N$ players. Then sort elements in descending or ascending based strictly on their visible rating and create matches by pairing strictly adjacent elements. It will generate a $2 \times \frac{N}{2}$ matrix.

However, the result from adjacent matching failed to converge. It seems that the pairings remain unchanged during the simulation. In contrast, random-matching converges very fast, although it's not acceptable for real games. For the sake of prototyping, the 1v1 Elo matchmaking system will use random-matching algorithm.

### 5v5 TrueSkill 2

Work In Progress.

## Rating Update

### 1v1 Elo

$$
V_{A}(t+1)=V_{A}+K(S_{A}-P_{sys}(A))
$$
Where $V_{A}(t)$ is the Visible MMR, $S_{A}$ is the result from Win/Loss Estimator with Hidden MMR, $P_{sys}(A)$ is the probability given by the estimator with Visible MMR (Bradley-Terry logistic function), $K$ is a hyper parameter.

### 5v5 TrueSkill 2

Work In Progress.
