当然我们也可以手动安装，教程在官网也有[安装教程](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/?_ga=1.65851438.1632872261.1435385597)
mongodb 的配置文件在/usr/local/etc/mongod.conf ##使用 mongo
在命令行启动 mongodb

```
mongod -config '/usr/local/etc/mongod.conf'
```

方便起见，我给这个命令起了一个别名：mongostart.启动后可以在浏览器上输入 localhost:27017 查看启动信息。
启动后，可以用**mongo**命令连接

```
db.version()        查看版本
db                  查看当前数据库
show dbs            查看有哪些数据库
use test            切换到test数据库下
show collections    查看当前数据库下的collections
db.user.insert()    在user表（collections）下插入文档
db.user.find()      查找数据
```

实例

```
use mydb
#但是现在我们show dbs发现mydb并不存在，如果你不对这个数据库进行操作的话，它就会被删掉，输入db发现还在mydb这个数据库。
show collections
#发现还没有表存在。
db.user.insert({name:"chen"})
现在我们再show dbs和show collections就没有问题了。
我再给这个表添加两个用户，名字将li和zhang。
db.usr.find()
查找一下名字叫做chen的用户
db.usr.find({name:"chen"})
```

