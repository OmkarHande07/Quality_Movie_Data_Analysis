import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsgluedq.transforms import EvaluateDataQuality
import concurrent.futures
import re

class GroupFilter:
      def __init__(self, name, filters):
        self.name = name
        self.filters = filters

def apply_group_filter(source_DyF, group):
    return(Filter.apply(frame = source_DyF, f = group.filters))

def threadedRoute(glue_ctx, source_DyF, group_filters) -> DynamicFrameCollection:
    dynamic_frames = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_filter = {executor.submit(apply_group_filter, source_DyF, gf): gf for gf in group_filters}
        for future in concurrent.futures.as_completed(future_to_filter):
            gf = future_to_filter[future]
            if future.exception() is not None:
                print('%r generated an exception: %s' % (gf, future.exception()))
            else:
                dynamic_frames[gf.name] = future.result()
    return DynamicFrameCollection(dynamic_frames, glue_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node s3_data_source
s3_data_source_node1724679976411 = glueContext.create_dynamic_frame.from_catalog(database="movie-catalog", table_name="imdb_movies_rating_csv", transformation_ctx="s3_data_source_node1724679976411")

# Script generated for node data_quality_checks
data_quality_checks_node1724680171257_ruleset = """

    Rules = [
    IsComplete "imdb_rating",
    ColumnValues "imdb_rating"between 8.5 and 10.3
        
    ]
"""

data_quality_checks_node1724680171257 = EvaluateDataQuality().process_rows(frame=s3_data_source_node1724679976411, ruleset=data_quality_checks_node1724680171257_ruleset, publishing_options={"dataQualityEvaluationContext": "data_quality_checks_node1724680171257", "enableDataQualityCloudWatchMetrics": True, "enableDataQualityResultsPublishing": True}, additional_options={"observations.scope":"ALL","performanceTuning.caching":"CACHE_NOTHING"})

# Script generated for node rowLevelOutcomes
rowLevelOutcomes_node1724695742214 = SelectFromCollection.apply(dfc=data_quality_checks_node1724680171257, key="rowLevelOutcomes", transformation_ctx="rowLevelOutcomes_node1724695742214")

# Script generated for node ruleOutcomes
ruleOutcomes_node1724695669963 = SelectFromCollection.apply(dfc=data_quality_checks_node1724680171257, key="ruleOutcomes", transformation_ctx="ruleOutcomes_node1724695669963")

# Script generated for node Conditional Router
ConditionalRouter_node1724696195765 = threadedRoute(glueContext,
  source_DyF = rowLevelOutcomes_node1724695742214,
  group_filters = [GroupFilter(name = "failed_records", filters = lambda row: (bool(re.match("failed", row["DataQualityEvaluationResult"])))), GroupFilter(name = "default_group", filters = lambda row: (not(bool(re.match("failed", row["DataQualityEvaluationResult"])))))])

# Script generated for node default_group
default_group_node1724696196245 = SelectFromCollection.apply(dfc=ConditionalRouter_node1724696195765, key="default_group", transformation_ctx="default_group_node1724696196245")

# Script generated for node failed_records
failed_records_node1724696196322 = SelectFromCollection.apply(dfc=ConditionalRouter_node1724696195765, key="failed_records", transformation_ctx="failed_records_node1724696196322")

# Script generated for node drop_column
drop_column_node1724696707489 = ApplyMapping.apply(frame=default_group_node1724696196245, mappings=[("overview", "string", "overview", "string"), ("gross", "string", "gross", "string"), ("director", "string", "director", "string"), ("certificate", "string", "certificate", "string"), ("star4", "string", "star4", "string"), ("runtime", "string", "runtime", "string"), ("star2", "string", "star2", "string"), ("star3", "string", "star3", "string"), ("no_of_votes", "long", "no_of_votes", "int"), ("series_title", "string", "series_title", "string"), ("meta_score", "long", "meta_score", "int"), ("star1", "string", "star1", "string"), ("genre", "string", "genre", "string"), ("released_year", "string", "released_year", "string"), ("poster_link", "string", "poster_link", "string"), ("imdb_rating", "double", "imdb_rating", "decimal")], transformation_ctx="drop_column_node1724696707489")

# Script generated for node Amazon S3
AmazonS3_node1724695962604 = glueContext.write_dynamic_frame.from_options(frame=ruleOutcomes_node1724695669963, connection_type="s3", format="json", connection_options={"path": "s3://project1-movie-data-analysis/rule_outcome/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1724695962604")

# Script generated for node Amazon S3
AmazonS3_node1724696505578 = glueContext.write_dynamic_frame.from_options(frame=failed_records_node1724696196322, connection_type="s3", format="json", connection_options={"path": "s3://project1-movie-data-analysis/bad-records/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1724696505578")

# Script generated for node redshift_load
redshift_load_node1724697062212 = glueContext.write_dynamic_frame.from_catalog(frame=drop_column_node1724696707489, database="movie-catalog", table_name="dev_movies_imdb_movies_rating", redshift_tmp_dir="s3://temp-project1",additional_options={"aws_iam_role": "arn:aws:iam::677276112463:role/redshift-role"}, transformation_ctx="redshift_load_node1724697062212")

job.commit()