# Centralization Metrics for P2P Network Databases

This project analyzes the centralization of peer-to-peer (P2P) networks using three key metrics: **Degree Distribution**, **Latency-Based Distribution**, and **ISP Centralization**. The metrics are computed for the following databases:
- `nebula_ipfs`
- `nebula_polkadot`
- `nebula_avail_mainnet`
- `nebula_filecoin`

The analysis helps to identify potential centralization bottlenecks in P2P overlays and provides insights into the distribution of network resources.

---

## Metrics Overview


  
#### Degree Centrality in Undirected Graphs

Degree centrality measures how many direct connections (or edges) a node in a graph has relative to the maximum possible number of connections. Below is the step-by-step explanation for computing degree centrality in this context.

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

   
#### Shannon Entropy 

Measures the distribution of a continuous quantity (e.g., crawl durations) across nodes in a network and determines if it is even or centralized.


```math
H = -\sum_{i=1}^n p_i \cdot \log(p_i)
```

```math
H_{\text{normalized}} = \frac{H}{\log(n)}
```

where 

```math
p_i = \frac{x_i}{\sum_{j=1}^n x_j}
```

#### Interpretation
- **Higher Entropy**: $H_{\text{normalized}}=1$ indicates Uniform distribution across nodes. 
- **Lower Entropy**: Centralized distribution dominated by a few nodes.
 


---

**Gini Coefficient**

The Gini coefficient is computed based on the Weighted Sum and Denominator:


```math
G = \frac{\text{Weighted Sum}}{\text{Denominator}} = \frac{\sum_{i=1}^{n} (2i - n - 1) \cdot x_i}{n \cdot \sum_{i=1}^{n} x_i}
```

where:

total number of elements \( n \).

```math
  n = \text{len}(x)
```




---





## Results

### 1. **Degree Distribution**

![Degree Distribution Plot](images/bins_degree_distribution_nebula_polkadot.png "Degree Distribution")



![Degree Distribution Plot](images/bins_degree_distribution_nebula_avail_mainnet.png "Degree Distribution")



![Degree Distribution Plot](images/bins_degree_distribution_nebula_filecoin.png "Degree Distribution")



![Degree Distribution Plot](images/bins_degree_distribution_nebula_ipfs.png "Degree Distribution")



#### Degree Centralization

| Database             | Average Outdegree Centralization | Average Indegree Centralization | Average Combined Centralization |
|----------------------|----------------------------------|---------------------------------|---------------------------------|
| nebula_polkadot      | 0.378                            | 0.868                           | 0.753                           |
| nebula_avail_mainnet | 0.466                            | 0.813                           | 0.603                           |
| nebula_filecoin      | 0.129                            | 0.876                           | 0.808                           |
| nebula_ipfs          | 0.273                            | 0.931                           | 0.884                           |


The table displays the degree centralization rate for the Outdegree, Indegree and the combination of both. We realize that the Outdegree exhibits lower centralization scores reflecting a more decentralized structure, while the Indegree's centralization scores are much higher, hence the total network has a more centralized structure.  

### 2. **Latency-Based Distribution**


| **Database**             | **Normalized Entropy** | **Number of Peers** |
|--------------------------|------------------------|---------------------|
| nebula_filecoin          | 0.823                  |     54234.8         |
| nebula_polkadot          | 0.842                  |     2697.2          |
| nebula_avail_mainnet     | 0.715                  |     8582.6          |
| nebula_ipfs              | 0.932                  |     855.8           |


### 3. **Country Centralization**


| **Database**             | **Gini Coefficient** | Number of Peers |
|--------------------------|----------------------|-----------------|
| nebula_ipfs              | 0.927                | 54234.8         |
| nebula_filecoin          | 0.934                | 2697.2          |
| nebula_polkadot          | 0.930                | 8582.6          |
| nebula_avail_mainnet     | 0.772                | 855.8           |



### 4. **IP-Address Centralization**


| Database                | Gini Coefficient | Number of Peers |
|-------------------------|------------------|-----------------|
| nebula_ipfs             | 0.510            | 54234.8         |
| nebula_filecoin         | 0.653            | 2697.2          |
| nebula_polkadot         | 0.722            | 8582.6          |
| nebula_avail_mainnet    | 0.387            | 855.8           |

### 5. ASN centralization

| Database                | Gini Coefficient | Number of Peers |
|-------------------------|------------------|-----------------|
| nebula_ipfs             | 0.981            | 54234.8         |
| nebula_filecoin         | 0.946            | 2697.2          |
| nebula_polkadot         | 0.986            | 8582.6          |
| nebula_avail_mainnet    | 0.819            | 855.8           |



### IPFS frequency bump

In this section we will study the IPFS networks in more detail paying special attention to the frequency bump in the range $[50,80]$.

We will start by studying the in-degree, which is the proportion of direct neighbors among all the nodes present.

The neighbor type of each node, whether direct or reversed, might give information about the function of that node.
For example, nodes without reversed neighbors likely act as clients that connect exclusively to a few other nodes acting as providers.
At each degree we will show the frequency as before, but also the out-degree ratio.

To simplify the analysis we will focus on one crawl.

![Degree Distribution Plot](images/filtered_neighbors_nebula_ipfs_19604.png "Degree Distribution")


Now we will view the ratio of direct neighbors among all nodes at each specific degree.


![Degree Distribution Plot](images/filtered_direct_neighbor_ratio_nebula_ipfs_19604.png
 "Degree Distribution")

We can see that in the degree range with the highest frequency the out-degree dominates the in-degree.
This means that most of the users are sending to other nodes rather than receiving from them.  
In the rest of the degree range there are more fluctuations in the out-degree ratio.

In order to obtain more information about this frequency bump we observe in degree range $[50, 80]$, we will proceede computing some of the centralization metrics we used before. 
Starting with IP-Address Centralization, we will extract the address prefixes as before and compute the number of peers and gini coefficient.


| Category  | Gini Coefficient | Number of Peers |
|-----------|------------------|-----------------|
| Whole     | 0.509            | 53851           |
| Filtered  | 0.215            | 1473            |


As we can see in the Table, the filtered dataset is still bigger than the avail mainnet we saw before. However the Gini Coefficient is lower, meaning lower inequality in the address prefixes. 

So despite having more peers, this subset of the IPFS network has more variety of IP address prefixes.


Another question that arises looking at the frequency bump is if it corresponds to a subnetwork disconnected from the rest. To address this question we will extract all nodes the subset in the degree range $[50, 80]$ are connected to. If the subset is well integrated in the network, they should reach almost all nodes.

We will take the subset of nodes plus their neighbors and dispay the resulting degree-frequency plot. Depending on how similar it looks to the original plot we can determine how close this subset is to the whole network.

The original plot of that crawl looks as follows:

![Degree Distribution Plot](images/neighbors_nebula_ipfs_19604.png
 "Degree Distribution")

 While for the subset of nodes and their neighbors it looks like this:

 ![Degree Distribution Plot](images/relevant_neighbors_degree_range_50_80_nebula_ipfs_19604.png
 "Degree Distribution")

 As we see, both plots are almost identical, seflecting the strong conectivity of the subset of nodes causing the frequency bump.


