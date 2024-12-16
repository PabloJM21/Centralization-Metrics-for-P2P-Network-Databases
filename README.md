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
  3. Analyze the frequency distribution of node degrees.
  4. Calculate the **weighted variance** of the degree distribution to assess centralization.

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



---

### 2. **Latency-Based Distribution**
**Purpose**: Analyzes centralization based on the uptime of the nodes during crawling.  
- Nodes with low crawl durations indicate connectivity issues.
- Networks with a high variance in crawl durations indicate inconsistency in the reliability of the nodes.  
- **Steps**:
  1. Compute average latency (e.g.`crawl_duration`) for each node.
  2. Compute the variance of these latencies.
   
- **Output**: Variance of latency distributions.

---

### 3. **ISP Centralization**
**Purpose**: Examines how nodes in the network are distributed across Internet Service Providers (ISPs).  
- ISP centralization can lead to bottlenecks if a small number of ISPs control a significant portion of network traffic.  
- **Steps**:
  1. Map each node’s IP address to its ISP.
  2. Compute the distribution of nodes across ISPs.
  3. Analyze the percentage of nodes controlled by the top ISPs.  
- **Output**: Gini coefficient or percentage of nodes controlled by the top ISPs.

#### Steps in Variance Calculation

Variance is a measure of the dispersion or spread in a set of data points, indicating how far the values deviate from the mean. Below are the steps involved in computing variance:

### 1. Calculate the Mean (Average)
The mean is computed as:
```math
\text{Mean} = \frac{\sum_{i=1}^n f_i}{n}
```
Where:
- $f_i$: Frequency of the $i$-th data point (e.g., a country’s occurrence).
- $n$: Total number of data points.



### 2. Compute the Deviations
For each data point, calculate the difference between its value and the mean:
```math
\text{Deviation for } f_i = f_i - \text{Mean}
```



### 3. Square the Deviations
Square each deviation to eliminate negative values:
```math
(\text{Deviation for } f_i)^2 = (f_i - \text{Mean})^2
```



### 4. Average the Squared Deviations
Sum all squared deviations and divide by $n - 1$ (sample variance):
```math
\text{Variance} = \frac{\sum_{i=1}^n (f_i - \text{Mean})^2}{n - 1}
```

This gives a single numerical value representing the spread of the data points.

---






## Results

### 1. **Degree Distribution**

![Degree Distribution Plot](images/bins_degree_distribution_nebula_polkadot.png "Degree Distribution")

weighted variance: 27553.19049212474

![Degree Distribution Plot](images/bins_degree_distribution_nebula_avail_mainnet.png "Degree Distribution")

weighted variance: 7151.645454149878

![Degree Distribution Plot](images/bins_degree_distribution_nebula_filecoin.png "Degree Distribution")

weighted variance: 43146.03780494059

![Degree Distribution Plot](images/bins_degree_distribution_nebula_ipfs.png "Degree Distribution")

weighted variancen: 306545.76279855054


### 2. **Latency-Based Distribution**


| Database          | avg.crawl duration variance |
|-------------------|-----------------------------|
| IPFS              | 215.2023919892557           |
| Filecoin          | 137.9478481490786           |
| Polkadot          | 242.98945260622315          |
| Avail Mainnet     | 315.3813616571848           |



## Repository Structure


