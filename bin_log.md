binlog（归档日志），是 server 层的日志，不管用啥存储引擎都有；而 redo log 是 innodb 层的日志。

binlog 是逻辑日志(记录这个操作要干啥)，而 redo log 是物理日志(记录了 **在某个数据页上做了什么修改**
)。

#### binlog 和 redolog 是啥时候写的？

比如我们要完成下面的操作

```
update T set c=c+1 where ID=2;
```

1. 我们从执行器开始说起吧，首先执行器调用 Innodb 的接口，按主键查回一条数据。
2. 然后执行器计算 c+1，并调用存储引擎去写入。

#### binlog 有啥用?

####
