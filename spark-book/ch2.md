# quick start
[下载](http://spark.apache.org/downloads.html)

解压并进入目录

```
bin/pyspark
```

进入了python shell，可以查看SparkContext的一些帮助

```python
help(sc)
dir(sc)
```

在python shell中创建一个RDD来作一个简单的即时统计

```
lines = sc.textFile("README.md") #创建一个RDD
print type(lines)   #<class 'pyspark.rdd.RDD'>
dir(lines)    #查看RDD的api
lines.count()  #104  返回行数
lines.first()  #u'# Apache Spark'   返回第一行内容

pythonLines = lines.filter(lambda line: 'Python' in line)  #<class 'pyspark.rdd.PipelinedRDD'>
pythonLines.count()  #3
pythonLines.first()  #u'high-level APIs in Scala, Java, Python, and R, and an optimized engine that'
```

# 核心概念
从上层看，每个spark都由一个**驱动器程序**来发起集群上的各种并行操作

驱动器程序通过SparkContext对象来访问Spark,这个对象代表对计算集群的一个连接（上面的sc）。

我们调用sc.textFile来创建了一个RDD,并在其上执行各种操作

要执行这些操作，驱动器程序要管理多个（或一个）执行器节点。比如上面的count操作就可以交个多个节点，分别统计不同部分的行数。

# 独立应用
在python中，可以把应用写成python脚本，但是需要bin/spark-submit来运行。

```python
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('my app')
sc = SparkContext(conf = conf)

lines = sc.textFile("README.md") #创建一个RDD
print lines.count()  #104  返回行数
print lines.first()  #u'# Apache Spark'   返回第一行内容

pythonLines = lines.filter(lambda line: 'Python' in line)  #<class 'pyspark.rdd.PipelinedRDD'>
print pythonLines.count()  #3
print pythonLines.first()  #u'high-level APIs in Scala, Java, Python, and R, and an optimized engine that'
```
