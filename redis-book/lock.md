Setnx : set if not exists

- 加锁： setnx key
- 释放锁： del key
- 锁超时 ： expire

从 2.6.12 开始，set 涵盖了 setex 的功能，**Set key val EX 1000 NX**

虽然我们有了 MULTI + WATCH + EXEC 的事务，但是这种类似乐观锁的机制在高负载的情况下表现可能很糟糕，因为可能出现不断重试。
为了保证数据正确的同时，以可扩展的方式来处理市场交易，我们使用锁来保证市场在任一时刻只能上架或销售一件商品。

```java
public String acquireLockWithTimeout(Jedis conn, String lockName, long acquireTimeout, long lockTimeout){
    String identifier = UUID.randomUUID().toString();
    String lockKey = "lock:" + lockName;
    int lockExpire = (int)(lockTimeout / 1000);
    long end = System.currentTimeMillis() + acquireTimeout;
    while (System.currentTimeMillis() < end) {
        if (conn.setnx(lockKey, identifier) == 1){
            conn.expire(lockKey, lockExpire);
            return identifier;
        }
        if (conn.ttl(lockKey) == -1) {
            conn.expire(lockKey, lockExpire);
        }
        try {
            Thread.sleep(1);
        }catch(InterruptedException ie){
            Thread.currentThread().interrupt();
        }
    }
    return null;
}

public boolean releaseLock(Jedis conn, String lockName, String identifier) {
    String lockKey = "lock:" + lockName;
    while (true){
        conn.watch(lockKey);                          // 监视锁，防止有人在同时修改锁
        if (identifier.equals(conn.get(lockKey))){    // 检查锁是否还被这个线程持有
            Transaction trans = conn.multi();
            trans.del(lockKey);
            List<Object> results = trans.exec();
            if (results == null) continue;
            return true;
         }
         conn.unwatch();
         break;
    }
    return false;      // 进程已经失去了锁
}
```
