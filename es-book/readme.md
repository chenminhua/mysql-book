### 版本

基于 7.x

### node

一个主节点 ,它将临时管理集群级别的一些变更，例如新建或删除索引、增加或移除节点等。

主节点不参与文档级别的变更或搜索，这意味着在流量增长的时候，该主节点不会成为集群的瓶颈。

用户能够与集群中的任何节点通信，包括主节点。

每一个节点都知道文档存在于哪个节点上，它们可以转发请求到相应的节点上。

### es 可以中途改 shard 数吗？

number_of_shards
每个索引的主分片数，默认值是 5 。这个配置在索引创建后不能修改。

### es 可以中途改 replicas 数吗？

每个主分片的副本数，默认值是 1 。对于活动的索引库，这个配置可以随时修改。

### 如何备份和恢复 es 中的数据？

### es 写入的效率怎么样？

### 算法

倒排索引

TF-IDF: term frequency - inverse document frequency 词在这篇文档中出现次数越高则分数越高；词越不常见则其权重越高。

### 导入测试数据(110468 个文档)

```
wget https://raw.githubusercontent.com/zq2599/blog_demos/master/files/create_shakespeare_index.sh \
&& chmod a+x create_shakespeare_index.sh \
&& ./create_shakespeare_index.sh 172.168.7.1 9200
```

### 调优

### scale out
