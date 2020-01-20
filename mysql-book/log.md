**binlog（归档日志），是 server 层的日志，不管用啥存储引擎都有；而 redo log 是 innodb 层的日志。binlog 是逻辑日志(记录这个操作要干啥)，而 redo log 是物理日志(记录了在某个数据页上做了什么修改)。**

## binlog 和 redolog 是啥时候写的？

```
update T set c=c+1 where ID=2;
```

1. 首先执行器调用 Innodb 的接口，按主键查回一条数据(如果在内存里了就直接返回，否则先从磁盘查到内存里面再返回)。
2. 然后执行器计算 c+1，并调用存储引擎去写入。
3. 然后存储引擎先写内存，再写 redo log，redo log 的状态为 prepared。
4. 然后返回 server 层，在 server 层记录 binlog。
5. 然后再通知 innodb 将 redo log 的状态改为 commited，并提交事务。

注意，整个步骤里面我们都不用去找磁盘上的那条数据修改，只要在 innodb 写 redo log 和内存，然后在 server 层写 binlog。

建议将**sync_binlog**设置为 1，这样每次事务的 binlog 都持久化到磁盘，保证 mysql 异常重启不丢 binlog。

# binlog

## binlog 有啥用?

## 如何让数据库恢复到半个月内任意一秒？

要做到这一点，我们需要做两件事。第一：我们需要保存半个月来所有的 binlog；第二：我们要定期做全库备份。

假如你做了以上两点，然后有一天不小心删库了，你希望回到删库前一秒，就可以

1. 首先找到最近的一次全量备份，将其恢复到临时库。
2. 然后从备份时间点开始，将 binlog 重放到要恢复的那个时刻。
3. 这样临时库就和误删前线上库一样了，然后你可以把表数据从临时库取出，按需恢复到线上。

## 备份间隔影响什么指标？

最长恢复时间

# redo log

## 为啥要有 redo log

为了让 update 更快。如果没有 redo log 的话，更新一条数据要先将查到其在磁盘上的位置，然后更新到磁盘上。而 redo log 是一种 WAL，也就是先写日志，以后再落盘。redo log 是 innodb 实现的。

## innodb_flush_log_at_trx_commit 与 crash-safe

**innodb_flush_log_at_trx_commit 建议设置为 1**，表示每次事务的 redo log 都直接持久化到磁盘，这样可以保证 MySQL 异常重启之后数据不丢失，即 crash-safe。

## redo log 是如何实现的

innodb 的 redo log 是固定大小的，比如可以配置一组 4 个文件，每个 1G，每次从头开始写，写到末尾又回到开头循环写。redo log 维护两个指针，一个叫 write pos，一个叫 checkpoint。每次写 redo log 就把 write pos 往前推；每次根据 redo log 完成落盘，就把 checkpoint 往前推。如果 write pos 追上了 checkpoint，就要停止新的写，把 checkpoint 往前推。

有写请求时，innodb 先把记录写到 redo log，并更新内存，然后等系统比较空闲的时候，再将其更新到磁盘里面。

## 为啥 redo log 要做两阶段提交？

为了让 redo log 和 binlog 保持一致。否则如果 mysql 异常重启的话，可能导致 binlog 和 redo log 不一致。

## binlog 写入机制

事务执行过程中，先把日志写到 binlog cache，事务提交时再把 binlog cache 写入 binlog 文件中。

系统给 binlog cache 分配了一片内存，每个线程一个，参数 binlog_cache_size 用于控制单个线程内 binlog cache 所占内存的大小。如果超过这个参数规定大小，就要暂存到磁盘。

事务提交时，binlog cache 中的完整事务写入 binlog，并清空 binlog cache。事实上，binlog cache 写入到 binlog 文件的步骤也是分两步的。第一步是写入文件系统的 page cache，第二步才是 fsync 到磁盘。

sync_binlog=0 的时候，表示每次提交事务都只 write,不 fsync.

sync_binlog=1 的时候，表示每次提交事务都会执行 fsync.

sync_binlog=N(N>1) 的时候，表示每次提交事务都 write，但累积 N 个事务后才 fsync。

如果你的 io 是瓶颈，可以考虑将 sync_binlog 设大一点，但是就会存在异常重启时丢失事务 binlog 的风险。一般不建议将 sync_binlog 设置为 0，会丢日志。
