## 如何构建Key
key不要太长，因为lookup of the key may require several costly key-comparisons。
key不要太短，不要牺牲可读性。
Try to stick with a schema.  "Object-type:id", "user:1000:followers", "comment:1234:reply.to"

```
Exists k
Set k v
Del k
Type k
```

## 字符串，binary-safe string
不能超过512M。

```
set k v nx        表示只在k不存在的时候才能set
set k v xx        表示只在k存在的时候才能set
set k v ex 10     表示 10秒 后 k 失效

incr k            原子增1
incrby k 100      原子增100
类似的还有 decr decrby

getset k newval   设置新值并返回旧值

批量get set
Mset k1 100 k2 1000 k3 10000
Mget k1 k2 k3

Expire key <seconds>   设定多少秒后k失效
ttl key           查看key何时失效
```

## List
双向链表，首尾添加元素很快，但access by index就可能很慢。如果你需要快速访问中间元素，请使用zset。

```
LPUSH KEY V1 V2 V3
RPUSH KEY V4 V5 V6

LLEN KEY    列表长度
LRANGE KEY 0 -1   得到结果 [V3 V2 V1 V4 V5 V6]

移除元素
LPOP Key
RPOP Key

LTRIM KEY 0 1000     保留前1000 个元素，其余删除
```

List常见应用场景: timeline, 消息队列，任务队列。

```
BRPOP KEY 5       阻塞式pop, 最多等5s。
BRPOP KEY 0       阻塞式pop, wait forever until have sth to pop
BRPOP KEY1 KEY2 KEY3 5   阻塞式pop，可以同时等多个列表
类似的当然还有BLPOP
```

redis在blpop命令处理过程时，首先会去查找key对应的list，如果存在，则pop出数据响应给客户端。否则将对应的key push到blocking\_keys数据结构当中，对应的value是被阻塞的client。当下次push命令发出时，服务器检查blocking\_keys当中是否存在对应的key，如果存在，则将key添加到ready\_keys链表当中，同时将value插入链表当中并响应客户端。

因为BRPOP和BLPOP都可以同时POP多个LIST，所以他们的返回除了value，还要包含对应的key。

```
// 这两个命令负责将元素从一个列表移动到另一个列表
RPOPLPUSH  src-key dest-Key
BRPOPLPUSH src-key dest-key timeout
```

## Set
```
sadd myset 1 2 3
smember myset
sismember myset 3
```
Sets are good for expressing relations between objects. 比如说，我们可以用set来实现tag的功能。

## sorted set (zset)

```
## zset,redis的有序集合
ZADD key-name score member [score member ...]      # 将带有给定分值的成员添加到有序集合里面
ZREM key-name member [member]     #从有序集合中删除元素
ZCARD key-name                    #返回有序集合包含的成员数
ZINCRBY key-name increment member  #将member成员的分数增加increment
ZCOUNT key-name min max     #返回分值在min到max之间的成员数量
ZRANGE z 0 -1 withscores   # 根据元素所处的位置取出多个元素
ZRANGE z 0 800 withscores  # 取出排名前八百的
ZRANK key-name member      # 返回成员排名
ZREVRANK key-name member   # 返回成员排名
ZREVRANGE key-name min max
ZREVRANGEBYSCORE key-name max min
zrangebyscore z 0 800 withscores # 获取给定分值范围内的元素
```

## Hash 
```
hmset user:1000 username antirez birthyear 1977 verified 1
hget user:1000 username
hget user:1000 birthyear
hgetall user:1000
hmget user:1000 username birthyear no-such-field
hincrby user:1000 birthyear 10
```

## Bit Arrays
offset最大不超过Integer.MAX\_VALUE，也就是最大 512M。

## HyperLogLog

```
pfadd hll a b c d
pfcount hll     // 返回4
Pfmerge hll1 hll2 // 把 hll2 merge到 hll1中
conn = redis.Redis()
for i in range(100):
    pipe = conn.pipeline()
    for j in range(10000):
        conn.pfadd("hll","foo" + str(i*10000 + j))
    pipe.execute()

```

## Stream

Append-only collections of map-like entries that provide an abstract log data type.
https://redis.io/topics/streams-intro

## GEO

```
新建
GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania"

计算距离
GEODIST Sicily Palermo Catania
> "166274.1516"

查看 （15, 37）周围 100 km 内的城市
GEORADIUS Sicily 15 37 100 km
> "Catania"

查看 (15, 37) 周围 200 km 内的城市
GEORADIUS Sicily 15 37 200 km
1) "Palermo"
2) "Catania"

### geohash
https://zhuanlan.zhihu.com/p/35940647
```

## reference
[redis数据类型](https://redis.io/topics/data-types-intro)

