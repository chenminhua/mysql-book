## 时间

DATETIME, 8 字节 1999-01-01 12:12:12
DATE, 3 字节 1999-01-01
TIMESTAMP 4 字节 实际存储内容为 1970-01-01 00:00:00 到当前的毫秒数
YEAR, 1 字节
TIME, 4 字节

NOW() 等价于 CURRENT_TIMESTAMP 返回执行 sql 时的时间
SYSDATE() 返回执行此函数的时间
DATE_ADD(), DATE_SUB() 时间加减
DATE_FORMAT() 函数

SELECT NOW(), SYSDATE(), SLEEP(2), NOW(), SYSDATE()
SELECT NOW() as now, DATE_ADD(now(), INTERVAL 1 DAY) AS tomorrow, DATE_SUB(now(), INTERVAL 1 DAY) as yesterday;
SELECT DATE_FORMAT(NOW(), '%Y%m%d') as datetime;

## 字符

SHOW CHARSET 查看 mysql 支持的字符集。 默认为 latin1。最好用 utf8

unicode != utf8。unicode 是字符编码，utf8 是字符集。

对于 unicode 编码的字符集，强烈建议将所有的 char 字段设置为 varchar，因为对于 char，数据库会保存最大可能的字节数。例如，对于 char(30)，数据库会存 90 个字节。

SHOW COLLATION; 可以查看字符排序规则。比如
SHOW COLLATION LIKE 'gbk%'\G;
SET NAMES utf8 COLLATE utf8_bin; 设置 utf8 的大小写敏感。
ALTER TABLE t MODIFY COLUMN a VARCHAR(10) COLLATE utf8_bin;

## Char vs varchar

CHAR 定长，自动 right padding。CHAR(N)注意 N 为字符数，而不是字节数。
SELECT @a:='mysql 技术内幕';
SELECT @a, HEX(@a), length(@a), char_length(@a);

VARCHAR 变长，存储时需要增加前缀存储长度。

## 逻辑查询与物理查询

```
(8) SELECT (9) DISTINCT<select_list>
(1) FROM <left_table>
(3) <join_type> JOIN <right_table>
(2) ON <join_condition>
(4) WHERE <where_condition>
(5) GROUP BY <group_by_list>
(6) WITH {CUBE|ROLLUP}
(7) HAVING <having_condition>
(10) ORDER BY <order_by_list>
(11) LIMIT ...;

CREATE TABLE customers(
  customer_id VARCHAR(10) NOT NULL,
  city VARCHAR(10) NOT NULL,
  PRIMARY KEY (customer_id)
) ENGINE =InnoDB;

CREATE TABLE orders (
  order_id INT NOT NULL AUTO_INCREMENT,
  customer_id VARCHAR(10),
  PRIMARY KEY (order_id)
) ENGINE = InnoDB;

查询来自杭州并且订单数小于2的客户，列出他们的订单数，并按照订单数从大到小排列
SELECT c.customer_id, count(o.order_id) as total_orders FROM customers AS c LEFT JOIN orders AS o on c.customer_id = o.customer_id where c.city = 'HangZhou' GROUP BY c.customer_id HAVING count (o.order_id) < 2 ORDER BY total_orders DESC;

第一步是先将customers表和orders表做一个笛卡尔积，（28行）
第二步是进行ON c.customer_id = o.customer_id 过滤 (6行)
第三步是添加外部行，这只有在OUTER JOIN中才会发生，OUTER可以省略 （7行）
第四步进行WHERE 过滤，（4行）
第五步进行分组  GROUP BY c.customer_id （3行）
第六步HAVING count (o.order_id) < 2 (2行)
第七步处理SELECT
第八步处理DISTINCT
第九步排序，
第十步分页
```
