## mapping types

7.x 开始已经没有 mapping 了。

[removal of mapping types](https://www.elastic.co/guide/en/elasticsearch/reference/current/removal-of-types.html)

## why are mapping types being removed

最初，es 认为 index 类比于数据库，而 type 类比与表。但这不是一个好的类比。

在 SQL 数据库中，表之间是相互独立的。而在 mapping types 中的 fields 之间确实强相关的。在 es 的 index 中，不同 mapping types 中的同名 fields 在 lucene 中其实是同一个。

On top of that, storing different entities that have few or no fields in common in the same index leads to sparse data and interferes with Lucene’s ability to compress documents efficiently.

## 过去的 mapping api

```
查看某个 index 下所有 types GET /indexname/_mapping
查看 types GET /indexname/typename/_mapping?pretty
删除 type (已经不支持了，需要安装 plugin install delete-by-query 才行)
```

```
新建 mapping PUT /company/employee/_mapping
{
    "employee": {
        "properties": {
        "name": {
            "type": "text"
            }
        }
    }
}
```

```
扩展 mapping PUT /company/employee/_mapping
{
    "employee": {
        "properties": {
            "name": {
                "type": "text"
            },
            "age": {
                "type": "long"
            }
        }
    }
}
```

修改 mapping，比如把上面的 name 改成 long 型，则只能删掉数据重新 index 一遍才行。
