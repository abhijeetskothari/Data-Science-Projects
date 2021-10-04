from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF 
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.sql.functions import col
from pyspark import SparkConf


conf = SparkConf().setMaster("yarn")
sc = SparkContext(conf=conf)
spark = SparkSession(sc).builder.getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

#1. Clean the dataset

df = spark.read.format("csv").option("header", "true").option("multiline","true").load("yelp_business.csv")
df.printSchema()
df.show()


# method 2 to read file

df1 = spark.read.format("csv").option("header", "true").option("multiline","true").load("yelp_business.csv")
df1.printSchema()
df1.show()


from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

#address|         business_id|          categories|                city|      is_open|     latitude|     longitude|                name|        neighborhood|postal_code|review_count|stars|state|


from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType, StringType
#df_business.printSchema()
schema = StructType([
StructField("business_id", StringType()),
StructField("name", StringType()),
StructField("neighborhood", StringType()),
StructField("address", StringType()),
StructField("city", StringType()),
StructField("state", StringType()),
StructField("postal_code", StringType()),
StructField("latitude", StringType()),
StructField("longitude", StringType()),
StructField("stars", StringType()),
StructField("review_count", StringType()),
StructField("is_open", DoubleType()),
StructField("categories", StringType())
])

schema = StructType([
StructField("address", StringType()),
StructField("business_id", StringType()),
StructField("categories", StringType()),
StructField("city", StringType()),
StructField("is_open", DoubleType()),
StructField("latitude", StringType()),
StructField("longitude", StringType()),
StructField("name", StringType()),
StructField("neighborhood", StringType()),
StructField("postal_code", StringType()),
StructField("review_count", StringType()),
StructField("stars", StringType()),
StructField("state", StringType())
])

df_business1 = (sqlContext
.read
.format("com.databricks.spark.csv")
.schema(schema)
.option("header", "true")
.option("multiline", "true")
.option("mode", "DROPMALFORMED")
.load("yelp_business.csv"))
df_business1.show()

from pyspark.sql import functions as F
df_business1.select("business_id", F.explode(F.split("categories", ";")).alias("category"), "stars").show(5)
businessdf=df_business1
businessdf.select(F.explode(F.split("categories", ";")).alias("category"), "stars").groupBy("category").agg(F.count("category").alias("businessCount"), F.avg("stars").alias("averageStarRating"), F.min("stars").alias("minStarRating"), F.max("stars").alias("maxStarRating")).show()
