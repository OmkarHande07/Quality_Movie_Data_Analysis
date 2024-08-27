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

    Now create a connection in Glue for JDBC,then create a VPC Endpoint for S3 bucket.
    Then create Glue Crawler for redshift table,after running the crawler meta table will be created.

6. The interesting part is here Creating the AWS Glue Visual ETL script:
   i] Add the data source as AWS Glue Catalog,choose the Database and table.
   ii] Now add transform - Evaluate Data Quality, then enter rules for data_quality_check.Select original data and Data Quality result options
   iii] 2 transforms will be created. In ruleOutCome add target as S3 bucket with Format as JSON and attach S3 bucket's rule_outcome folder.
   iv] In rowLevelOutCome add conditional router,2 transforms will be created now choose AND operator with key as DataQualityEvaluationResult, operation as matches, value as Failed. Now the records which will fail the rule will go to the failed_records side and passed records will added to default

7. Add target to the failed_records so that the records will be uploaded to the bad_records in the S3 bucket.
8. Add change schema to default group, drop the unwanted columns and update the data types.
9. Add target to Glue Data Catalog to change schema which will connect to the destination table by choosing the database and the table.
10. Finally save the script and run it.

   ![image](https://github.com/user-attachments/assets/690a3833-9a54-434f-8b19-289061bd8144)

we can check the success by running select query in redshift editor 

![image](https://github.com/user-attachments/assets/851e44b9-9d3b-43ca-8f5e-01462a93fc51)

also check the S3 bucket the bad records will be added to the bad_record folder

![image](https://github.com/user-attachments/assets/7fc19f68-146f-416b-ae1a-9aa3b968ce6d)

11. Now create AWS EventBridge rule to capture the success of records after running the data_quality_check, integrate the SNS topic with email endpoint so that we can get notification to our email. 

![image](https://github.com/user-attachments/assets/bb915600-ba40-4188-873d-b0baeace4374)





