import pandas as pd
from datetime import datetime
import json
import boto3
import io
import os
from utils.clean_transform import clean_and_transform

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Get bucket and key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = event['Records'][0]['s3']['object']['key']

    print(f"Triggered by: s3://{bucket}/{raw_key}")

    # 2. Download raw CSV file
    raw_obj = s3.get_object(Bucket=bucket, Key=raw_key)
    df = pd.read_csv(raw_obj['Body'])

    # 3. Clean and transform
    df_cleaned = clean_and_transform(df)

    # 4. Convert to Parquet
    out_buffer = io.BytesIO()
    df_cleaned.to_parquet(out_buffer, index=False, engine='pyarrow', timestamp_unit='ms')

    # 5. Upload to cleaned/ folder
    file_name = os.path.basename(raw_key).replace(".csv", ".parquet")
    clean_key = f"cleaned/{file_name}"

    s3.put_object(Bucket=bucket, Key=clean_key, Body=out_buffer.getvalue())

    print(f"Cleaned file uploaded to s3://{bucket}/{clean_key}")

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed successfully!')
    }
