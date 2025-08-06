# ETL Data Pipeline Project - AWS + Python

##  Overview

This project demonstrates a fully automated ETL (Extract, Transform, Load) pipeline that ingests large CSV datasets (50M+ rows) from a local FTP server, cleans and transforms the data using AWS Lambda, and stores the cleaned data back into S3 in Parquet format.

---

##  Features

*  Local **FTP server setup** with multiple CSV datasets
*  **Chunked uploading** of large CSV files (1M+ rows per chunk) to Amazon S3
*  **S3 Triggered Lambda** function for real-time processing
*  Data cleaning using **pandas** (e.g., handling missing values, dropping rows, type casting)
*  Final data stored in **Parquet format** in a separate S3 folder
*  Error handling for common issues (AccessDenied, OutOfMemory, ModuleNotFound, etc.)

---

##  Tech Stack

* **Language:** Python 3.10+
* **AWS Services:**

  * S3 (Storage)
  * Lambda (Serverless Computing)
  * IAM (Permissions)
* **Python Libraries:** boto3, pandas, ftplib, io
* **Tools:** pyftpdlib (for local FTP server)

---

##  Project Structure

```
My_ETl_data-Pipeline_Project/
├── ftp/                    # Contains FTP server setup & raw CSVs
├── config/                # JSON config file for credentials & paths
├── scripts/
│   └── upload_to_s3.py    # Uploads chunked CSV files to S3 from FTP
├── lambda_function/
│   ├── lambda_handler.py  # Entry point for AWS Lambda
│   └── utils/
│       └── clean_transform.py  # Logic to clean/transform data
└── temp_chunks/           # Temporary local chunk files (auto-deleted)
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

##  Common Errors Handled

*  `AccessDenied` (resolved via IAM permission updates)
*  `Runtime.ImportModuleError` (fixed by zipping correct folder structure)
*  `OutOfMemory` (resolved by increasing Lambda memory size)

---

##  Output

* Cleaned `.parquet` files in S3: `s3://<bucket-name>/cleaned/`
* Real-time processing logs in AWS CloudWatch

---

##  Author

Tara Chand Gurjar
