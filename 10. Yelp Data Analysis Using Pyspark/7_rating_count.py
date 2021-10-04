from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF 
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.sql.functions import col
from pyspark.sql.functions import count
from pyspark import SparkConf


conf = SparkConf().setMaster("yarn")
sc = SparkContext(conf=conf)
spark = SparkSession(sc).builder.getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

#1. Clean the dataset
df = spark.read.format("csv").option("header", "true").option("multiline","true").load("yelp_review.csv")
result=df.groupBy('stars').agg(count('review_id').alias('count')).sort('stars')
list1=result.collect()
for l in list1:
    if l[0]=='1' or l[0]=='2' or l[0]=='3' or l[0]=='4' or l[0]=='5':
        print('for rating {}, the total count is {}'.format(l[0], l[1]))

