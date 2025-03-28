import psycopg2
import pandas as pd
import numpy as np

# Database connection details
host = "cmi-read.cla0ai5jnqlv.us-east-1.rds.amazonaws.com"
port = "5432"
user = "jahnen_goettingen"
password = "WAvuMJzVk8vfVVofUq4-"

# List of databases to connect to
databases = ["nebula_ipfs", "nebula_filecoin", "nebula_polkadot", "nebula_avail_mainnet"]

# Function to calculate Gini coefficient
def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)
    # Values cannot be 0:
    array = array + 0.0000001
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

# Loop through each database and compute the Gini coefficient
results = []  # Store Gini coefficient results for each database
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

        # Query to count occurrences of each country
        query = """
        SELECT
            country,
            COUNT(*) AS frequency
        FROM multi_addresses
        GROUP BY country
        """

        # Execute the query and load the result into a DataFrame
        country_frequency_df = pd.read_sql_query(query, conn)

        # Calculate Gini coefficient for the country frequencies
        gini_coefficient = gini(country_frequency_df['frequency'].values)

        # Store the result
        results.append({'database': database, 'country_frequency_gini': gini_coefficient})
        print(f"Gini Coefficient of country frequencies for {database}: {gini_coefficient}")

    except Exception as e:
        print(f"Error processing database {database}: {e}")
        results.append({'database': database, 'country_frequency_gini': None})

    finally:
        # Close the connection
        if 'conn' in locals() and conn:
            conn.close()

# Save the Gini coefficient results to a CSV file
results_df = pd.DataFrame(results)
output_filename = "../images/country_frequency_gini_results.csv"
results_df.to_csv(output_filename, index=False)
print(f"Results saved to {output_filename}")
