构建计数信号量时要考虑的事情和构建其他类型的锁时要考虑的事情大部分相同。
比如判断是哪个客户端取得了锁，如何处理客户端在获得锁之后崩溃的情况，如何处理超时。

```java
public String acquireFairSemaphore(Jedis conn, String semname, int limit, long timeout){
    String identifier = UUID.randomUUID().toString();
    String czset = semname + ":owner";
    String ctr = semname + ":counter";
    long now = System.currentTimeMillis();
    Transaction trans = conn.multi();
    trans.zremrangeByScore(semname.getBytes(),"-inf".getBytes(),String.valueOf(now - timeout).getBytes());
    ZParams params = new ZParams();
    params.weights(1, 0);
    trans.zinterstore(czset, params, czset, semname);
    trans.incr(ctr);
    List<Object> results = trans.exec();
    int counter = ((Long)results.get(results.size() - 1)).intValue();
    trans = conn.multi();
    trans.zadd(semname, now, identifier);
    trans.zadd(czset, counter, identifier);
    trans.zrank(czset, identifier);
    results = trans.exec();
    int result = ((Long)results.get(results.size() - 1)).intValue();
    if (result < limit){return identifier;}
    trans = conn.multi();
    trans.zrem(semname, identifier);
    trans.zrem(czset, identifier);
    trans.exec();
    return null;
}
public boolean releaseFairSemaphore(Jedis conn, String semname, String identifier){
    Transaction trans = conn.multi();
    trans.zrem(semname, identifier);
    trans.zrem(semname + ":owner", identifier);
    List<Object> results = trans.exec();
    return (Long)results.get(results.size() - 1) == 1;
}
```
