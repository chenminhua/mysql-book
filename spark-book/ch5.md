# 数据读取与保存
spark支持很多种输入输出源。一部分原因是spark本身是基于hadoop生态圈构建的，特别是spark可以通过hadoop mapReduce所使用的InputFormat和OutputFormat接口访问数据，而大部分文件格式和存储系统都支持这种接口。

# 本地文件系统或者分布式文件系统

```python
sc.textFile('...')
import json
data = input.map(labmda x: json.loads(x))
```

# spark SQL中的结构化数据
### Apache Hive
是hadoop上的一种常见的结构化数据源，hive可以在HDFS内或者其他存储系统上存储多种格式的表。这些格式从普通文本到列式存储格式都有。spark SQL可以读取Hive支持的任何表。

### JSON

# 数据库与键值存储

### 数据库
spark可以从任何支持jdbc的关系型数据库中读取数据，包括mysql, postgre等等

### cassandra
目前只能在java和scala中使用。

### HBase
spark可以通过hadoop访问hbase

### elasticsearch
使用Elasticsearch-hadoop从elasticsearch中读取数据


