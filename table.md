innodb 存储两部分数据：表结构定义和数据。在 8.0 前，表结构数据存在.frm 文件中
innodb_file_per_table 配置，默认为 ON。一个表单独存一个文件更容易管理，而且在不需要这个表的时候，drop table 就可以删除这个文件了。

## 数据删除流程

删除数据的时候不会缩小磁盘空间，而是将这个数据标记为删除，如果之后有数据要写入到这个位置（和主键有关），则可以复用这块空间。

如果删除了整个数据页的数据，则整个数据页被标记为可复用。如果两个相邻的数据页都有大部分数据被标记为删除，则会把两个页面合并，并将其中空的那个标记为可复用。

如果我们用 delete 删除了整个表，则所有数据页都变成可复用，但磁盘文件不会变小。

**delete 只是把记录的位置或者数据页标记为可复用，但磁盘文件的大小是不变的。也就是说，delete 命令不能回收表空间。**

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
