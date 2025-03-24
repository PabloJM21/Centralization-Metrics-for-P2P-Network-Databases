import psycopg2
import pandas as pd
import matplotlib.pyplot as plt


# Database connection details
host = "cmi-read.cla0ai5jnqlv.us-east-1.rds.amazonaws.com"
port = "5432"
user = "jahnen_goettingen"
password = "WAvuMJzVk8vfVVofUq4-"


database = #select one of the following databases: "nebula_ipfs" "nebula_filecoin", "nebula_polkadot", "nebula_avail_mainnet"
try:
    print(f"Processing database: {database}")

    # Connect to the database using psycopg2
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    # Query
    query = """
    SELECT crawl_id, peer_id, neighbor_ids
    FROM neighbors
    WHERE crawl_id IN (
        SELECT DISTINCT crawl_id
        FROM neighbors
        ORDER BY crawl_id
        LIMIT 5
    )
    """

    # Execute query and load data into a pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Ensure neighbor_ids is processed as a Python set
    df['neighbor_ids'] = df['neighbor_ids'].apply(lambda x: set(x) if x else set())

    # Separate data based on crawl_id
    separated_dfs = {crawl_id: df[df['crawl_id'] == crawl_id].copy() for crawl_id in df['crawl_id'].unique()}

    # Add the reverse neighbor set for each crawl_id
    for crawl_id, crawl_df in separated_dfs.items():
        reverse_neighbors = []
        for _, row in crawl_df.iterrows():
            peer_id = row['peer_id']
            reverse_neighbors_set = set(
                crawl_df[crawl_df['neighbor_ids'].apply(lambda neighbors: peer_id in neighbors)]['peer_id']
            )
            reverse_neighbors.append(reverse_neighbors_set)
        crawl_df['reverse_neighbors'] = reverse_neighbors

    # Replace neighbor_ids with the union of neighbor_ids and reverse_neighbors
    for crawl_id, crawl_df in separated_dfs.items():
        crawl_df['combined_neighbors'] = crawl_df.apply(
            lambda row: row['neighbor_ids'].union(row['reverse_neighbors']),
            axis=1
        )
        crawl_df.drop(columns=['neighbor_ids', 'reverse_neighbors'], inplace=True)

    # Combine all crawl-specific dataframes back into one
    df_combined = pd.concat(separated_dfs.values())

    # Calculate the degree (size of the combined_neighbors set) for each peer_id
    df_combined['degree'] = df_combined['combined_neighbors'].apply(len)

    # Compute the frequency of each degree for each crawl_id
    degree_distribution = (
        df_combined.groupby(['crawl_id', 'degree'])
        .size()
        .reset_index(name='frequency')
    )

    # Bin degrees into ranges of 100
    degree_distribution['degree_bin'] = (degree_distribution['degree'] // 20) * 20

    # Calculate average frequency for each bin across all crawl_ids
    binned_data = (
        degree_distribution.groupby('degree_bin')['frequency']
        .mean()
        .reset_index(name='average_frequency')
    )

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(binned_data['degree_bin'], binned_data['average_frequency'], width=18,  # Width covers the entire bin range
    align='edge',  # Align bars to the edge of the bin
    color='blue', alpha=0.7
)

    # Customize the plot
    plt.title(f"Average Frequency per Degree Bin ({database})", fontsize=16)
    plt.xlabel("Degree Bin (Number of Combined Neighbors)", fontsize=12)
    plt.ylabel("Average Frequency", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save and display the plot
    plot_filename = f"bins_degree_distribution_{database}.png"
    plt.tight_layout()
    plt.savefig(plot_filename)
    
  print(f"Bar chart saved as {plot_filename}")
    plt.show()

except Exception as e:
    print(f"Error processing database {database}: {e}")

finally:
    # Close the connection
    if 'conn' in locals() and conn:
        conn.close()
