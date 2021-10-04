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
import re
from pyspark import SparkConf



conf = SparkConf().setMaster("yarn")
sc = SparkContext(conf=conf)
spark = SparkSession(sc).builder.getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

#1. Clean the dataset

df = spark.read.format("csv").option("header", "true").option("multiline","true").load("yelp_review.csv")
df.printSchema()
df.show()
#df = df.withColumnRenamed("stars", "label")
df = df.withColumn("label", df["stars"].cast("double"))
#df = df.where(col("label").isNotNull())
df = df.dropna(subset=['label', 'text', 'funny', 'cool',"useful"])

df = df.select('text', 'useful')

df = df.filter(df.useful.isin(1))

df.show()

# Refering columns by index.
rdd2=df.rdd.map(lambda x:
    (x[1],x[0])
    )

#print(rdd2.collect())

readin_clean = rdd2.map(lambda x: (x[0], re.sub("\W+"," ", x[1]).strip().lower()))

#print(readin_clean.collect())

import nltk
from nltk.corpus import stopwords
stopword_list = set(stopwords.words("english"))
def ProcessText(text,stopword_list):
        tokens = nltk.word_tokenize(text)
        remove_punct = [word for word in tokens if word.isalpha()]
        remove_stop_words = [word for word in remove_punct if not word in stopword_list]
        return remove_stop_words



#words=lines.flatMap(lambda x:ProcessText(x,stopword_list))

results_rdd=readin_clean.mapValues(lambda x:ProcessText(x,stopword_list))

print(results_rdd.collect())

#result_rdd1=results_rdd.filter(lambda keyValue: keyValue[0]==1)

result_rdd2=results_rdd.reduceByKey(lambda x,y:x+y)

result_rdd3=result_rdd2.values()

result_rdd4=result_rdd3.flatMap(lambda x:x)

result_rdd44=result_rdd4.map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y)

result_rdd4.reduceByKey(lambda x,y:x+y)

result_rdd45=result_rdd44.map(lambda x:(x[1],x[0])).sortByKey(False).map(lambda x:(x[1]))

result_final=result_rdd45.collect()

print("useful",result_final[:10])




