# 累积器（对信息进行聚合）
提供了将工作节点中的值聚合到驱动器程序的简单语法，下面的例子累计文件中的空行。

```python
file = sc.textFile(inputFile)
blankLines = sc.accumulator(0)  #累加器

def extractCallSigns(line):
  global blankLines #访问全局变量
  if (line == ""):
    blankLines += 1
  return line.split(" ")

callSigns = file.flatMap(extractCallSigns)
callSigns.saveAsTextFile(outputDir + '/callsigns')
print "blk lines:", blankLines.value
```

# 广播变量（高效分发较大的对象）
向所有工作节点发送一个较大的制度值

```python
signPrefixes = sc.broadcast(loadCallSignTable())
def processSignCount(sign_count, signPrefixes):
  country = lookupCountry(sign_count[0], signPrefixes.value)
  count = sign_count[1]
  return (country, count)

countryContactCounts = (contactCounts.map(processSignCount).reduceByKey((lambda x,y: x+y)))
```

