## 配置查看

mysql --help | grep my.cnf

当几个配置文件中包含同一个参数，mysql 会以最后一个配置文件中的参数为准。

## 总览全局

```
show processlist;
show global status;
show engine innodb status;
```

## 事务相关

```
select * from information_schema.innodb_trx;

## 如何查看现在 mysql 正在使用的隔离级别
select @@tx_isolation 当前会话隔离级别
select @@global.tx_isolation 全局隔离级别

设置隔离级别
set session transaction isolation level read committed;
set global transaction isolation level read committed;
```

## 锁相关

```sql
show global status like '%lock%';
Table_locks_waited/Table_locks_immediate=0.3% 如果这个比值比较大的话，说明表锁造成的阻塞比较严重
Innodb_row_lock_waits innodb 行锁，太大可能是间隙锁造成的

SHOW status like '%lock%';

SHOW engine innodb status;

查看表锁
SHOW OPEN TABLES where In_use > 0;

锁等待时间，默认是50s。
SHOW VARIABLES like 'innodb_lock_wait_timeout';

死锁检测是否开启
SHOW VARIABLES like `innodb_deadlock_detect`;

查锁
select * from information_schema.INNODB_LOCKS;

SHOW ENGINE INNODB STATUS; 看有没有死锁
或者查看 information_schema 下的表 INNODB_TRX, INNODB_LOCKS, INNODB_LOCK_WAITS 来观察锁的信息。

lock_id 锁 id
lock_trx_id 事务 id
lock_mode 锁的模式
lock_type 锁的类型，行锁还是表锁
lock_table 要加锁的表
lock_index 锁住的索引
lock_space 锁对象的 space id
lock_page 事务锁定页的数量，如果为表锁则为 NULL
lock_rec 事务锁定行的数量，如果为表锁则为 NULL
lock_data 事务锁定记录的主键值，如果为表锁则为 NULL
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

## order by 相关

排序可能在内存中完成，也可能需要使用外部排序，这取决于排序所需的内存和参数 sort_buffer_size。
如果排序需要的数据量小于 sort_buffer_size，排序就在内存中完成，但是如果排序数据量太久，内存放不下，就利用磁盘临时文件辅助排序。

可以从 number_of_tmp_files 中看到是否使用了临时文件，其表示排序过程中使用的临时文件数。如果 Mysql 担心排序内存太小，会影响排序效率，才会采用 rowid 算法，这样排序过程中一次可以排序更多行，但是需要回表取数据。

```sql
SHOW VARIABLES like 'sort_buffer_size';

/_ 打开 optimizer_trace，只对本线程有效 _/
SET optimizer_trace='enabled=on';

/_ @a 保存 Innodb_rows_read 的初始值 _/
select VARIABLE_VALUE into @a from performance_schema.session_status where variable_name = 'Innodb_rows_read';

/_ 执行语句 _/
select city, name,age from t where city='杭州' order by name limit 1000;

/_ 查看 OPTIMIZER_TRACE 输出 _/
SELECT * FROM `information_schema`.`OPTIMIZER_TRACE`\G

/_ @b 保存 Innodb_rows_read 的当前值 _/
select VARIABLE_VALUE into @b from performance_schema.session_status where variable_name = 'Innodb_rows_read';

/_ 计算 Innodb_rows_read 差值 _/
select @b-@a;
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

innodb_log_waits 值不等于 0 的话，表明 innodb log buffer 因为空间不足而等待
show status like 'innodb_log_waits';
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

Binlog Cache 使用状况，如果 Binlog_cache_disk_use 值不为 0 ，可能需要调大 binlog_cache_size 大小。
show status like 'Binlog_cache%';

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

## 表相关

```sql
临时表状况：Created_tmp_disk_tables/Created_tmp_tables 比值最好不要超过 10%，如果 Created_tmp_tables 值比较大，可能是排序句子过多或者是连接句子不够优化
show status like '%Created_tmp%';

表大小
SELECT TABLE_NAME, INDEX_LENGTH, DATA_LENGTH FROM information_schema.TABLES WHERE TABLE_NAME = 'table_name';
show table status like 'table_name';

SHOW variables like '%innodb_file_per_table%'; 如果为 on 则每个表有独立的表空间。回滚信息，插入缓冲索引，系统事务信息，二次写缓冲等等数据还是放在共享表空间中。

SHOW VARIABLES WHERE Variable_Name = "datadir"; 查看数据目录

ls -lh /var/lib/mysql/ibdata1 查看共享表空间大小
```

## Online DDL 和 Inplace DDL

删除数据的时候不会缩小磁盘空间，而是将这个数据标记为删除，并且让这个数据页可复用。注意，**数据页的复用跟记录的复用是不同的。**记录的复用只限于符合范围条件的数据。而页复用则可以复用到任何位置。如果相邻的两个数据页利用率都很小，系统就会把这两个页上的数据合到其中一个页上，另外一个数据页就被标记为可复用。如果我们用 delete 命令把整个表的数据删除呢？结果就是，所有的数据页都会被标记为可复用。但是磁盘上，文件不会变小。这些可以复用，而没有被使用的空间，看起来就像是**空洞**。

**delete 只是把记录的位置或者数据页标记为可复用，但磁盘文件的大小是不变的。也就是说，delete 命令不能回收表空间。**

除了删除数据，插入数据也会导致文件空洞。如果数据是按照索引递增顺序插入的，那么索引是紧凑的。但如果数据是随机插入的，就可能造成索引的**数据页分裂**。另外，更新索引上的值，可以理解为删除一个旧的值，再插入一个新值。不难理解，这也是会造成空洞的。。解决方法是**重建表**，下面这个操作会完成**新建表，转存数据，交换表名，删除旧表**等操作。

```
Alter table A engine=InnoDB
```

显然，花时间最多是往临时表插入数据。如果在这个过程中，有新的数据要写入，就会造成数据丢失。因此在这个 DDL 过程中，表 A 不能有更新。但这就有点傻逼了。因此 Mysql 在 5.6 引入了 online ddl 优化。**其实就是加入了日志记录与回放的功能。**

```
1. 建立一个临时文件，扫码表A主键的所有数据页
2. 用数据页中表A的记录生成B+树，存到临时文件中
3. 将生成临时文件过程中的所有对A的操作记录记到一个日志文件(row log)中
4. 临时文件生成后，将日志文件中的操作应用到临时文件
5. 用临时文件替换表A的数据文件
```

除此之外，**Online DDL 是要拿 MDL 写锁的，但是在开始拷贝数据前就退化成 MDL 读锁了**，这样就不会阻塞其他操作了。对于很大的表来说，重建表操作很消耗 IO 和 CPU。推荐使用 **gh-ost** 来做。

Inplace 是对于 server 层的概念。如果 DDL 的临时表是 server 层创建的，则不是 Inplace 的，如果是存储引擎创建的，则是 Inplace 的。

```
Alter table A engine=innodb; 等价于
Alter table A engine=innodb,ALGORITHM=inplace;

而与其对应的另一种方式就是拷贝表的方式了，这种方式就会采用非 online 的那种方式。
Alter table engine=innodb,ALGORITHM=copy;

Online 一定 inplace ，但 inplace 不一定 online。比如给字段加全文索引可以是 inplace 的，但不 online，这个过程是 inplace 的，但会阻塞增删改操作，是非 Online 的。
alter table t add FULLTEXT(field_name);
```

## Analyze 与 Optimize

除了 recreate 表(alter table t engine=innodb)外，还有常见的

```
analyze table t; --对表的索引信息做重新统计
Optimize table t; --recreate + analyze
```

# 指标

## TPS,QPS 统计

```
QPS:每秒请求数
TPS:每秒事务处理数
SHOW GLOBAL STATUS LIKE 'com_commit'\G; 只显示显式的提交和回滚
show global status like 'com_rollback'\G;
show global status like 'handler_commit'\G; 显示显式的和隐式的提交和回滚
show global status like 'handler_rollback'\G;

com_commit = show global status like 'com_commit';
com_rollback = show global status like 'com_rollback';
uptime = show global status like 'uptime';
questions = show global status like 'questions';
qps = questions / uptime;
tps=(com_commit + com_rollback) / uptime;
方法二
show global status where variable_name in('com_select','com_insert','com_delete','com_update');
```

## innodb buffer 命中率

```
Innodb_buffer_pool_read_requests 表示 read 请求的次数，
Innodb_buffer_pool_reads 表示从物理磁盘中读取数据的请求次数，

所以 innodb buffer 的 read 命中率就可以这样得到：
（Innodb_buffer_pool_read_requests - Innodb_buffer_pool_reads） / Innodb_buffer_pool_read_requests

一般来讲这个命中率不会低于 99%，如果低于这个值的话就要考虑加大 innodb buffer pool。
show variables like "%innodb_buffer_pool_size%"
```

## Table Cache 状态量

```
mysql> show global status like 'open%';
比较 open_tables 与 opend_tables 值
Open_tables ：代表当前打开表的数量。
Opened_tables：代表自从 MySQL 启动后，打开表的数量。
对于 innodb 存储引擎，开启表的独立表空间（innodb_file_per_table）打开 1 张表只需要 1 个文件描述符（一个.ibd 文件）。
Open_files ：代表当前打开的文件。对应存储引擎（如：innodb）使用存储引擎自己内部函数打开的话，这个值是不会增加的。
Opened_files：代表使用 MySQL 的 my_open()函数打开过的文件数。如果不是使用这个函数打开文件的话，这个值是不会增加的。
```

### Thread Cache 命中率

```
mysql> show global status like 'Thread%';
mysql> show global status like 'Connections';
Thread_cache_hits = (1 - Threads_created / connections ) \* 100%
```

### 复制延时量

mysql > show slave status

## 为啥即使有索引，有时候简单的查询也会很慢很慢？

遇到这种情况先 show processlist; 看下

1. 等锁，比如等 mdl 写锁。这时候一般先把 mdl 锁对应的连接 kill 掉。
   select blocking_pid from sys.schema_table_lock_waits;

2. 等 flush。flush 会关闭打开的表。通常来说，flush 都很快，除非，它们被堵住了。所以解决方案是找出堵住 flush 的操作。

```
flush table t with read lock;
flush tables with read lock;
```

3. 等行锁，先查下是谁占着行锁。

```
select * from t sys.innodb_lock_waits where locked_table=`'test'.'t'`\G
```
