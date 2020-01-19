## 如何构建 Key

key 不要太长，因为 lookup of the key may require several costly key-comparisons。
key 不要太短，不要牺牲可读性。
Try to stick with a schema. "Object-type:id", "user:1000:followers", "comment:1234:reply.to"

```
Exists k
Set k v
Del k
Type k
```

## 字符串，binary-safe string

不能超过 512M。

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

双向链表，首尾添加元素很快，但 access by index 就可能很慢。如果你需要快速访问中间元素，请使用 zset。

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

List 常见应用场景: timeline, 消息队列，任务队列。

```
BRPOP KEY 5       阻塞式pop, 最多等5s。
BRPOP KEY 0       阻塞式pop, wait forever until have sth to pop
BRPOP KEY1 KEY2 KEY3 5   阻塞式pop，可以同时等多个列表
类似的当然还有BLPOP
```

redis 在 blpop 命令处理过程时，首先会去查找 key 对应的 list，如果存在，则 pop 出数据响应给客户端。否则将对应的 key push 到 blocking_keys 数据结构当中，对应的 value 是被阻塞的 client。当下次 push 命令发出时，服务器检查 blocking_keys 当中是否存在对应的 key，如果存在，则将 key 添加到 ready_keys 链表当中，同时将 value 插入链表当中并响应客户端。

因为 BRPOP 和 BLPOP 都可以同时 POP 多个 LIST，所以他们的返回除了 value，还要包含对应的 key。

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

Sets are good for expressing relations between objects. 比如说，我们可以用 set 来实现 tag 的功能。

## sorted set (zset)

与 set 的不同之处在于 zset 中的每个数都对应一个绑定的浮点数 score。

- if A.score > B.score, then A > B
- if A.score == B.score，then compare lexicographically.

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

示例

```
zadd hackers 1940 "Alan Kay"
zadd hackers 1957 "Sophie Wilson"
zadd hackers 1953 "Richard Stallman"
zadd hackers 1949 "Anita Borg"
zadd hackers 1965 "Yukihiro Matsumoto"
zadd hackers 1914 "Hedy Lamarr"
zadd hackers 1916 "Claude Shannon"
zadd hackers 1969 "Linus Torvalds"
zadd hackers 1912 "Alan Turing"

zrange hackers 0 -1
1) "Alan Turing"
2) "Hedy Lamarr"
3) "Claude Shannon"
4) "Alan Kay"
5) "Anita Borg"
6) "Richard Stallman"
7) "Sophie Wilson"
8) "Yukihiro Matsumoto"
9) "Linus Torvalds"

zrevrange hackers 0 -1
1) "Linus Torvalds"
2) "Yukihiro Matsumoto"
3) "Sophie Wilson"
4) "Richard Stallman"
5) "Anita Borg"
6) "Alan Kay"
7) "Claude Shannon"
8) "Hedy Lamarr"
9) "Alan Turing"

zrange hackers 0 -1 withscores
 1) "Alan Turing"
 2) "1912"
 3) "Hedy Lamarr"
 4) "1914"
 5) "Claude Shannon"
 6) "1916"
 7) "Alan Kay"
 8) "1940"
 9) "Anita Borg"
10) "1949"
11) "Richard Stallman"
12) "1953"
13) "Sophie Wilson"
14) "1957"
15) "Yukihiro Matsumoto"
16) "1965"
17) "Linus Torvalds"
18) "1969"

zrangebyscore hackers -inf 1950
1) "Alan Turing"
2) "Hedy Lamarr"
3) "Claude Shannon"
4) "Alan Kay"
5) "Anita Borg"

zremrangebyscore hackers 1940 1960
(integer) 4

zrank hackers "Claude Shannon"
(integer) 2
zrank hackers "Alan Turing"
(integer) 0
// also zrevrank



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

## Bit Arrays (bitmap, 位图)

offset 最大不超过 Integer.MAX_VALUE，也就是最大 512M。可以用来搞 bloom filter 。

```
SETBIT key offset val
GETBIT key offset
BITCOUNT key [start] [end]
BITPOS KEY bit [start] [end]
```

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

[redis 数据类型](https://redis.io/topics/data-types-intro)
