import psycopg2
import pandas as pd

# Database connection details
host = "cmi-read.cla0ai5jnqlv.us-east-1.rds.amazonaws.com"
port = "5432"
user = "jahnen_goettingen"
password = "WAvuMJzVk8vfVVofUq4-"

databases = ["nebula_polkadot", "nebula_avail_mainnet", "nebula_filecoin", "nebula_ipfs"]

# Output list for storing results
results = []

for database in databases:
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
        print('Executing query...')
        df = pd.read_sql_query(query, conn)
        print('Query executed.')

        # Ensure neighbor_ids is processed as a Python set
        df['neighbor_ids'] = df['neighbor_ids'].apply(lambda x: set(x) if x else set())

        # Separate data based on crawl_id
        separated_dfs = {crawl_id: df[df['crawl_id'] == crawl_id].copy() for crawl_id in df['crawl_id'].unique()}

        # Add reverse neighbors for each crawl_id
        for crawl_id, crawl_df in separated_dfs.items():
            reverse_neighbors = []
            for _, row in crawl_df.iterrows():
                peer_id = row['peer_id']
                reverse_neighbors_set = set(
                    crawl_df[crawl_df['neighbor_ids'].apply(lambda neighbors: peer_id in neighbors)]['peer_id']
                )
                reverse_neighbors.append(reverse_neighbors_set)
            crawl_df['reverse_neighbors'] = reverse_neighbors

        print('Added reverse neighbors.')

        # Compute indegree, outdegree, and combined degree centrality for each crawl
        crawl_indegree_centralizations = []
        crawl_outdegree_centralizations = []
        crawl_combined_centralizations = []

        for crawl_id, crawl_df in separated_dfs.items():
            # Initialize dictionaries to store centralities
            outdegree_centrality = {}
            indegree_centrality = {}
            combined_degree_centrality = {}

            # Compute outdegree centrality
            for _, row in crawl_df.iterrows():
                peer_id = row['peer_id']
                outdegree_centrality[peer_id] = len(row['neighbor_ids'])

            # Compute indegree centrality
            for _, row in crawl_df.iterrows():
                peer_id = row['peer_id']
                indegree_centrality[peer_id] = len(row['reverse_neighbors'])

            # Compute combined degree centrality
            crawl_df['combined_neighbors'] = crawl_df.apply(
                lambda row: row['neighbor_ids'].union(row['reverse_neighbors']),
                axis=1
            )
            for _, row in crawl_df.iterrows():
                peer_id = row['peer_id']
                combined_degree_centrality[peer_id] = len(row['combined_neighbors'])

            # Calculate max degrees for centralization
            max_outdegree = max(outdegree_centrality.values())
            max_indegree = max(indegree_centrality.values())
            max_combined_degree = max(combined_degree_centrality.values())

            # Compute centralization for outdegree, indegree, and combined degree
            outdegree_centralization = sum(
                max_outdegree - outdegree_centrality[peer] for peer in outdegree_centrality
            ) / ((len(outdegree_centrality) - 1) * (max_outdegree - 1) if len(outdegree_centrality) > 1 and max_outdegree > 1 else 1)

            indegree_centralization = sum(
                max_indegree - indegree_centrality[peer] for peer in indegree_centrality
            ) / ((len(indegree_centrality) - 1) * (max_indegree - 1) if len(indegree_centrality) > 1 and max_indegree > 1 else 1)

            combined_centralization = sum(
                max_combined_degree - combined_degree_centrality[peer] for peer in combined_degree_centrality
            ) / ((len(combined_degree_centrality) - 1) * (max_combined_degree - 1) if len(combined_degree_centrality) > 1 and max_combined_degree > 1 else 1)

            crawl_outdegree_centralizations.append(outdegree_centralization)
            crawl_indegree_centralizations.append(indegree_centralization)
            crawl_combined_centralizations.append(combined_centralization)

        # Compute average centralization across crawls
        avg_outdegree_centralization = sum(crawl_outdegree_centralizations) / len(crawl_outdegree_centralizations)
        avg_indegree_centralization = sum(crawl_indegree_centralizations) / len(crawl_indegree_centralizations)
        avg_combined_centralization = sum(crawl_combined_centralizations) / len(crawl_combined_centralizations)

        print(f"Database: {database}, Average Outdegree Centralization: {avg_outdegree_centralization}, "
              f"Average Indegree Centralization: {avg_indegree_centralization}, "
              f"Average Combined Degree Centralization: {avg_combined_centralization}")

        # Append results
        results.append({
            "database": database,
            "average_outdegree_centralization": avg_outdegree_centralization,
            "average_indegree_centralization": avg_indegree_centralization,
            "average_combined_centralization": avg_combined_centralization
        })

    except Exception as e:
        print(f"Error processing database {database}: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

# Save results to CSV
results_df = pd.DataFrame(results)
results_df.to_csv("../images/centralization_results.csv", index=False)

print("Results saved to centralization_results.csv")
