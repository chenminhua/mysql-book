# 键值对操作
spark为包含键值对类型的RDD提供了一些专有的操作。



```python
# rdd 为 {(1,2), (3,4), (3,6)}
rdd.reduceByKey((x,y) => x+y)   #{(1,2),(3,10)}
rdd.groupByKey()                #{(1,[2]),(3,[4,6])}
rdd.mapValues(x => x+1)         #{(1,3),(3,5),(3,7)}
rdd.flatMapValues(x => (x to 5)) #{(1,2),(1,3),(1,4),(1,5),(3,4),(3,5)}
rdd.keys()      #{1,3,3}
rdd.values()    #{2,4,6}
rdd.sortByKey()  #按键排序

# other{(3,9)}
rdd.subtractBykey(other)   #{(1,2)}
rdd.join(other)            #{(3,(4,9)), (3,(6,9))}
rdd.rightOuterJoin(other)  #{(3,(Some(4),9)), (3,(Some(6),9))}
rdd.leftOuterJoin(other)   #{(1,(2,None)), (3,(4,Some(9))),(3,(6,Some(9)))}
rdd.cogroup(other)         #{(1,([2],[])),(3,([4,6],[9]))}
```

### 聚合操作

```python
rdd = sc.textFile('README.md')
words = rdd.flatMap(lambda x: x.split(" "))
result = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y:x +y)
result.sortBy(lambda x: x[1]).collect()
```

### combimeByKey
最为常用的基于键的聚合操作。

```
sumCount = nums.combineByKey((lambda x: (x, 1)),
    (lambda x,y: (x[0] + y, x[1] + 1)),
    (lambda x,y: (x[0] + y[0], x[1] + y[1])))
sumCount.map(lambda key, xy: (key, xy[0]/xy[1])).collectAsMap()
```

### 数据分组

### 连接

### 行动操作
```python
# {(1,2),(3,4),(3,6)}
rdd.countByKey()    #{(1,1),(3,2)}
rdd.collectAsMap()  #Map{(1,2),(3,4),(3,6)}
rdd.lookup(3)    # [4,6]
```


### 数据分区






