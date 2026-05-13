from google.cloud import bigquery
from google.oauth2 import service_account

KEY_PATH = "../credentials.json"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id
)

def fetch_filtered_data(sql_conditions):

    query = f"""
    SELECT *
    FROM `acn-datafabricpoc.Interns_Test_Dataset.AG_network_kpi_output`
    WHERE {sql_conditions}
    """

    print("\nGenerated Query:\n")
    print(query)

    df = client.query(query).to_dataframe()

    return df