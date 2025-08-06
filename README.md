# My ETL Data Pipeline Project

This project automates the end-to-end ETL workflow:
- Reads raw data from client's SFTP server
- Uploads raw data to AWS S3
- AWS Lambda transforms and cleans the data
- Saves cleaned data back to S3 in Parquet format

## Folders:
- `scripts/`: SFTP download + S3 upload logic
- `lambda/`: S3 trigger logic and data transformation
- `config/`: Credentials and environment config files
 
