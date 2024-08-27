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
 
