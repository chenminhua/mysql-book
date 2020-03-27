https://github.com/databricks/learning-spark
spark是一个用来实现快速而通用的集群计算的平台

spark使用mapReduce计算模型

spark可以运行在hadoop集群上，访问包括cassandra在内的任意hadoop数据源。

spark核心是一个对计算任务进行调度，分发和监控的计算引擎。

spark还支持为各种不同场景设计的高级组件，比如SQL和机器学习。

组件包括
    spark SQL, spark Streaming, MLlib, GraphX, Spark, Core, YARN, Mesos

### spark core
实现spark基本功能，包含任务调度，内存管理，错误恢复，与存储交互，RDD API

### spark sql
用来操作结构化的数据

### spark streaming
对实时数据进行流式计算，比如服务器日志，或者消息队列

### MLlib
提供机器学习的程序库

### GraphX
用来操作图的程序库，可以进行并行的图计算

### 集群管理器
独立调度器，YARN，Mesos等等
