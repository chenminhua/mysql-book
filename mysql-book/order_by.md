```sql
CREATE TABLE `t` (
  `id` int(11) NOT NULL,
  `city` varchar(16) NOT NULL,
  `name` varchar(16) NOT NULL,
  `age` int(11) NOT NULL,
  `addr` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city` (`city`)
) ENGINE=InnoDB;

假设你要查城市是杭州的所有人名字，并按照名字排序返回前1000人的姓名和年龄。
explain select city,name,age from t where city='杭州' order by name limit 1000 ;
```

主要 Extra 这个字段中的 “Using filesort”表示的就是需要排序，Mysql 会给每个线程分配一块内存用于排序，称为 sort_buffer。执行过程如下

```
初始化sort_buffer， 确定放入name，city，age三个字段；
从索引city找到第一个满足条件的主键id，也就是ID_X。
到主键索引中取出整行，取name,city,age放入sort buffer。
重复上面两步，将满足city查询条件的数据不停放入sort buffer。
对sort buffer中的数据按照name进行排序。
按照排序结果取前1000行返回给客户端。
```

其中按 name 排序这一步，可能在内存中完成，也可能需要使用外部排序，这取决于排序所需内存和 sort_buffer_size 的大小。如果 sort_buffer_size 不够大的话，就会利用磁盘临时文件辅助排序。

### rowid 排序

上面的算法有个问题，就是如果单行很大的话，都查到 sort buffer 里面很亏啊。
SET max_length_for_sort_data = 16;

Max_length_for_sort_data 是专门控制用于排序的行数据长度的一个参数。意思是，如果单行数据超过这个值，mysql 就会换一个算法。
此时新的算法放入 sort_buffer 的字段就只有要排序的列和主键了。

### 全字段排序 vs Rowid 排序

如果 mysql 认为内存足够大，会优先使用全字段排序，把需要的字段都加入 sort buffer。
那是不是所有的 order by 都需要用到 sort buffer 呢？ 不是的！

还是上面的例子，如果我们有一个 city-name 的索引的话，从索引上取出来的就是按照 name 递增的，就不用再排序了。
