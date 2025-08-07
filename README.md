# ETL Data Pipeline Project - AWS + Python

##  Overview

Designed and implemented a scalable end-to-end ETL data pipeline to process and analyze large datasets (50M+ rows) from an on-premise FTP server to AWS S3, leveraging AWS native services for automation, transformation, and analytics.
---

##Key Features & Responsibilities:

*Data Source Automation:
Set up FTP-based data ingestion from local server using Python and boto3.
Uploaded raw CSVs (users, orders, products – multi-million rows) in chunks to Amazon S3 (raw/ folder) without manual intervention.

*ETL Orchestration (Lambda + Pandas):
Configured AWS Lambda to trigger automatically on new file uploads in the raw/ S3 prefix.
Performed data cleaning, formatting, and transformation (e.g., timestamp correction, null handling, standardization) using Python (pandas, pyarrow).
Converted cleaned data to efficient Parquet format, stored in cleaned/ S3 folder.

*Data Merging & Organization:
Grouped and merged chunked parquet files per entity (users, orders, products) using Python scripts.
Stored final merged outputs to final_cleaned/ folder for downstream analytics.

*Metadata Management & Querying:
Used AWS Glue Crawler to automatically detect schema and create Athena tables.
Ensured proper partitioning, schema consistency, and SERDE settings.
Resolved issues like empty Athena query results due to incorrect folder structure and data format.

* Common Errors Handled
   `AccessDenied` (resolved via IAM permission updates)
   `Runtime.ImportModuleError` (fixed by zipping correct folder structure)
   `OutOfMemory` (resolved by increasing Lambda memory size)
  
* Business-Level SQL Analytics via Athena:
   Delivered SQL-based analytics such as:
	Top users by order value
	Most in-demand products
	Delivery time KPIs and cancellation trends
	
 Created Athena Views with cleaned timestamp columns using SQL functions like from_unixtime and timezone conversion (AT TIME ZONE 'Asia/Kolkata').
---

##  Tech Stack

* **Language:** Python 3.10+
* **AWS Services:**

  * S3 (Storage)
  * Lambda (Serverless Computing)
  * IAM (Permissions)
* **Python Libraries:** boto3, pandas, ftplib, io , PyArrow, Parquet
* **Tools:** pyftpdlib (for local FTP server)
* AWS Glue, AWS Athena 
*FTP/SFTP
*SQL
---

##  Project Structure

```
My_ETl_data-Pipeline_Project/
├── ftp/                    					# Contains FTP server setup & raw CSVs
├── config/                					# JSON config file for credentials & paths
├── lambda_function/
│   ├── lambda_handler.py  		# Entry point for AWS Lambda
│   └── utils/
│       └── clean_transform.py	  # Logic to clean/transform data
├── merged/
│   └── merged_data.py   			 # merged chunked files to S3 from S3
├── scripts/
   └── upload_to_s3.py   			 # Uploads chunked CSV files to S3 from FTP
```

---

##  How It Works

### 1. Start FTP Server

```bash
python ftp/ftp_server.py
```

### 2. Upload CSV Files to S3

```bash
python scripts/upload_to_s3.py
```

> Uploads large CSV files in chunks (as defined in config) from local FTP to S3 (`raw/` folder).

### 3. S3 Triggers Lambda

Each time a new file lands in the `raw/` folder, a Lambda function is triggered:

* Reads the CSV chunk
* Applies transformations
* Saves the cleaned output to `cleaned/` folder in **Parquet** format

---

## Example Transformation (clean\_transform.py)

```python
def clean_and_transform(df):
    df.dropna(subset=["id", "email"], inplace=True)
    df['email'] = df['email'].str.lower()
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    return df
```

---

##  Output

* Cleaned `.parquet` files in S3: `s3://<bucket-name>/final_cleaned/`
* Real-time processing logs in AWS CloudWatch

---

##  Author

Tara Chand Gurjar
