import boto3
import pandas as pd
import os
import json
from io import BytesIO
from ftplib import FTP

with open("config/sftp_config.json") as f:
    config = json.load(f)

FTP_HOST = config["host"]
FTP_PORT = config["port"]
FTP_USER = config["username"]
FTP_PASS = config["password"]
FTP_FOLDER = config["remote_path"]

S3_BUCKET = config["s3_bucket"]
S3_PREFIX = config["s3_prefix"]
CHUNK_SIZE = config["chunk_size"]
LOCAL_TEMP = "temp_chunks"

os.makedirs(LOCAL_TEMP, exist_ok=True)

def upload_file_to_s3(s3_client, file_path, s3_key):
    s3_client.upload_file(file_path, S3_BUCKET, s3_key)
    print(f"Uploaded to s3://{S3_BUCKET}/{s3_key}")

def download_and_upload_all_csvs():
    s3 = boto3.client("s3")

    # Connect to FTP
    ftp = FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.cwd(FTP_FOLDER)

    filenames = ftp.nlst()
    csv_files = [f for f in filenames if f.endswith(".csv")]
    print(f"Found {len(csv_files)} CSV files on FTP.")

    for file_name in csv_files:
        print(f"\n Processing: {file_name}")
        bio = BytesIO()
        ftp.retrbinary(f"RETR {file_name}", bio.write)
        bio.seek(0)

        # Chunk + Upload to S3
        chunk_num = 1
        for chunk in pd.read_csv(bio, chunksize=CHUNK_SIZE):
            temp_file = os.path.join(LOCAL_TEMP, f"{file_name}_part{chunk_num}.csv")
            chunk.to_csv(temp_file, index=False)

            s3_key = f"{S3_PREFIX}/{file_name}_part{chunk_num}.csv"
            upload_file_to_s3(s3, temp_file, s3_key)

            os.remove(temp_file)
            chunk_num += 1

    ftp.quit()
    print(" All files  uploaded.")

if __name__ == "__main__":
    download_and_upload_all_csvs()