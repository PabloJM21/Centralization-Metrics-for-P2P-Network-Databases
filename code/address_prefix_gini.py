import psycopg2
import pandas as pd
import numpy as np
import ipaddress  # To handle IP address parsing

# Database connection details
host = "cmi-read.cla0ai5jnqlv.us-east-1.rds.amazonaws.com"
port = "5432"
user = "jahnen_goettingen"
password = "WAvuMJzVk8vfVVofUq4-"

databases = ["nebula_ipfs", "nebula_filecoin", "nebula_polkadot", "nebula_avail_mainnet"]

# Function to calculate Gini coefficient
def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    array = array.flatten()
    if np.amin(array) < 0:
        array -= np.amin(array)
    array = array + 0.0000001  # Avoid division by zero
    array = np.sort(array)
    n = array.shape[0]
    index = np.arange(1, n + 1)
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

# Function to extract prefixes from an IP address
def extract_prefix(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.version == 4:
            return str(ip_obj).rsplit('.', 1)[0]
        elif ip_obj.version == 6:
            return ':'.join(str(ip_obj).split(':')[:3])
    except ValueError:
        return None

# Initialize results list
results = []

# Iterate through the databases
for database in databases:
    try:
        print(f"Processing database: {database}")

        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        # Get the first 5 crawl_ids
        crawl_id_query = "SELECT DISTINCT crawl_id FROM neighbors ORDER BY crawl_id LIMIT 5"
        crawl_id_df = pd.read_sql_query(crawl_id_query, conn)
        if crawl_id_df.empty:
            print(f"No crawl_ids found in database: {database}")
            continue
        crawl_ids = crawl_id_df['crawl_id'].tolist()

        # Initialize accumulators for averages
        total_gini = 0
        total_nodes = 0
        crawl_count = 0

        for crawl_id in crawl_ids:
            # Query to fetch the addresses and calculate combined neighbors
            query = f"""
            SELECT ma.addr
            FROM multi_addresses ma
            JOIN peers_x_multi_addresses pxma ON ma.id = pxma.multi_address_id
            JOIN neighbors n ON pxma.peer_id = n.peer_id
            WHERE n.crawl_id = {crawl_id}
            """

            # Execute the query and load the result into a DataFrame
            addr_df = pd.read_sql_query(query, conn)

            if addr_df.empty:
                print(f"No data returned for database: {database}, crawl_id: {crawl_id}")
                continue

            # Extract prefixes from the addresses
            addr_df['prefix'] = addr_df['addr'].apply(extract_prefix)

            # Count the frequency of each prefix
            prefix_counts = addr_df['prefix'].value_counts()

            if prefix_counts.empty:
                print(f"No valid prefixes found for database: {database}, crawl_id: {crawl_id}")
                continue

            # Calculate the Gini coefficient for the prefix frequencies
            gini_coefficient = gini(prefix_counts.values)

            # Print the crawl_id, Gini coefficient, and number of nodes
            num_nodes = prefix_counts.values.sum()
            print(f"Crawl ID: {crawl_id}, Gini Coefficient: {gini_coefficient}, Number of Nodes: {num_nodes}")

            # Update totals
            total_gini += gini_coefficient
            total_nodes += num_nodes
            crawl_count += 1

        # Calculate averages
        if crawl_count > 0:
            avg_gini = total_gini / crawl_count
            avg_nodes = total_nodes / crawl_count
        else:
            avg_gini = None
            avg_nodes = None

        # Store the results
        results.append({
            'database': database,
            'avg_gini_coefficient': avg_gini,
            'avg_number_of_nodes': avg_nodes
        })
        print(f"Averages for {database}: Gini Coefficient = {avg_gini}, Nodes = {avg_nodes}")

    except Exception as e:
        print(f"Error processing database {database}: {e}")
        results.append({'database': database, 'avg_gini_coefficient': None, 'avg_number_of_nodes': None})

    finally:
        # Close the connection
        if conn:
            conn.close()

# Save the results to a CSV file
results_df = pd.DataFrame(results)
output_filename = "average_gini_coefficient_results.csv"
results_df.to_csv(output_filename, index=False)
print(f"Results saved to {output_filename}")
