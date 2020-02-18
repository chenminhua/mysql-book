## 获取集群信息

```
/_cluster/state?pretty
/_cluster/health?pretty
/_node/http?pretty
```

## index

```
创建 index PUT /indexname
查看所有 index GET /_cat/indices?v
查看某个 index GET /indexname?pretty
删除 index DELETE /indexname
```

## document

加数据 POST /indexname/type/1 {"name": "aa", age: 12}
删除数据 DELETE /indexname/type/1

## setting

遇到过一个问题，es 写不进数据，检查一下 index 的设置发现这个 index 变成只读的了。原因是磁盘超过 watermark 了，可以通过修改 index 的设置来让数据可以继续写入。

```
PUT /_settings 或者 /indexname/_settings
{
    "index": {
        "blocks": {
            "read_only_allow_delete": "false"
        }
    }
}
```

## 查询

如何衡量相关性？

- Precision 查准率，尽可能返回较少无关文档
- Recall 查全率，尽量返回较多相关文档
- Ranking 是否能按照相关度进行排序

#### URI SEARCH

- q 指定查询语句，使用 query string syntax
- df 默认字段，不指定时，会对所有字段进行查询
- Sort 排序
- from/size 用于分页
- Profile 可以查看查询是如何被执行的

```
GET /movies/_search?q=2012&df=title&sort=year:desc&from=0&size=10&timeout=1s
{
    "profile": true
}

泛查询，针对对_all，所有字段。
GET /indexname/_search?q=sample'

指定字段查询
GET /indexname/_search?q=customer_first_name:Eddie

pharse查询，使用引号
GET /movies/_search?q=title:"Beautiful Mind"

term 查询，title里面包含Beautiful和Mind
GET /movies/_search?q=title:(Beautiful Mind)

布尔操作
AND / OR / NOT 或者 && / || / !, 必须大写， title:(matrix NOT reloaded)

分组
+ 表示 must, - 表示 must_not, 比如 title:(+matrix -reloaded)

范围查询，[]表示闭区间，{}表示开区间
year:{2019 TO 2018], year:[* TO 2018]

通配符查询
title:mi?d
title:be*

正则表达
title:[bt]oy

模糊匹配与近似查询
title:befutifl~1
title:"lord rings"~2

分页和排序
from, size, sort, fields
GET /_search?q=sample&from=0&size=2'

在多个index中查询
GET /index1,index2/_search?q=sample"

在全部 index 中搜索
GET /_search?q=sample'

按照 id 查
GET /indexname/_doc/1

```

#### Request Body Search

```sh
POST /movies/_search
{
    "sort": [{"order_date": "desc"}],
    "from": 10,
    "size": 20,
    "profile": true,
    "query": {
        "match_all": {}
    }
}

curl -X POST 172.168.7.1:9200/shakespeare/_search?pretty -H 'Content-Type: application/json' -d '{
    "query": {
        "query_string": {
            "query": "earthquake"
        }
    }
}'

curl -X POST 172.168.7.1:9200/shakespeare/_search?pretty -H 'Content-Type: application/json' -d '{
    "query": {
        "term": {
            "play_name": "Romeo and Juliet"
        }
    }
}'

# 脚本字段

# 使用match
POST movies/_search
{
    "query": {
        "match": {
            "title": "Last Christmas"
        }
    }
}
GET /movies/_search
{
    "query": {
        "match": {
            "title": {
                "query": "Last Christmas",
                "operator": "AND"
            }
        }
    }
}


# 短语搜索 match phrase，match pharse的term之间是AND的关系，而match的term之间默认是OR的关系
GET /movies/_search
{
    "query": {
        "match_phrase": {
            "title": {
                "query": "one love"
            }
        }
    }
}
### slop参数告诉match_phrase查询词条能够相隔多远时仍然将文档视为匹配。相隔多远的意思是，你需要移动一个词条多少次来让查询和文档匹配？
GET /movies/_search
{
    "query": {
        "match_phrase": {
            "title": {
                "query": "one love",
                "slop": 1
            }
        }
    }
}

# simple query string query
### 类似query string,但是会忽略错误，Term之间的关系默认是OR，可以指定Operator。
POST users/_search
{
    "query": {
        "simple_query_string": {
            "query": "chen minhua",
            "fields": ["name"],
            "default_operator": "AND"
        }
    }
}
```

#### terms query

#### bool query

#### filter (不在乎分数)

{
"query": {
"bool": {
"filter": {
"term": {
"name": "earthquake"
}
}
}
}
}

#### aggregations 聚类，类似于 group by

{
"aggs": {
"country": {
"terms": {
"field": "country_id"
}
}
}
}

## Mapping

- Mapping 定义索引中的字段名称和数据类型。
- 字段，倒排索引的相关配置。（analyzed or not, analyzer）
- Mapping 会把 JSON 文档映射成 lucence 所需要的扁平格式。
- 一个 Mapping 属于一个索引的 Type，7.0 开始不需要指定 type 信息（一个索引只能有一个 type）。

- text，keyword
- long, integer, short, byte, double, float, half_float, scaled_float
- date
- boolean
- binary
- integer_range, float_range, long_range, double_range, date_range
- Array datatype：Array support does not require a dedicated type
- Object datatype：object for single JSON objects
- Nested datatype：nested for arrays of JSON objects
- Geo-point datatype：geo_point for lat/lon points
- Geo-Shape datatype：geo_shape for complex shapes like polygons
- IP datatype：ip for IPv4 and IPv6 addresses

es 中其实不提供专门的数组类型，但是任何字段都可以包含多个相同类型的数值。

#### 定义 mapping

```sh
PUT movies {
    "mappings": {
        // define your mappings here
    }
}
```

为了减少工作量和出错概率，你可以这样建 mapping：创建一个临时的 index，写入样本数据；然后访问 mapping API 拿到动态 mapping 定义；最后用此配置创建你的索引。

```sh
# 控制字段不被索引
PUT users
{
    "mappings": {
        "properties": {
            "mobile": {
                "type": "text",
                "index": false
            }
        }
    }
}
```

#### dynamic mapping

- 在写入文档时，如果索引不存在，会自动创建索引。
- dynamic mapping 的机制，使得我们无需手动定义 mappings。
- es 会根据文档信息推算出字段类型。有时候会推算的不对。
- 推算错误会导致有些功能无法正常使用。

```sh
PUT mapping_test/_doc/1
{
    "firstName": "Chen",
    "lastName": "Minhua",
    "loginDate": "2019-07-24T10:29:12.103Z"
}
# 查看mapping
GET mapping_test/_mapping
```

#### 能否更改 mapping 字段的类型

如果是新增字段

- dynamic 设为 true 时，可以。
- dynamic 设为 false 时，mapping 不会被更新，新增字段不会被索引，但信息会出现在\_source 中
- dynamic 设为 strict 时，文档无法写入。

如果是已有字段，一旦有数据写入，就不能修改 mapping。如果要修改字段类型，必须 reindex。

```sh
PUT movies/_mapping
{
    "dynamic": "false"
}
```

#### 多字段类型

```
"properties": {
    "qrcode_display": { -
        "type": "text",
        "fields": { -
            "keyword": { -
                "type": "keyword",
                "ignore_above": 256
            }
        }
    },
}
```

#### mapping 中配置自定义 analyzer，char_filter, tokenizer, filter

https://github.com/geektime-geekbang/geektime-ELK/tree/master/part-1/3.12-%E5%A4%9A%E5%AD%97%E6%AE%B5%E7%89%B9%E6%80%A7%E5%8F%8AMapping%E4%B8%AD%E9%85%8D%E7%BD%AE%E8%87%AA%E5%AE%9A%E4%B9%89Analyzer

#### 精确值 vs 全文本

精确值： exact value, es 中使用 keyword，不需要进行分词处理。
全文本： full text, es 中使用 text，会被分词处理。

## 索引方式

默认的 analyzer 会 Lowercase 所有字符，并按单词切分后索引，比如"Late Night with Elasticssearch"被默认的 analyzer 处理后会得到"late","night","elasticsearch"三个 term，如果搜"late"会匹配上，但是如果搜"lat"或者"later"则不会。

你也可以设置字段为 not_analyzed，这样索引的时候 analysis 的过程就会被跳过，整个字段就被完整的索引，也只有完整输入才能匹配到。

## 预定义字段

\_id: 如果没有为文档指定 id,则 es 会自动为文档生成一个 id,例如 i0ee9mYBeoybXdlFPCNe

\_timestamp 已经废弃了
\_ttl 也已经废弃了

## index

close POST /indexname/\_close
open POST /indexname/\_open

## 搜索

## 基本操作

GET /megacorp/employee/\_search 搜索全部员工，默认会返回前十个结果
GET /megacorp/employee/\_search?q=last_name:lennon 寻找约翰列侬
HEAD /website/blog/123 查看是否存在
PUT /megacorp/employee/1 { ... } 更新 (\_version++, created 为 false)
POST /megacorp/employee/ { ... } 新建
DELETE /megacorp/employee/1 删除
GET /website/blog/123?\_source=title,text 不想要全部\_source
GET /website/blog/123/\_source 不想要元数据，只想要\_source
POST /website/blog/1/\_update
{"doc": {"tags": [ "testing" ],"views": 0}}

## mget api

可以使用 Mget 来检索多个文档
POST /website/blog/\_mget
{
"docs" : [
{ "_id" : 2 },
{ "_type" : "pageviews", "_id" : 1 }
]
}

POST /website/blog/\_mget
{
"ids" : [ "2", "1" ]
}

## bulk api

bulk api 允许我们一次性实现多个文档的 create, index, update, delete
POST /\_bulk
{ "delete": { "\_index": "website", "\_type": "blog", "\_id": "123" }} <1>
{ "create": { "\_index": "website", "\_type": "blog", "\_id": "123" }}
{ "title": "My first blog post" }
{ "index": { "\_index": "website", "\_type": "blog" }}
{ "title": "My second blog post" }
{ "update": { "\_index": "website", "\_type": "blog", "\_id": "123", "\_retry_on_conflict" : 3} }
{ "doc" : {"title" : "My updated blog post"} } <2>
每个子请求都会被独立执行，一个子请求的错误不会影响其他请求。

## 使用 DSL 语句查询

GET http://0.0.0.0:9200/megacorp/employee/_search
全文搜索 {"query" : {"match" : {"last_name" : "Smith"}}}
match_all 匹配所有文档
短语搜索 {"query": {"match_phrase": {"about": "rock climbing"}}}
多字段查询 {"multi_match": {
"query": "full text search",
"fields": [ "title", "body" ]}}
精确匹配 { "term": { "age": 26}}
多匹配条件精确匹配 {"terms": {"tag": ["search", "full_text", "nosql"]}}
分页 GET /\_search?size=5&from=

## 更复杂的搜索

{QUERY_NAME: {
ARGUMENT: VALUE,ARGUMENT: VALUE,...}}
{QUERY_NAME: {FIELD_NAME: {
ARGUMENT: VALUE,ARGUMENT: VALUE,...}}}

查找所有年龄大于 30，last_name 能 match 到 smith 的
GET /megacorp/employee/\_search
{"query": {
"filtered": {
"filter": {"range": {"age": {"gt": 30 }}},
"query": {"match": {"last_name": "smith"}}
}}}

#### 聚合，很像 sql 中的 group by

举个例子，让我们找到所有职员最大的共同点

```

GET /megacorp/employee/\_search
{
"aggs": {
"all_interests": {
"term": {"field": "interests"}
}
}
}

```

查询所有姓 smith 的人的最大共同点

```

GET /megacorp/employee/\_search
{
"query": {
"match": {
"last_name": "smith"
}
},
"aggs": {
"all_interests": {
"terms": {
"field": "interests"
}
}
}
}

```

统计每种兴趣下职员的平均年龄

```

GET /megacorp/employee/\_search
{
"aggs" : {
"all_interests" : {
"terms" : { "field" : "interests" },
"aggs" : {
"avg_age" : {
"avg" : { "field" : "age" }
}
}
}
}
}

```

结果为

```

"all_interests": {
"buckets": [
{
"key": "music",
"doc_count": 2,
"avg_age": {
"value": 28.5
}
},
{
"key": "forestry",
"doc_count": 1,
"avg_age": {
"value": 35
}
},
{
"key": "sports",
"doc_count": 1,
"avg_age": {
"value": 25
}
}
]
}

```

结果中

{
"\_index" : "website",
"\_type" : "blog",
"\_id" : "123",
"\_version" : 2,
"created": false <1>
}

```

#### 合并多个子句

以下实例查询的是邮件正文中含有“business opportunity”字样的星标邮件或收件箱中正文中含有“business opportunity”字样的非垃圾邮件：
{
"bool": {
"must": { "match": { "email": "business opportunity" }},
"should": [
{ "match": { "starred": true }},
{ "bool": {
"must": { "folder": "inbox" }},
"must_not": { "spam": true }}
}}
],
"minimum_should_match": 1
}
}

#### range 过滤 (按照指定范围查找一批数据)

{
"range": {
"age": {
"gte": 20,
"lt": 30
}
}
}

#### bool 过滤

must --> and
must_not --> not
should --> or

{
"bool": {
"must": {"term": {"folder": "inbox"}},
"must_not": {"term": {"tag": ""spam}},
"should": [
{"term": {"starred": true}}
{"term": {"unread": true}}
]
}
}

#### bool 查询

{
"bool": {
"must": { "match": { "title": "how to make millions" }},
"must_not": { "match": { "tag": "spam" }},
"should": [
{ "match": { "tag": "starred" }},
{ "range": { "date": { "gte": "2014-01-01" }}}
]
}
}

## analyzer

如何增加 analyzer?

#### 在创建 index 时增加 analyzer

#### 在配置 elasticsearch 时增加 analyzer

index:
analysis:
analyzer:
myCustomAnalyzer:
type: custom
tokenizer: myCustomTokenizer
filter: [myCustomerFilter1, myCustomerFilter2]
char_filter: myCustomCharFilter
tokenizer:
myCustomerTokenizer:
type: letter
filter:
myCustomerFilter1:
type: lowercase
myCustomerFilter2:
type: kstem
char_filter:
myCustomCharFilter:
type: mapping
mappings: ["ph=>f", "u=>you"]

#### 给 mapping 中的某个字段指定 analyzer

```

```

```
