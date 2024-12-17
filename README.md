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

### 3. **IP Address Centralization**

**Purpose**: Analyzes how nodes in the network are distributed across IPv4 and IPv6 address prefixes.  

- **Centralization in Address Prefixes**:  
  IP address prefixes represent logical groupings of addresses, reflecting how networks are allocated across geographical regions or organizations. Centralization in these prefixes can reveal the extent to which network traffic or resources are concentrated within a few address ranges.  

- **Steps**:  
  1. **Extract Address Prefixes**:  
      - For IPv4 addresses, extract the `/24` prefix (e.g., `192.168.1.x`).  
      - For IPv6 addresses, extract the `/48` prefix (e.g., `2001:db8:abcd`).  
  2. **Count Prefix Frequencies**: Compute the number of nodes associated with each prefix.  
  3. **Quantify Centralization**: Apply metrics to evaluate how address prefixes are distributed, such as:  
      - **Gini Coefficient**: Measures inequality in prefix frequencies, with higher values indicating greater concentration.  
      - **Top Prefix Contribution**: Calculate the percentage of nodes associated with the most frequent prefixes.  

- **Output**:  
  Metrics such as the Gini coefficient or the proportion of nodes associated with the top prefixes provide a quantifiable view of IP address centralization. These insights help identify regions or organizations that dominate the network, potentially exposing vulnerabilities or bottlenecks.




### **Steps to Compute the Gini Coefficient**

The following outlines the step-by-step process for calculating the Gini coefficient:


#### **Flatten the Array**
`array = array.flatten()`

- **Purpose**: Ensure the input is a 1D array.
- **Result**: If the input is multidimensional, it becomes:
  \[
  x = [x_1, x_2, \dots, x_n]
  \]



#### **Handle Negative Values**
`if np.amin(array) < 0: array -= np.amin(array)`

- **Purpose**: Adjust the array to remove any negative values.
- **Result**: Shift all elements so the minimum value becomes zero:
  \[
  x_i = x_i - \min(x) \quad \forall \, x_i \in x
  \]



#### **Avoid Zero Values**
`array = array + 0.0000001`

- **Purpose**: Add a small constant (\( \epsilon \)) to prevent division errors or issues with zeros.
- **Result**: 
  \[
  x_i = x_i + \epsilon \quad \forall \, x_i \in x
  \]



#### **Sort the Array**
`array = np.sort(array)`

- **Purpose**: Sort the array in ascending order.
- **Result**: 
  \[
  x_1 \leq x_2 \leq \ldots \leq x_n
  \]



#### **Compute Index Values**
`index = np.arange(1, array.shape[0] + 1)`

- **Purpose**: Assign indices \( i \) to each sorted element.
- **Result**:
  \[
  \text{index} = [1, 2, \dots, n]
  \]



#### **Total Number of Elements**
`n = array.shape[0]`

- **Purpose**: Get the total number of elements \( n \).
- **Result**:
  \[
  n = \text{len}(x)
  \]



#### **Calculate the Gini Coefficient**

**Step 1: Compute the Weighted Sum**


```math
\text{Weighted Sum} = \sum_{i=1}^{n} (2i - n - 1) \cdot x_i
```

**Step 2: Normalize by Total Array Sum**
`denominator = n * np.sum(array)`

\[
\text{Denominator} = n \cdot \sum_{i=1}^{n} x_i
\]

**Step 3: Compute the Gini Coefficient**
`return weighted_sum / denominator`

\[
G = \frac{\sum_{i=1}^{n} (2i - n - 1) \cdot x_i}{n \cdot \sum_{i=1}^{n} x_i}
\]



#### **Final Formula**
The Gini coefficient is computed as:
```math
G = \frac{\sum_{i=1}^{n} (2i - n - 1) \cdot x_i}{n \cdot \sum_{i=1}^{n} x_i}

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


