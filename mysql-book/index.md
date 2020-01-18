在 innodb 中表都是根据主键索引形式存放的，称为索引组织表，每个索引都是 B+树。

### 前缀索引怎么加，有啥用

```
前六个字符做索引
alter table SUser add index index2(email(6));
```

前缀索引的好处是其占用空间更小，并且这样在一个数据页上能放下的索引节点也就更多，搜索效率就更高。（缺点是可能导致扫描更多的行，并且没有覆盖索引的优化可用）

如何确定我该使用多长的前缀呢？建立索引关注的是区分度，区分度越高越好。因此可以通过统计索引上有多少不同的值来判断用多长的前缀。

```
select count(distinct email) as L from user;
select count(distinct left(email, 4)) as L4,
       count(distinct left(email, 5)) as l5,
       count(distinct left(email, 6)) as l6,
       count(distinct left(email, 7)) as l7 from user;
```

### 如何重建索引？

```
alter table T engine=InnoDB
```

### 采用自增 id 做主键有什么好处？

首先，如果不是自增主键的话，插入新数据的时候如果插入到中间的某个数据页上（前后都有数据），就需要在逻辑上挪动后面的数据，如果数据页已经满了，还会导致页分裂。

其次，由于自增主键还是普通索引的叶子节点，所以主键所占的空间越小越好。通常自增主键都是一个长 int，占用空间较小。

### 如何看一个请求会用什么索引

```
explain <sql>
```

### 如何看一个请求扫描了多少行

### 如何看慢查询日志

### 覆盖索引是啥

覆盖索引是一种通过建立联合索引以避免回表的手段，假设你有一个高频 sql，需要根据某个索引字段 a 查到另一个字段 b，可以考虑建立一个 a-b 联合索引，这样就可以直接从辅助索引上拿到要返回的全部数据，避免了回表。

### 最左前缀

建立联合索引的时候我们要考虑索引的复用能力，比如我们需要一个 a 索引，也需要一个 a-b 索引，但不需要 b 索引这时候我们就只用建立 a-b 索引了。

### 索引下推是啥

索引下推是 mysql5.6 引入的特性。比如我们有个 user 表，然后有一个 name-age 的索引，我们进行下面的请求。

```
select * from user where name like '张%' and age=10;
```

如果没有索引下推的话，请求只能在 name-age 索引上找到所有姓张的人的 id，然后回表到主键上一个一个查出 user 并比较 age 是否满足。但有了索引下推之后，就可以在变量 name-age 索引的时候直接判断是否满足 age=10，不满足的就直接不用回表了。

### (Change buffer)用普通索引还是唯一索引

由于身份证号字段比较大，做主键不太好。那么你可以给身份证号字段创建唯一索引，要么创建一个普通索引。那么从性能的角度考虑，你应该建唯一索引还是普通索引呢？

从查询角度看，对于唯一索引来说，查到第一条记录查询就结束了；而对于普通索引来说，还要多查下一个记录。但是因为 Innodb 是页为单位读写的，而页的默认大小为 16k，所以这两种索引在查询上的差距微乎其微。

从更新过程来看，如果要更新的数据在内存里了就直接更新；如果不在的话，Innodb 会先将更新操作写入 change buffer，下次查到这个数据页的时候，执行 change buffer 中的操作（这个操作叫做 merge，后台也会定期 merge），好处是更新的时候可以不用读磁盘。(Change buffer 在内存中有拷贝，也会被写入到磁盘上)

但是，如果你更新的是唯一索引的话，因为需要判断这个操作有没有违反唯一性约束，就不能用 change buffer 了。

Change buffer 的大小可以通过 innodb_change_buffer_max_size 来动态设置，这个参数设置为 50，表示 change buffer 的大小最多为 buffer pool 的 50%.

对于写多读少的业务，使用 change buffer 比较划算；如果是写完就会读的业务，change buffer 就没啥用了。

## change buffer 和 redo log

```
insert into t(id, k) values(id1, k1), (id2, k2);
```

假设我们查到插入位置后，k1 所在的页在内存中，K2 所在的页不在内存中。这条语句更新了四个部分：内存、redo_log（ib_log_fileX），数据表空间(t.ibd)，系统表空间(ibdata1)。

而事实上，当时这条语句做了如下操作。

1. Page1 在内存中，直接更新内存
2. Page2 没有在内存中，先写 change buffer，记录下“我要在 page2 插入一行”。
3. 将上述过程计入 redo log

这个操作就写了两处内存，一处磁盘(redo log)。

redo log 主要是节省随机写磁盘的 IO 消耗（转成顺序写），而 change buffer 则是节省随机读的 IO 消耗。