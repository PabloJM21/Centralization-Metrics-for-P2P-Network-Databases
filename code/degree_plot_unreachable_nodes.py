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

    # Identify all peer IDs in the dataset
    all_peer_ids = set(df['peer_id'])
    print("All Peer IDs:")
    print(all_peer_ids)

    # Find unreachable neighbors
    df['unreachable_neighbors'] = df['neighbor_ids'].apply(
        lambda neighbors: neighbors - all_peer_ids
    )
    print("Unreachable Neighbors Column:")
    print(df['unreachable_neighbors'])



    # Add the reverse neighbor set
    # Create a DataFrame from the combined set
    unreachable_df = pd.DataFrame({'unreachable_id': list(set().union(*df['unreachable_neighbors']))})
    print("Unreachable neighbors: ")
    print(unreachable_df['unreachable_id'])
    reverse_neighbors = []
    for _, row in unreachable_df.iterrows():
        peer_id = row['unreachable_id']
        # Find all crawl_ids where this peer_id appears in neighbor_ids
        reverse_neighbors_set = set(
            df[df['unreachable_neighbors'].apply(lambda neighbors: peer_id in neighbors)]['peer_id']
        )
        reverse_neighbors.append(reverse_neighbors_set)

    unreachable_df['reverse_neighbors'] = reverse_neighbors
    print('Reversed neighbors: ')
    print(unreachable_df['reverse_neighbors'])

    unreachable_df['reverse_degree'] = unreachable_df['reverse_neighbors'].apply(len)




    # Compute the frequency of each degree of unreachable neighbors
    degree_distribution = (
        unreachable_df.groupby('reverse_degree')
        .size()
        .reset_index(name='frequency')
    )

    sorted_frequency = degree_distribution.sort_values(by='reverse_degree', ascending=True)

    # Display the sorted frequency column
    print("degree column sorted in ascending order:")
    print(sorted_frequency[['reverse_degree']])



    # Plot the bar chart
    plt.figure(figsize=(12, 6))


    # Plot degree distribution
    plt.plot(degree_distribution['reverse_degree'], degree_distribution['frequency'],
             marker='o', label=f"Crawl {specific_crawl_id}")

    # Customize the plot
    plt.title(f"Unreachable Neighbors Distribution for Crawl {specific_crawl_id}", fontsize=16)
    plt.xlabel("Degree Bin (Number of Unreachable Neighbors)", fontsize=12)
    plt.ylabel("Average Frequency", fontsize=12)
    plt.grid(True)

    # Save and display the plot
    plot_filename = f"../images/unreachable_neighbors_{database}_{specific_crawl_id}.png"
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
