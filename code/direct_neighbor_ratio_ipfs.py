import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Database connection details
# Database connection details
host = "cmi-read.cla0ai5jnqlv.us-east-1.rds.amazonaws.com"
port = "5432"
user = "jahnen_goettingen"
password = "WAvuMJzVk8vfVVofUq4-"


database = "nebula_ipfs"  # Query only the IPFS database

# Specify the crawl ID of interest

specific_crawl_id = 19604

try:
    print(f"Processing database: {database} for crawl ID: {specific_crawl_id}")

    # Connect to the database using psycopg2
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    # Query to fetch data for the specific crawl ID
    query = f"""
    SELECT crawl_id, peer_id, neighbor_ids
    FROM neighbors
    WHERE crawl_id = {specific_crawl_id}
    """

    # Execute query and load data into a pandas DataFrame
    df = pd.read_sql_query(query, conn)
    print("Initial DataFrame:")
    print(df)

    # Ensure neighbor_ids is processed as a Python set
    df['neighbor_ids'] = df['neighbor_ids'].apply(lambda x: set(x) if x else set())



    reverse_neighbors = []
    for _, row in df.iterrows():
        peer_id = row['peer_id']
        reverse_neighbors_set = set(
            df[df['neighbor_ids'].apply(lambda neighbors: peer_id in neighbors)]['peer_id']
        )
        reverse_neighbors.append(reverse_neighbors_set)
    df['reverse_neighbors'] = reverse_neighbors

    df['combined_neighbors'] = df.apply(
        lambda row: row['neighbor_ids'].union(row['reverse_neighbors']),
        axis=1
    )

    # Calculate the degree (size of the combined_neighbors set) for each peer_id
    df['degree'] = df['combined_neighbors'].apply(len)

    # Add reverse_ratio column to df
    df['neighbor_ratio'] = df['neighbor_ids'].apply(len) / df['degree']

    # Calculate the average reverse_ratio for each degree in the degree_distribution table
    degree_distribution = (
        df.groupby(['crawl_id', 'degree'])
            .agg(
            frequency=('peer_id', 'size'),  # Count the number of nodes with this degree
            avg_reverse_ratio=('neighbor_ratio', 'mean')  # Calculate average reverse_ratio
        )
            .reset_index()
    )


    # Plot degree vs reverse ratio
    plt.figure(figsize=(12, 6))
    plt.plot(degree_distribution['degree'], degree_distribution['avg_reverse_ratio'],
             marker='o', color='orange', label=f"Reverse Ratio for Crawl {specific_crawl_id}")

    # Customize the plot
    plt.title(f"Direct Neighbor Ratio Distribution for Crawl {specific_crawl_id}", fontsize=16)
    plt.xlabel("Degree (Number of Neighbors)", fontsize=12)
    plt.ylabel("Average Direct Neighbor Ratio", fontsize=12)
    plt.grid(True)

    # Save and display the plot
    plot_filename_ratio = f"direct_neighbor_ratio_{database}_{specific_crawl_id}.png"
    plt.tight_layout()
    plt.savefig(plot_filename_ratio)
    print(f"../images/Direct Neighbor Ratio chart saved as {plot_filename_ratio}")
    plt.show()

except Exception as e:
    print(f"Error processing database {database}: {e}")

finally:
    # Close the connection
    if 'conn' in locals() and conn:
        conn.close()
