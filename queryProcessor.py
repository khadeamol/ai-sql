import duckdb
import dask.dataframe as dd
import ollama
import re
s3_path = "s3://app1data/geoguessr-user-data-12-12-2024.csv"


# Read the file into a Dask DataFrame
class queryProcessor():
    def __init__(self):
        self.model_name = "llama3.2:1b"
        return None

    def cleanQuery(self, query):

        clean_query = re.sub(r"```sql\s*|\s*```", '', query).strip()
        return clean_query
        # message = query + ". Extract the SQL query from this. No other text at all."
        # response = ollama.chat(model=self.model_name, messages=[{"role":"user", "content":message}],         options={
        #     "num_predict": 1000,   # Limits max tokens in response (default is too high)
        #     "temperature": 0.2,   # Lower = more deterministic, slightly faster
        #     "top_k": 40,          # Restrict next token choices
        #     "top_p": 0.9          # Reduce probability range
        # })
        # # print("Cleaned Query is:", response["message"]["content"])
        # return response["message"]["content"]

        
    def runSql(self, query):
        print("Trying to run")
        df = dd.read_csv(s3_path, storage_options={"anon": False}, dtype={'suspendedUntil': 'object'})

        df_pandas = df.compute()

        # Perform SQL-like query using Dask query
        duckdb.register("df", df_pandas)

        # Compute the result (only when needed)

        result = duckdb.sql(query).df()
        print("Query successful")
        return result