# Quality_Movie_Data_Analysis
Designed ETL Pipeline to find out quality movies based on IMDb rating using AWS services

# Tech Stack: 
# Source:
1. AWS S3 : Used as a Datalake to store the input or raw file.
2. AWS Glue Crawlers : Used for automated schema discovery and data classification.
3. AWS Glue Catalog : Used to provide a unified interface to store and query information about data formats, schemas, and sources.

 # Transform:
 1. AWS Glue Data Quality : Used to analyze the data, identify rules, and create a ruleset that can evaluate in a data quality task.
 2. AWS Glue Low Code ETL : Helped to visually design data transformation workflows.

 # Load:
 1. Aws Redshift : Used as data warehousing solution for efficient querying and analytics.

 # Alert:
 1. AWS EventBridge : Used to manage event-driven processing and workflows.
 2. AWS SNS : Used to sends notifications to endpoint regarding pipeline status and alerts.


# Complete Pipeline :

![image](https://github.com/user-attachments/assets/690a3833-9a54-434f-8b19-289061bd8144)

# Steps to design data pipeline :
1. Create a S3 bucket with following folders and upload the imdb_ratings.csv file to the input folder.

![image](https://github.com/user-attachments/assets/d9628e62-abab-4ed9-947a-afd10fabacdb)

2. Create a database in AWS Glue, then create Crawler pointing to S3 bucket which is created and attach the input csv file,then run the crawler it will create meta data table under the database.


