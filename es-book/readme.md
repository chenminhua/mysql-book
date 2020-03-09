## 倒排索引

- 单词词典（Term Dictionary），记录所有文档的单词，记录单词到倒排列表的关联关系。
- 倒排列表（Posting List），倒排索引项由一下内容组成
  -- 文档 ID
  -- 词频 TF，单词在文档中出现的次数，用于相关性分析
  -- 位置，单词在文档中分词的位置。
  -- 偏移，记录单词的开始结束位置。

可以指定某些字段不做索引。优点是节省空间，缺点是该字段无法被搜索。

TF-IDF: term frequency - inverse document frequency 词在这篇文档中出现次数越高则分数越高；词越不常见则其权重越高。

倒排索引不可变性的好处：无锁带来高并发。能更好地利用内存做缓存。数据能更好地生成和维护，数据可以压缩。

## 集群

- 不同的集群通过不同名称来区分，默认名字“elasticsearch”。
- 集群可有一个或多个节点，每个节点有自己的名字。节点启动后有个 UID，保存在 data 目录下。
- 节点默认 master eligible，可参加 Master 竞选。第一个节点启动时会将自己选为 master。
- 每个节点都保存了集群的状态，但**只有 master 节点能修改集群状态，并将集群信息同步给其他节点**。
- 主节点不参与文档级别的变更或搜索，这意味着在流量增长的时候，该主节点不会成为集群的瓶颈。
- 用户能够与集群中的任何节点通信，包括主节点。
- 集群状态维护了节点的信息，所有索引相关的信息以及 mapping 和 setting 信息，分片的路由信息。
- 选主过程是 master eligible 节点互相 ping 对方，node ID 低的节点被选为 master 节点。
- 脑裂问题，由于网络问题导致出现双 master，解决方法是 quorem 机制。7.0 开始默认 quorem。
- Data node： 负责保存数据的节点。
- Coordinating node：负责接受请求并转到合适的节点，最终将结果汇聚到一起。每个节点都默认是协调者。
- Hot & Warm Node：不同硬件配置的 data node。
- 一个主分片就是一个 lucene 实例。主分片数在索引创建时指定，不允许修改，除非 reindex。
- 主副分片都可以 serve search。所以数据的冗余越多，搜索吞吐量就越大。
- Fail over: 集群中某个节点挂掉后，其上的 shard 会被重新分配到其他节点（当然需要有可用的副本分片）。

#### 文档的分布式存储

- 文档会存储在具体的某个主分片和副本分片上，比如文档 1 在 P0 和 R0 上。
- 文档要能均匀分布在所有分片上。
- 算法: shard = hash(\_routing) % number_of_primary_sharding。默认的\_routing 是文档 id。

更新文档时：

- 用户请求发给了 es 集群中的某个节点（充当协调者）。
- 节点充当协调者计算出对应的 shard 所在的 Node，并将请求路由给该 node
- node 收到请求后删除原来的文档，并重新创建新的文档。
- 成功后 Node 将请求发回给协调者，协调者再返回给用户。

## settings

- number_of_shards，主分片数。7.0 开始默认为 1（之前是 5）。这个配置在索引创建后不能修改。
- number_of_replicas，每个分片的副本数，默认为 1，可以临时修改。
- sharding for scalability，replicas for reliability and performance。
- 分片数设置过小：后续无法通过增加节点实现水平扩展。单分片数据量过大，数据重新分配耗时过长。
- 分片数设置过大：影响搜索结果相关性打分，影响统计结果准确性。单节点上过多的分片会影响性能。

集群健康状态：

- green: 主分片和副本都正常
- yellow: 主分片正常，有副本不正常
- red: 有主分片不正常

- http://localhost:9200/_cluster/health
- http://localhost:9200/_cat/nodes
- http://localhost:9200/_cat/shards

## Lucene Index

- lucene 中，单个倒排索引文件被称为 segment；segment 是自包含的，不可变的。
- lucene 中多个 segments 汇总起来就是 lucene 的 index，也就是 es 中的 shard。
- index 文档的时候，先写入 index buffer。
- 然后将 index buffer 里面的数据写入 segment。这个过程叫 refresh，refresh 不执行 fsync 操作。
- refresh 频率默认为 1 秒一次，可通过 index.refresh_interval 配置，refresh 后数据就可以被搜索到了。
- index buffer 被占满后也会触发 refresh。
- 为了保证数据不丢，在 index 文档的同时会写 transaction log。
- transaction log 默认落盘，每个分片有一个 transaction log。
- 查询总是会同时查所有的 segments，并对结果进行汇总。
- lucene 中有一个文件，用来记录所有 segments 信息，叫 commit point。
- index 文档时，首先发送文档到主分片，然后文档被发送到主分片的其他 replicas。in sync 之后副本就能够提供搜索服务，并且在主分片不能工作时被选为主分片。
- 如果要删除文档，会将信息记录在.del 文件中。查的时候会根据.del 文件过滤掉已经删除的文件。所以删除文档不会立即释放磁盘空间。

#### es flush & lucene commit

- refresh, index buffer 清空。
- fsync，写入磁盘。
- 清空 transaction log。
- 默认 30 分钟 flush 一次。
- transaction Log 满了也会 flush（默认 512M）。

#### merge

- 合并 segment 以减少 segment 数，删除已删除文档。
- merge 是自动进行的。
- 也可以手动 merge: POST my_index/\_forcemerge

#### 并发读写操作

- **es 中文档不可变，更新一个文档，就会将文档标记为删除，同时增加一个新文档，并将 version 加 1。**
- es 通过 if_seq_no + if_primary_term 进行乐观锁的并发控制。

## 分布式搜索的机制

- 搜索分为两个阶段，query 和 fetch。
- 首先用户搜索请求发到 es 节点，节点收到请求后，在主副分片中选择 num_of_shard 个分片发送查询请求。
- 被选中的分片执行查询，进行排序。每个分片都会返回 from + size 个排序后的文档 id 和排序值给 coordinating 节点。
- coordinating 节点会将 query 返回数据重新排序，选取 from 到 from+size 个文档的 id。
- 然后再以 multi get 的方式，取回详细的文档数据。
- query then fetch 存在潜在的性能问题，尤其是在深度分页的时候。
- 由于每个分片都基于自己分片上的数据进行相关性计算，会导致打分偏离的情况出现。
- 在数据量较少的时候，将主分片设置为 1，可以规避算分不准的问题。

#### 深度分页问题（search_after, scroll api）

from + size 不能超过 10000，否则会报 illegal_argument_exception。

search_after 能够避免深度分页问题：不支持指定页数，只能往下翻。

另一种方式是使用 scroll api，这种方式是创建快照。

## 排序

- 排序是针对字段原始内容进行的，倒排索引无法发挥作用。
- 需要使用正排索引。es 有两种实现方式： fielddata 和 doc values（列式存储，对 text 无效）。
- doc values 是在索引文档的时候和倒排索引一起创建的，使用磁盘。
- Fielddata 是在搜索时创建的，在 jvm 堆内创建。
- 默认使用 doc values，但是对 text 类型需要使用 fielddata。
- doc values 默认启用，但是如果你明确不需要该字段进行排序和聚合分析，则应该关闭 doc values。

```sh
# 多字段排序
POST /movies/_search
{
    "size": 5,
    "query": {
        "match_all": {}
    },
    "sort": [
        {"order_date": {"order":"desc"}},
        {"_doc": {"order":"asc"}},
        {"_score": {"order":"desc"}},
    ]
}
```

## Analysis 与 Analyzer (分词与分词器)

- analysis 是把全文本转换成一系列单词(term, token)的过程，也叫分词。analyzer 由三部分组成

- character filters（针对原始文本处理，例如去掉 html）
- tokenizer（按照规则切分为单词）
- token filter（将切分的单词进行加工，小写，删除 stopwords，增加同义词等等）

比如 Mastering Elasticsearch & Elasticsearch in Action 分词后得到的是 master, elasticsearch, action。

内置分词器

- Standard Analyzer，默认分词器，按词切分，小写处理
- Simple Analyzer，按非字母切分，小写处理
- Stop Analyzer，小写，停用词过滤
- Whitespace Analyzer，按空格切分，不转小写
- Keyword Analyzer，不分词，直接将输入当输出
- Patter Analyzer，正则表达式，默认\W+（非字符分隔）
- Language，提供了 30 多种常见语言分词器
- Customer Analyzer，自定义分词器

中文分词器

- icu-analyzer
- ik 支持自定义词库，支持热更新分词字典
- thulac 清华大学推出的一套中文分词器

## 配置

- xms 和 xmx 设置成一样，避免 heap resize。
- xmx 设置不要超过物理内存的 50%；单个节点不要超过 32G。
- 生产环境 JVM 必须使用 server 模式，要关闭 JVM swapping。
- 增加可用线程数的配置，ulimit -u 4096。

内存大小，内存和磁盘大小的比例。

- 搜索类的比例建议： 1：16
- 日志类： 1：48 ~ 1：96
