#coding:utf8
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('my app')
sc = SparkContext(conf = conf)

lines = sc.textFile("README.md") #创建一个RDD
print lines.count()  #104  返回行数
print lines.first()  #u'# Apache Spark'   返回第一行内容

pythonLines = lines.filter(lambda line: 'Python' in line)  #<class 'pyspark.rdd.PipelinedRDD'>
print pythonLines.count()  #3
print pythonLines.first()  #u'high-level APIs in Scala, Java, Python, and R, and an optimized engine that'
