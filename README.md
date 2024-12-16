# Centralization Metrics for P2P Network Databases

This project analyzes the centralization of peer-to-peer (P2P) networks using three key metrics: **Degree Distribution**, **Latency-Based Distribution**, and **ISP Centralization**. The metrics are computed for the following databases:
- `nebula_ipfs`
- `nebula_polkadot`
- `nebula_avail_mainnet`
- `nebula_filecoin`

The analysis helps to identify potential centralization bottlenecks in P2P overlays and provides insights into the distribution of network resources.

---

## Metrics Overview

### 1. **Degree Distribution**
**Purpose**: Measures the connectivity of nodes in the P2P network.  
- Nodes with higher degrees are more central, potentially serving as hubs in the network.  
- **Steps**:
  1. Extract the neighbors of each node.
  2. Calculate the degree of each node (number of neighbors).
  3. Analyze the frequency distribution of node degrees and compute variance to assess centralization.
  4. 4. Calculate the **weighted variance** of the degree distribution to assess centralization.

**Formula**:  
The **weighted variance** $\sigma_w^2$ is computed as:  

```math
\sigma_w^2 = \frac{\sum_{i} w_i \cdot (x_i - \mu_w)^2}{\sum_{i} w_i}
```
Where:
- $x_i$: Center of each degree bin.
- $w_i$: Average frequency of nodes in bin \( i \).
- $\mu_w$: Weighted mean of the degree distribution, calculated as:
  
```math
\mu_w = \frac{\sum_{i} w_i \cdot x_i}{\sum_{i} w_i}
```
    
- **Output**: A weighted variance of the degree distribution, indicating how evenly connectivity is spread across the network.

![Degree Distribution Plot](images/bins_degree_distribution_nebula_avail_mainnet.png "Degree Distribution")

---

### 2. **Latency-Based Distribution**
**Purpose**: Analyzes centralization based on latency in network communication.  
- Nodes with consistently lower latencies may act as de facto hubs for routing and communication.  
- **Steps**:
  1. Compute average latency (e.g., `dial_duration`, `crawl_duration`) for each node.
  2. Analyze the distribution of latencies across all nodes.
  3. Identify outliers with significantly low or high latencies.  
- **Output**: Variance or other statistical summaries of latency distributions.

---

### 3. **ISP Centralization**
**Purpose**: Examines how nodes in the network are distributed across Internet Service Providers (ISPs).  
- ISP centralization can lead to bottlenecks if a small number of ISPs control a significant portion of network traffic.  
- **Steps**:
  1. Map each node’s IP address to its ISP.
  2. Compute the distribution of nodes across ISPs.
  3. Analyze the percentage of nodes controlled by the top ISPs.  
- **Output**: Gini coefficient or percentage of nodes controlled by the top ISPs.

---

## Repository Structure


