from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF 
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.sql.functions import col

from pyspark import SparkContext
from pyspark import sql
from pyspark.sql import SQLContext
from pyspark.sql.functions import avg
from pyspark import SparkConf
import re


conf = SparkConf().setMaster("yarn")
sc = SparkContext(conf=conf)
spark = SparkSession(sc).builder.getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


#1. Clean the dataset

df = spark.read.csv( "yelp_review.csv", header=True)
df.printSchema()
df.show()
#df = df.withColumnRenamed("stars", "label")
df = df.withColumn("label", df["stars"].cast("double"))
#df = df.where(col("label").isNotNull())
df = df.dropna(subset=['label', 'text', 'funny', 'cool',"useful"])

df = df.select('text', 'label')

df = df.filter(df.label.isin(1.0,2.0,3.0,4.0,5.0))

df = df.limit(1000)
df.show()


#####################################
import pyspark.sql.functions as f
df = df.withColumn('wordCount', f.size(f.split(f.col('text'), ' ')))
df.show()


results = df.groupBy("label").agg(avg("wordCount"))

#####################################

#Create list of results
answer = sorted(results.collect())

#Print Output
for i in answer:
	print(str(i[0])+ " Star Rating: Average Length of Comments "+ str(i[1]))


#Create list of results
#answer = sorted(results.collect())

#Print Output
#for i in answer:
#	print(str(i[0])+ " Star Rating: Average Length of Comments "+ str(i[1]))

