# DebtRank Methodology

DebtRank is a recursive algorithm that quantifies systemic risk in financial systems. It models the propagation of financial distress through a network of institutions, considering both direct and indirect impacts. This guide provides a detailed mathematical derivation of the algorithm, explaining its significance at each step.

## Mathematical Formulation

**Key Equation:**
The impact of each institution $i$ on its neighbors $j$ (and its neighbors' neighbors/indirect impact) in the financial network is given by:

$$I_i = \sum_j W_{ij}v_j + \beta\sum_j W_{ij} I_j$$

$\sum_j W_{ij} * v_j$ -> represents much money $j$ looses from $i$ times the fraction of total outstanding loans that are owed by institution j: *the potential systemic impact of a default by institution i, taking into account the exposure of institution $j$ and the relative size of institution $j$'s obligations.* This is our direct impact.

$\beta\sum_j W_{ij} I_j$ -> represents the indirect impact of institution i on its neighbors, taking into account the potential for distress to propagate through the network. Here, $I_j$ is the impact of institution $j$ on its own neighbors, and the sum adds up these impacts over all neighbors $j$ of institution $i$. The damping factor $\beta$, $\beta < 1$ reduces the impact of these indirect effects.

## Components of DebtRank

1. **Asset Liability Network (L)**: A matrix representation of financial exposures, where $L_{ij}$ represents the amount loaned by institution $j$ to institution $i$.

2. **Exposure Network (W):**  This matrix represents the risk or exposure between institutions in the event of a default.
    - **Element $W_{ij}$:** This value quantifies the proportion of institution $j$'s capital that would be lost if institution $i$, to whom $j$ has loaned money, defaults.
    - **Calculation:** $W_{ij} = \min[1, L_{ij}/C_j]$, where $L_{ij}$ is the loan from $j$ to $i$, and $C_j$ is the total capital of institution $j$.
    - **Interpretation:** If $W_{ij} = 0.2$, it means that a default by institution $i$ would result in a loss of 20% of institution $j$'s capital.
    - **Limitation:** The exposure is capped at $1$, meaning that the maximum possible loss is 100% of the capital.

3. **Outstanding Loans:** This concept is crucial in understanding the financial obligations and risk exposure within a network of institutions.
    - **Total Outstanding Loans for Institution $i$:** The total amount of outstanding loans $L_i$ for institution $i$ is calculated as $\sum_{j} L_{ji}$. This represents the total amount that other institutions owe to institution $i$.
    - **Fraction of Total Outstanding Loans for Institution $i$:** The fraction of the total outstanding loans in the system that are owed by institution $i$, denoted as $v_i$, is calculated as $v_i = \frac{L_i}{\sum_{j}L_j}$. This fraction is used to assess the relative importance of institution $i$'s loans within the entire system.
    - *Note:* $v_i$ represents the fraction of outstanding loans from institution $i$ relative to all the loans in the system. It helps in understanding the potential impact of defaults and the distribution of risk within the network.

4. **Update Economic Value:**In the context of financial institutions, the health and state of each institution are represented by two vectors $ h $ and $ s $.
    - **Health ($ h_j(t) $):** Represents the economic value or financial stability of institution $ j $ at time $ t $. It is a percentage that reflects the institution's ability to withstand financial shocks and meet its obligations. A value closer to 1 indicates a healthy institution, while a value closer to 0 indicates potential distress.
    - **State ($ s_j(t) $):** Represents the operational status of institution $ j $ at time $ t $. The state can be:
    - **Undistress:** The institution is operating normally and is financially stable.
    - **Distress:** The institution is facing financial difficulties and may be at risk of defaulting on its obligations.
    - **Inactive:** The institution has defaulted or ceased operations.
    The health and state values are constrained as follows:
        - $ h_i(t) \in [0,1] $
        - $ s_i(t) \in \{ \text{Undistress}, \text{Distress}, \text{Inactive} \} $
    These metrics provide insights into the overall financial health of the system and can be used to assess the potential systemic risk and the propagation of financial distress through the network of institutions.
    For more details on the equations for $ h $ and $ s $, see [Dynamics](#dynamics)

5. **Calculate DebtRank:** The DebtRank of a node/set of nodes is calculated as the sum of the decrease in economic value across all nodes, expressed as a percentage of the total economic value of the network.
    - DebtRank of $S_f$ containing only the single node $i$, is expressed as $R_i = \sum_j h_j(t)v_j - h_i(1)v_i$
    - DebtRank of set $S_f$ (set of nodes in distress in the beginning), is expressed as $R_S = \sum_j h_j(t)v_j - \sum_j h_j (1)v_j$
    - In both instances, we disregard the initial health values, $h(1)$, because DebtRank is concerned with the *change* in economic value due to distress or default.

## Dynamics

$$h_i(t) = min[1, h_i(t-1) + \sum_{j|s_j(t-1)=D}W_{ji}h_j(t-1)]$$

$$
s_i(t)=
\begin{cases}
D,  & \text{if $h_i(t) > 0; s_i(t-1) \neq I$} \\
I, & \text{if $s_i(t-1) = D$} \\
s_i(t-1) &\text{otherwise}
\end{cases}
$$
