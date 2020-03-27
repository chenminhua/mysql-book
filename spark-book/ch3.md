RDD（弹性分布式数据集）就是分布式的元素集合。
在spark中，对数据的操作不外乎创建RDD，转化已有RDD以及调用RDD操作。而背后spark会将RDD中的数据分发到集群上，并将操作并行化。

# 创建RDD

```python
# 直接将已有集合转为RDD
lines = sc.parallelize(['hello', 'world'])

# 文件读取
lines = sc.textFile('README.md')
```

# 转化操作和行动操作

### 转化操作
转化操作将一个RDD转化为另一个RDD，比如

```python
errorsRDD = inputRDD.filter(lambda x: "error" in x)
warningsRDD = inputRDD.filter(lambda x: "warning" in x)
badLinesRDD = errorsRDD.union(warningsRDD)
```

常见转化操作如下

```python
map
filter
flatMap
distinct 生成一个只包含不同元素的RDD
sample 采样

union(other) 合并
intersection(other) 交集
subtract(other) 差集
cartesian(other) 笛卡尔积
```

### 行动操作
行动操作会对RDD计算出一个结果，比如

```python
badLinesRDD.count()   #计数

for line in badLinesRDD.take(10):  #取前十个
  print line
```

常见的行动操作如下

```python
collect  返回所有元素
count    返回元素个数
countByValue   返回各个元素出现次数
take(n)        返回n个元素
top(n)         返回最前面的n个元素
takeOrdered(n) 按顺序返回前n个元素
takeSample(false, n) 返回任意n个元素
reduce(func)   reduce
fold(init)()   和reduce一样，但是要提供初始值
aggregate(zeroValue)  类似于reduce
forEach()      对每个元素执行操作，但不返回
```

### 不同类型RDD间的转换
有些函数只能用于特定类型的RDD，比如mean()和variance()只能用在数值RDD上，而join()只能用在键值对RDD上

### 区别
虽然你可以在任何时候定义新的RDD，但是spark只会惰性计算这些RDD，它们只在第一次行动操作时才会真正计算。在我们调用sc.textFile()时，数据并没有被读取进来，而是在必要的时候才读取
RDD会在你每次对它进行行动操作时重新计算，如果想在多个行动操作中重用一个RDD，可以使用RDD.persist()缓存这个RDD

```
pythonLines.persist
pythonLines.count()
```

# RDD持久化（缓存）
默认情况下persist会把数据以序列化的形式缓存在jvm的堆空间中。
