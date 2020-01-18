binlog（归档日志），是 server 层的日志，不管用啥存储引擎都有；而 redo log 是 innodb 层的日志。

binlog 是逻辑日志(记录这个操作要干啥)，而 redo log 是物理日志(记录了 **在某个数据页上做了什么修改**
)。

#### binlog 和 redolog 是啥时候写的？

比如我们要完成下面的操作

```
update T set c=c+1 where ID=2;
```

1. 我们从执行器开始说起吧，首先执行器调用 Innodb 的接口，按主键查回一条数据(如果在内存里了就直接返回，否则先从磁盘查到内存里面再返回)。
2. 然后执行器计算 c+1，并调用存储引擎去写入。
3. 然后存储引擎先写内存，再写 redo log，redo log 的状态为 prepared。
4. 然后返回 server 层，在 server 层记录 binlog。
5. 然后再通知 innodb 将 redo log 的状态改为 commited，并提交事务。

注意，整个步骤里面我们都不用去找磁盘上的那条数据修改，只要在 innodb 写 redo log 和内存，然后在 server 层写 binlog。

建议将**sync_binlog**设置为 1，这样每次事务的 binlog 都持久化到磁盘，保证 mysql 异常重启不丢 binlog。

#### 为啥 redo log 要做两阶段提交？

为了让 redo log 和 binlog 保持一致。否则如果 mysql 异常重启的话，可能导致 binlog 和 redo log 不一致。

#### binlog 有啥用?
