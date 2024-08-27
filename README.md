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

2. Create a database in AWS Glue, then create Crawler pointing to S3 bucket which is created and attach the input csv file.

![image](https://github.com/user-attachments/assets/0106b320-4dce-4fc9-b655-2eee957fab74)

Then run the crawler it will create meta data table under the database.

![image](https://github.com/user-attachments/assets/22b95035-2b64-4862-ab26-b60d93abb276)

3. Open the meta data table created in tables sections.you will find data quality section,now click on recommend rules and scan the data, some rules will be suggested.We have to update it as per our need. here we need to add following rules:

 ![image](https://github.com/user-attachments/assets/6e0a6af6-1ba8-460e-9b89-6c2a7a6c0571)

 4. Now run the data-quality-check and the output will be uploaded to the historical_data_rule_outcome folder under the S3 bucket.
 5. Create a redshift cluster for destination table,start the cluster, now open the Query editor.
    Here we need to connect to the cluster created
    create a schema and table for destination table as follows:

    ![image](https://github.com/user-attachments/assets/219eb9bf-6086-4dd8-88b9-a7d2b22a87c7)

    Now create a connection in Glue for JDBC,then create a VPC Endpoint for S3 bucket
    Then create Glue Crawler for redshift table,after running the crawler meta table will be created. 




