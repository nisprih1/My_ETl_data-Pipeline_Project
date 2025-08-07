import boto3
import pandas as pd
from io import BytesIO
from collections import defaultdict
import os

# S3 config
bucket_name = 'my-etl-pipeline-5m'
input_prefix = 'cleaned/'
output_prefix = 'final_cleaned/'

s3 = boto3.client('s3')

# 1. Get all cleaned parquet files
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=input_prefix)
files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.parquet')]

#  Group files by table name
table_groups = defaultdict(list)
for file_key in files:
    base_name = os.path.basename(file_key)
    table_name = base_name.split('_part')[0].split('.')[0]  # gets data from parts. parquet"
    table_groups[table_name].append(file_key)

# 3. Merge each table's chunks
for table_name, file_keys in table_groups.items():
    print(f"\nMerging {len(file_keys)} files for table: {table_name}")
    dfs = []

    for key in sorted(file_keys):  # Sort to keep order
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        df = pd.read_parquet(BytesIO(obj['Body'].read()))
        dfs.append(df)

    # Combine
    merged_df = pd.concat(dfs, ignore_index=True)
    subfolder_path = f"{output_prefix}{table_name}_cleaned/"
    output_key = f"{subfolder_path}{table_name}_cleaned.parquet"

    out_buffer = BytesIO()
    merged_df.to_parquet(out_buffer, index=False)

    s3.put_object(Bucket=bucket_name, Key=output_key, Body=out_buffer.getvalue())
    print(f" Uploaded: s3://{bucket_name}/{output_key}")
