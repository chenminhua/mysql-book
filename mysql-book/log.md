- binlog（归档日志），是 server 层的日志，是逻辑日志（记录操作干了什么），是追加写的。
- redo log 是 innodb 的日志，是物理日志(记录了在某个数据页上做了什么修改)，是循环写的。
- undo log 也是 innodb 的，是用于实现 MVCC 的（事务的隔离与回滚），undo log 记录了数据修改前的值。

## binlog 和 redo log 是啥时候写的？

```
update T set c=c+1 where ID=2;
```

1. 执行器调用 Innodb 的接口，按主键查回一条数据(如果在内存里了就直接返回，否则先从磁盘查到内存里面再返回)。
2. 然后执行器计算 c+1，并调用存储引擎去写入。
3. 然后存储引擎先写内存，再写 redo log，redo log 的状态为 prepared。
4. 然后返回 server 层，在 server 层记录 binlog。
5. 然后再通知 innodb 将 redo log 的状态改为 commited，并提交事务。

总结起来就是：查数据，写内存，写 redo log(prepared)，写 binlog，提交事务(redo log committed)。注意，整个步骤里面我们都不用去找磁盘上的那条数据修改，只要在 innodb 写 redo log 和内存，然后在 server 层写 binlog。

### 为啥 redo log 要做两阶段提交？

为了让 redo log 和 binlog 保持一致。否则如果 mysql 异常重启的话，可能导致 binlog 和 redo log 不一致。如果你需要将数据库恢复到指定的某一秒，首先，找到最近的一次全量备份，如果你运气好，可能就是昨天晚上的一个备份，从这个备份恢复到临时库；然后，从备份的时间点开始，将备份的 binlog 依次取出来，重放到中午误删表之前的那个时刻。这样你的临时库就跟误删之前的线上库一样了，然后你可以把表数据从临时库取出来，按需要恢复到线上库去。

如果没有两阶段提交，就可能出现丢失 binlog 或多出 binlog 的问题，数据库的状态就有可能和用它的日志恢复出来的库的状态不一致。当你需要扩容的时候，也就是需要再多搭建一些备库来增加系统的读能力的时候，现在常见的做法也是用全量备份加上应用 binlog 来实现的。

# binlog

## binlog 写入机制

事务执行过程中，先把日志写到 binlog cache（感觉其实是 buffer，而不是 cache），事务提交时再把 binlog cache 写入 binlog 文件中。

系统给 binlog cache 分配了一片内存，每个线程一个，参数 binlog_cache_size 用于控制单个线程内 binlog cache 所占内存的大小。如果超过这个参数规定大小，就要暂存到磁盘。事务提交时，binlog cache 中的完整事务写入 binlog，并清空 binlog cache。事实上，binlog cache 写入到 binlog 文件也分两步。第一步是写入文件系统的 page cache，第二步才是 fsync 到磁盘。

如果你的 io 是瓶颈，可以考虑将 sync_binlog 设大一点，但是就会存在异常重启时丢失事务 binlog 的风险。一般不建议将 sync_binlog 设置为 0，会丢日志。

## 如何让数据库恢复到半个月内任意一秒？

要做到这一点，我们需要做两件事。第一：我们需要保存半个月来所有的 binlog；第二：我们要定期做全库备份。建议将**sync_binlog**设置为 1，这样每次事务的 binlog 都持久化到磁盘，保证 mysql 异常重启不丢 binlog。

假如你做了以上两点，然后有一天不小心删库了，你希望回到删库前一秒，就可以

1. 首先找到最近的一次全量备份，将其恢复到临时库。
2. 然后从备份时间点开始，将 binlog 重放到要恢复的那个时刻。
3. 这样临时库就和误删前线上库一样了，然后你可以把表数据从临时库取出，按需恢复到线上。

## 备份间隔影响什么指标？

最长恢复时间

# redo log

## 为啥要有 redo log

为了让 update 更快。而 redo log 是一种 WAL，先写日志以后再落盘。避免了频繁的磁盘读写。

## redo log 是如何实现的

innodb 的 redo log 是固定大小的，比如可以配置一组 4 个文件，每个 1G，每次从头开始写，写到末尾又回到开头循环写。redo log 维护两个指针，一个叫 write pos，一个叫 checkpoint。每次写 redo log 就把 write pos 往前推；每次根据 redo log 完成落盘，就把 checkpoint 往前推。如果 write pos 追上了 checkpoint，就要停止新的写，把 checkpoint 往前推。也就是 flush 一些脏页到磁盘。(脏页就是有更新，但还没 flush 到磁盘)

默认在事务提交时，将 redo log 缓冲写入 redo log 文件，并调用 fsync 操作。参数 innodb_flush_log_at_trx_commit 用来控制是否每次都在提交时写入文件。

注意，这里有提到两个落盘操作，他们是不同的，一个是按照 redo log 记录的内容更新磁盘上的数据，因为在写数据库的时候并没有直接更新磁盘，而只更新了内存，并记录了 redo log。另一个是 redo log 自己的落盘，是为了 crash safe。

有写请求时，innodb 先把记录写到 redo log，并更新内存，然后等系统比较空闲的时候，再将其更新到磁盘里面。平时执行很快的更新操作，其实就是在写内存和日志，而 MySQL 偶尔“抖”一下的那个瞬间，可能就是在刷脏页（flush）。

redo log 并没有记录数据页的完整数据，所以它并没有能力自己去更新磁盘数据页。对于正常运行的情况，刷脏页的这个过程，甚至与 redo log 毫无关系。而在崩溃恢复场景中，InnoDB 如果判断到一个数据页可能在崩溃恢复的时候丢失了更新，就会将它读到内存，然后让 redo log 更新内存内容。更新完成后，内存页变成脏页，就回到了第一种情况的状态。

redo log buffer 就是一块内存，用来先存 redo 日志的。也就是说，在执行第一个 insert 的时候，数据的内存被修改了，redo log buffer 也写入了日志。但是，真正把日志写到 redo log 文件（文件名是 ib_logfile+数字），是在执行 commit 语句的时候做的。单独执行一个更新语句的时候，InnoDB 会自己启动一个事务，在语句执行完成的时候提交。过程跟上面是一样的，只不过是“压缩”到了一个语句里面完成。

## 什么情况会引发数据库的 flush 过程呢？

1. redo log 写不下了。这时候系统会停止所有更新操作进行 flush。这种情况是 InnoDB 要尽量避免的。
2. 系统内存不足，需要淘汰一些数据页，空出内存给别的数据页使用。如果淘汰的是“脏页”，就要先将脏页写到磁盘。
3. 系统空闲的时候。
4. MySQL 正常关闭的情况。

刷脏页虽然是常态，但是出现以下这两种情况，都是会明显影响性能的：

1. 一个查询要淘汰的脏页个数太多，会导致查询的响应时间明显变长；
2. 日志写满，更新全部堵住，写性能跌为 0。

## InnoDB 刷脏页的控制策略

这就要用到 innodb_io_capacity (我的机器设的是 4000)这个参数了，它会告诉 InnoDB 你的磁盘能力。这个值我建议你设置成磁盘的 IOPS。磁盘的 IOPS 可以通过 fio 这个工具来测试，下面的语句是我用来测试磁盘随机读写的命令：

     fio -filename=$filename -direct=1 -iodepth 1 -thread -rw=randrw -ioengine=psync -bs=16k -size=500M -numjobs=10 -runtime=10 -group_reporting -name=mytest

如果你的主机磁盘用的是 SSD，但是却设置了很低的 innodb_io_capacity，InnoDB 认为你的机器很烂，所以刷脏页刷得很慢，这样就造成了脏页累积，影响了查询和更新性能。

InnoDB 的刷盘速度要参考这两个因素：**一个是脏页比例，一个是 redo log 写盘速度。**参数 innodb_max_dirty_pages_pct 是脏页比例上限，默认值是 75%。

现在你知道了，InnoDB 会在后台刷脏页，而刷脏页的过程是要将内存页写入磁盘。所以，无论是你的查询语句在需要内存的时候可能要求淘汰一个脏页，还是由于刷脏页的逻辑会占用 IO 资源并可能影响到了你的更新语句，都可能是造成你从业务端感知到 MySQL“抖”了一下的原因。

要尽量避免这种情况，你就要合理地设置 innodb_io_capacity 的值，并且**平时要多关注脏页比例，不要让它经常接近 75%**。**脏页比例是通过 Innodb_buffer_pool_pages_dirty/Innodb_buffer_pool_pages_total 得到的**

一旦一个查询请求需要在执行过程中先 flush 掉一个脏页时，这个查询就可能要比平时慢了。而 MySQL 中的一个机制，可能让你的查询会更慢：在准备刷一个脏页的时候，如果这个数据页旁边的数据页刚好是脏页，就会把这个“邻居”也带着一起刷掉；而且这个把“邻居”拖下水的逻辑还可以继续蔓延，也就是对于每个邻居数据页，如果跟它相邻的数据页也还是脏页的话，也会被放到一起刷。在 InnoDB 中，innodb_flush_neighbors 参数就是用来控制这个行为的，值为 1 的时候会有上述的“连坐”机制，值为 0 时表示不找邻居，自己刷自己的。

找“邻居”这个优化在机械硬盘时代是很有意义的，可以减少很多随机 IO。机械硬盘的随机 IOPS 一般只有几百，相同的逻辑操作减少随机 IO 就意味着系统性能的大幅度提升。而如果使用的是 SSD 这类 IOPS 比较高的设备的话，我就建议你把 innodb_flush_neighbors 的值设置成 0。因为这时候 IOPS 往往不是瓶颈，而“只刷自己”，就能更快地执行完必要的刷脏页操作，减少 SQL 语句响应时间。在 MySQL 8.0 中，innodb_flush_neighbors 参数的默认值已经是 0 了。
