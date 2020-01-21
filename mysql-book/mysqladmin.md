```
sudo mysqladmin -p -u root version
```

## 配置查看

mysql --help | grep my.cnf

当几个配置文件中包含同一个参数，mysql 会以最后一个配置文件中的参数为准。

## server 排查

show processlist;

## 事务

```
select * from information_schema.innodb_trx;
```

## 索引相关

```sql
重建索引
alter table T engine=InnoDB

查看一个请求会用什么索引
explain <sql>

# 如何看一个请求扫描了多少行

# 如何看慢查询日志
```

## redo log 相关

```sql
如果对数据安全要求很高，innodb_flush_log_at_trx_commit 建议设置为 1，表示每次事务的 redo log 都直接持久化到磁盘，这样可以保证 MySQL 异常重启之后数据不丢失，即 crash-safe。
0: 每秒将存储引擎log buffer中的redo日志写入到log file，并调用sync将日志刷新到磁盘。
1：每次事务提交都将redo日志写入到log file，并调用sync将日志刷新到磁盘。
2：每次事务提交时，将log buffer中的redo日志写入log file，但是每秒调用sync操作写入磁盘。

查看 redo log 大小
show variables like 'innodb_log%';

修改 redo log 大小（修改my.cnf并重启）
innodb_log_file_size=1G

磁盘io能力
show variables like 'innodb_io_capacity';

脏页比例上限
show variables like 'innodb_max_dirty_pages_pct';

当前脏页比例计算 Innodb_buffer_pool_pages_dirty/Innodb_buffer_pool_pages_total，
可以通过 show engine innodb status 查看
show engine innodb status;

刷脏页的时候是否将“邻居脏页一起刷掉”，mysql 8.0 开始默认设为0了。
show variables like 'innodb_flush_neighbors';
```

## binlog 相关

```sql
sync_binlog=0 的时候，表示每次提交事务都只 write,不 fsync.
sync_binlog=1 的时候，表示每次提交事务都会执行 fsync.
sync_binlog=N(N>1) 的时候，表示每次提交事务都 write，但累积 N 个事务后才 fsync。
建议将**sync_binlog**设置为 1，这样每次事务的 binlog 都持久化到磁盘，保证 mysql 异常重启不丢 binlog。
完全的crash-safe需要将 innodb_flush_log_at_trx_commit 和 sync_binlog 都设为1，但这会让 IO 增多，性能变差。

查看binlog_cache_size。每次事务执行的时候，先写binlog cache，事务提交时将 cache，写入binlog file，之后再找时间写入磁盘。
show variables like 'binlog_cache_size';

mysql-bin.index 文件是所有 bin log 文件的列表

查看所有 binlog
show binary logs;

查看某一个 binlog 中的 events
show binlog events in 'mysql-bin.000001';

关闭当前使用的 binary log，然后打开一个新的 binary log 文件
flush logs;

查看是否打开 binlog
show variables like 'log_bin';

查看当前数据库 binlog 的位置
show master status;

获取指定位置的 binlog
show binlog events from 123;

a、提取指定的 binlog 日志
mysqlbinlog /opt/data/APP01bin.000001
mysqlbinlog /opt/data/APP01bin.000001|grep insert

/_!40019 SET @@session.max_insert_delayed_threads=0_/;
insert into tb values(2,'jack')

b、提取指定 position 位置的 binlog 日志
mysqlbinlog --start-position="120" --stop-position="332" /opt/data/APP01bin.000001

c、提取指定 position 位置的 binlog 日志并输出到压缩文件
mysqlbinlog --start-position="120" --stop-position="332" /opt/data/APP01bin.000001 |gzip >extra_01.sql.gz

d、提取指定 position 位置的 binlog 日志导入数据库
mysqlbinlog --start-position="120" --stop-position="332" /opt/data/APP01bin.000001 | mysql -uroot -p

e、提取指定开始时间的 binlog 并输出到日志文件
mysqlbinlog --start-datetime="2014-12-15 20:15:23" /opt/data/APP01bin.000002 --result-file=extra02.sql

f、提取指定位置的多个 binlog 日志文件
mysqlbinlog --start-position="120" --stop-position="332" /opt/data/APP01bin.000001 /opt/data/APP01bin.000002|more

g、提取指定数据库 binlog 并转换字符集到 UTF8
mysqlbinlog --database=test --set-charset=utf8 /opt/data/APP01bin.000001 /opt/data/APP01bin.000002 >test.sql

h、远程提取日志，指定结束时间
mysqlbinlog -urobin -p -h192.168.1.116 -P3306 --stop-datetime="2014-12-15 20:30:23" --read-from-remote-server mysql-bin.000033 |more

i、远程提取使用 row 格式的 binlog 日志并输出到本地文件
mysqlbinlog -urobin -p -P3606 -h192.168.1.177 --read-from-remote-server -vv inst3606bin.000005 >row.sql
```

## 数据插入与页分裂

除了删除数据，插入数据也会导致文件空洞。解决方法是**重建表**，下面这个操作会完成**新建表，转存数据，交换表名，删除旧表**等操作。

```
Alter table A engine=InnoDB
```

显然，花时间最多是往临时表插入数据。如果在这个过程中，有新的数据要写入，就会造成数据丢失。因此在这个 DDL 过程中，表 A 不能有更新。

但这就有点傻逼了。因此 Mysql 在 5.6 引入了 online ddl 优化。

```
1. 建立一个临时文件，扫码表A主键的所有数据页
2. 用数据页中表A的记录生成B+树，存到临时文件中
3. 将生成临时文件过程中的所有对A的操作记录记到一个日志文件(row log)中
4. 临时文件生成后，将日志文件中的操作应用到临时文件
5. 用临时文件替换表A的数据文件
```

**其实就是加入了日志记录与回放的功能。**

除此之外，**Online DDL 是要拿 MDL 写锁的，但是在开始拷贝数据前就退化成 MDL 读锁了**，这样就不会阻塞其他操作了。

对于很大的表来说，重建表操作很消耗 IO 和 CPU。推荐使用 gh-ost 来做。

## Online 和 Inplace

```
整个 DDL 都在 Innodb 内部完成，对于 server层 来说，这就是 inplace 的。
Alter table A engine=innodb;
等价于
Alter table A engine=innodb,ALGORITHM=inplace;
而与其对应的另一种方式就是拷贝表的方式了，这种方式就会采用非 online 的那种方式##。
Alter table engine=innodb,ALGORITHM=copy;
```

还需要注意一点，Online 一定是 inplace 的，但 inplace 不一定 online。比如给某个字段加全文索引可以是 inplace 的，但不 online
alter table t add FULLTEXT(field_name);

## Analyze 与 Optimize

除了 recreate 表(alter table t engine=innodb)外，还有常见的

```
analyze table t; --对表的索引信息做重新统计
Optimize table t; --recreate + analyze
```

## 如何查看现在 mysql 正在使用的隔离级别

```ß
select @@tx_isolation       当前会话隔离级别
select @@global.tx_isolation     全局隔离级别

设置隔离级别
set session transaction isolation level read committed;
set global transaction isolation level read committed;
```

innodb 存储两部分数据：表结构定义和数据。在 8.0 前，表结构数据存在.frm 文件中
innodb_file_per_table 配置，默认为 ON。一个表单独存一个文件更容易管理，而且在不需要这个表的时候，drop table 就可以删除这个文件了。

## 数据删除流程

删除数据的时候不会缩小磁盘空间，而是将这个数据标记为删除，如果之后有数据要写入到这个位置（和主键有关），则可以复用这块空间。

如果删除了整个数据页的数据，则整个数据页被标记为可复用。如果两个相邻的数据页都有大部分数据被标记为删除，则会把两个页面合并，并将其中空的那个标记为可复用。

如果我们用 delete 删除了整个表，则所有数据页都变成可复用，但磁盘文件不会变小。

**delete 只是把记录的位置或者数据页标记为可复用，但磁盘文件的大小是不变的。也就是说，delete 命令不能回收表空间。**
