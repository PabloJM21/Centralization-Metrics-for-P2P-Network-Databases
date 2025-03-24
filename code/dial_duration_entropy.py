import psycopg2
import pandas as pd
import numpy as np

# Database connection details
host = "cmi-read.cla0ai5jnqlv.us-east-1.rds.amazonaws.com"
port = "5432"
user = "jahnen_goettingen"
password = "WAvuMJzVk8vfVVofUq4-"

# List of databases to connect to
databases = ["nebula_filecoin", "nebula_polkadot", "nebula_avail_mainnet", "nebula_ipfs"]

# Loop through each database and compute the entropy
results = []  # Store entropy results for each database
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

        # Query to compute the average crawl duration for each peer_id
        query = """
        SELECT
            v.peer_id,
            AVG(EXTRACT(EPOCH FROM v.dial_duration)) FILTER (WHERE v.dial_duration IS NOT NULL) AS avg_dial_duration
        FROM visits v
        WHERE v.dial_duration IS NOT NULL
        GROUP BY v.peer_id
        """

        # Execute the query and load the result into a DataFrame
        avg_dial_duration_df = pd.read_sql_query(query, conn)

        print(avg_dial_duration_df['avg_dial_duration'].head(10))

        # Normalize the crawl durations to create a probability distribution
        total_dial_duration = avg_dial_duration_df['avg_dial_duration'].sum()
        avg_dial_duration_df['probability'] = avg_dial_duration_df['avg_dial_duration'] / total_dial_duration

        # Calculate maximum entropy for a uniform distribution
        num_elements = len(avg_dial_duration_df)
        max_entropy = np.log(num_elements)  # Maximum entropy if all elements are equally likely

        # Calculate entropy
        avg_dial_duration_df['entropy_component'] = avg_dial_duration_df['probability'] * np.log(avg_dial_duration_df['probability'])
        entropy = -avg_dial_duration_df['entropy_component'].sum() / max_entropy

        # Store the result
        results.append({'database': database, 'dial_duration_entropy': entropy})
        print(f"Entropy of average dial durations for {database}: {entropy}")

    except Exception as e:
        print(f"Error processing database {database}: {e}")
        results.append({'database': database, 'dial_duration_entropy': None})

    finally:
        # Close the connection
        if 'conn' in locals() and conn:
            conn.close()

# Save the entropy results to a CSV file
results_df = pd.DataFrame(results)
output_filename = "avg_dial_duration_entropy_results.csv"
results_df.to_csv(output_filename, index=False)
print(f"Results saved to {output_filename}")
