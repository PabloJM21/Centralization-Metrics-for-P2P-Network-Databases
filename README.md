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
  4. Calculate the **degree centrality** of the graph to assess centralization.
  
#### Degree Centrality in Undirected Graphs

Degree centrality measures how many direct connections (or edges) a node in a graph has relative to the maximum possible number of connections. Below is the step-by-step explanation for computing degree centrality in this context:


#### **Graph Setup**
Consider an undirected graph $G = (V, E)$, where:
- $V$: set of nodes (vertices).
- $E$: set of edges connecting nodes in $V$.

The total number of nodes is $N = |V|$.



#### **Degree of a Node**
The **degree** of a node $i$, denoted as $d(i)$, is the number of edges connected to it.

```math
d(i) = |\{j \in V : \{i, j\} \in E \}|
```



#### **Degree Centrality**
Degree centrality \( C_D(i) \) for a node \( i \) is the ratio of its degree \( d(i) \) to the maximum possible degree in the graph \( N - 1 \), which occurs when the node is connected to all other nodes in \( V \).

```math
C_D(i) = \frac{d(i)}{N - 1}
```



#### **Degree Centralization**
Degree centralization measures the inequality of degree centrality across all nodes in the graph. It captures how central the most connected node is relative to others.

#### Formula:
```math
C^* = \frac{\sum_{i=1}^{N} \left( C_{\text{max}} - C_D(i) \right)}{(N - 1)(C_{\text{max}} - 0)}
```

Where:
- $C_{\text{max}}$: maximum degree centrality in the graph.
- $C_D(i)$: degree centrality of node $i$.

This normalizes the centralization score to a value between 0 and 1, where:
- $C^* = 1$ indicates a star graph (one central node connected to all others).
- $C^* = 0$ indicates a completely regular graph (e.g., all nodes have the same degree).





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

### 3. **Country Centralization**

**Purpose**: Analyzes how nodes in the network are distributed across countries

- **Steps**:  
  1. **Extract Countries**:   
  2. **Count Country Frequencies**: Compute the number of nodes associated with each country.  
  3. **Quantify Centralization**: Apply Gini Coefficient metric to measures inequality in countries.
 
  





### **Steps to Compute the Gini Coefficient**

The following outlines the step-by-step process for calculating the Gini coefficient:


#### **Flatten the Array**


Ensure the input is a 1D array.

  ```math
  x = [x_1, x_2, \dots, x_n]
  ```



#### **Handle Negative Values**


Adjust the array to remove any negative values.

  ```math
  x_i = x_i - \min(x) \quad \forall \, x_i \in x
  ```



#### **Avoid Zero Values**


Add a small constant (\( \epsilon \)) to prevent division errors or issues with zeros.

 
  ```math
  x_i = x_i + \epsilon \quad \forall \, x_i \in x
  ```



#### **Sort the Array**


Sort the array in ascending order.

```math
x_1 \leq x_2 \leq \ldots \leq x_n
```



#### **Compute Index Values**


Assign indices \( i \) to each sorted element.

```math
\text{index} = [1, 2, \dots, n]
```



#### **Total Number of Elements**

Get the total number of elements \( n \).

```math
  n = \text{len}(x)
```



#### **Calculate the Gini Coefficient**

**Step 1: Compute the Weighted Sum**


```math
\text{Weighted Sum} = \sum_{i=1}^{n} (2i - n - 1) \cdot x_i
```

**Step 2: Normalize by Total Array Sum**


```math
\text{Denominator} = n \cdot \sum_{i=1}^{n} x_i
```

**Step 3: Compute the Gini Coefficient**

```math
G = \frac{Weighted Sum}{Denominator} = \frac{\sum_{i=1}^{n} (2i - n - 1) \cdot x_i}{n \cdot \sum_{i=1}^{n} x_i}
```



#### **Final Formula**
The Gini coefficient is computed as:
```math
G = \frac{\sum_{i=1}^{n} (2i - n - 1) \cdot x_i}{n \cdot \sum_{i=1}^{n} x_i}
```


---

### 4. **IP Address Centralization**

**Purpose**: Analyzes how nodes in the network are distributed across IPv4 and IPv6 address prefixes.  

- **Centralization in Address Prefixes**:  
  IP address prefixes represent logical groupings of addresses, reflecting how networks are allocated across geographical regions or organizations. Centralization in these prefixes can reveal the extent to which network traffic or resources are concentrated within a few address ranges.  

- **Steps**:  
  1. **Extract Address Prefixes**:  
      - For IPv4 addresses, extract the `/24` prefix (e.g., `192.168.1.x`).  
      - For IPv6 addresses, extract the `/48` prefix (e.g., `2001:db8:abcd`).  
  2. **Count Prefix Frequencies**: Compute the number of nodes associated with each prefix.  
  3. **Quantify Centralization**: Apply Gini Coefficient metric to measures inequality in prefix frequencies.   





---





## Results

### 1. **Degree Distribution**

![Degree Distribution Plot](images/bins_degree_distribution_nebula_polkadot.png "Degree Distribution")

**Degree Centrality** : 0.753

![Degree Distribution Plot](images/bins_degree_distribution_nebula_avail_mainnet.png "Degree Distribution")

**Degree Centrality** : 0.603

![Degree Distribution Plot](images/bins_degree_distribution_nebula_filecoin.png "Degree Distribution")

**Degree Centrality** : 0.808

![Degree Distribution Plot](images/bins_degree_distribution_nebula_ipfs.png "Degree Distribution")

**Degree Centrality** : 0.884


### 2. **Latency-Based Distribution**


| Database                 | avg.crawl duration variance |
|--------------------------|-----------------------------|
| nebula_ipfs              | 215.202                     |
| nebula_filecoin          | 137.948                     |
| nebula_polkadot          | 242.989                     |
| nebula_avail_mainnet     | 315.381                     |


### 3. **Country Centralization**


| **Database**             | **Gini Coefficient** |
|--------------------------|----------------------|
| **nebula_ipfs**          | 0.927                |
| **nebula_filecoin**      | 0.934                |
| **nebula_polkadot**      | 0.930                |
| **nebula_avail_mainnet** | 0.772                |



### 4. **IP-Address Centralization**


| Database                | Gini Coefficient |
|-------------------------|------------------|
| nebula_ipfs             | 0.936            |
| nebula_filecoin         | 0.945            |
| nebula_polkadot         | 0.974            |
| nebula_avail_mainnet    | 0.461            |

## Repository Structure


