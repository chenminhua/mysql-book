#### 为啥要有 redo log

为了让 update 更快。如果没有 redo log 的话，更新一条数据要先将查到其在磁盘上的位置，然后更新到磁盘上。而 redo log 是一种 WAL，也就是先写日志，以后再落盘。

#### redo log 是 那一层实现的？

innodb 实现的

#### innodb_flush_log_at_trx_commit 与 crash-safe

innodb_flush_log_at_trx_commit 这个参数设置成 1 的时候，表示每次事务的 redo log 都直接持久化到磁盘。**这个参数建议设置成 1，这样可以保证 MySQL 异常重启之后数据不丢失，即 crash-safe**。

#### redo log 是如何实现的

innodb 的 redo log 是固定大小的，比如可以配置一组 4 个文件，每个 1G，每次从头开始写，写到末尾又回到开头循环写。redo log 维护两个指针，一个叫 write pos，一个叫 checkpoint。每次写 redo log 就把 write pos 往前推；每次根据 redo log 完成落盘，就把 checkpoint 往前推。如果 write pos 追上了 checkpoint，就要停止新的写，把 checkpoint 往前推。

有写请求时，innodb 先把记录写到 redo log，并更新内存，然后等系统比较空闲的时候，再将其更新到磁盘里面。

#### 如何让数据库恢复到半个月内任意一秒？
