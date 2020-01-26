zk 是一个分布式数据一致性的解决方案。分布式应用可以基于它实现数据发布订阅，负载均衡，命名服务，分布式协调通知，集群管理，master 选举，分布式锁，分布式队列等。

**顺序一致性，原子性，单一视图，可靠性。适用于读多的场景。**

- Zk 没有使用 master/slave，而是引入了 leader，follower，observer 三种角色。
- 只有 leader 提供写服务，其他只能提供读服务。
- Observer 不参与选举，可以在不影响写性能的情况下提升集群的读性能。

- 客户端和服务端间有 TCP 长连接，连接建立后，客户端和服务端间通过心跳检测保持有效会话。
- sessionTimeout 用来设置客户端会话超时时间。

### ZNODE

ZK 将数据都存在内存里，数据模型是一棵树。znode 可以分为临时节点和持久节点。临时节点的生命周期和客户端会话绑定，会话失效后 znode 就会被移除。

对应每个 znode，zk 都会为其维护一个叫 stat 的数据结构，里面记录这三个数据版本: version, cversion, aversion。

### Watcher

Zk 允许用户在指定节点上注册一些 watcher，在一些特定事件发生时，服务端会通知客户端。

### ACL

zk 采用 ACL 策略来进行权限控制，类似 UNIX 文件系统的权限控制。CREATE, READ, WRITE, DELETE, ADMIN。

### ZAB 协议

Zk 没有采用 paxos 算法，而是采用了 zookeeper atomic broadcast 的协议作为其数据一致性的核心算法。

zab 协议的核心： 所有事务请求都要由一个全局唯一的服务器协调处理（leader 服务器），而余下的其他服务器则成为 follower 服务器。leader 服务器负责将一个客户端事务请求转换成一个 proposal，并将其分发给集群中所有 follower 服务器。之后 leader 服务器要等待 follower 反馈，一旦超过半数 follower 发回正确 ack，leader 就会再次向所有 follower 发送 commit 消息，要求将前一个 proposal 进行提交。

### 协议两大模式: 崩溃恢复和消息广播

## zk 使用方式

```
# 配置
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
initLimit=5
syncLimit=2
server.1=IP1:2888:3888
server.2=IP2:2888:3888
server.3=IP3:2888:3888
```

测试一下 zk 集群 telnet IP1 2181。可以看到 MODE 里面有 leader 或者 follower，如果是单机模式的话就是 standalone

```
zkServer.sh start
```

#### 客户端脚本

zkCli.sh -server ip:port

```
create [-s] [-e] path data acl 创建
ls path [watch] 读取
get path [watch] 获取指定节点的数据和属性
set path data [version] 更新
delete path [version] 删除，注意，要删除某个节点，该节点必须没有子节点
create /zk-book 123
ls /
get /zk-book
set /zk-book 456
delete /zk-book
```

#### java 客户端

同步调用和异步调用。同步调用是需要抛出异常的，并且是阻塞的，而异步调用则需要使用 callback，调用本身不会抛出异常。
除了官方客户端外，还可以使用 zkclient, curator 等。看起来 curator 的 contributors 更多也更活跃，stars 也更多一点。

#### 更新与 CAS

zookeeper 的 setData 接口中的 version 参数正式基于 CAS 原理演化来的。
假如一个客户端需要对某个节点进行更新，它会携带上次获取到的 version 值进行更新，如果这个值被其他客户端提前更新了，数据版本就会变化，更新也会失败。

# zk 使用场景

## pub/sub

zk 采用推拉结合的方式：客户端向服务端注册自己需要关注的节点，一旦该节点的数据发生变化，服务端就会向相应的客户端发送 watcher 事件通知，客户端收到通知后，需要主动到服务端获取最新数据。（**Push you to pull**）
应用系统开发中，常常会有这样的需求，系统中要使用一些通用的配置，例如数据库配置信息，运行时开关配置等等。
我们希望能够做到快速的全局配置中心。
一般情况下，我们可以在 zk 上选取一个数据节点用于配置存储，例如 /configserver/app1/database_config，我们将数据库配置信息写入到这个 znode 中去。
集群中每台机器初始化时，首先从上面的 zookeeper 配置节点上读取数据库信息，同时，客户端还要在配置节点上注册一个数据变更的 watcher 监听，一旦节点数据发生变化，所有订阅的客户端都能获取数据变更通知。
客户端在接到通知后，进行数据库切换。

## 负载均衡

基于 zk 实现的动态 DNS 方案（DDNS）。
首先，我们可以在 /DDNS/app1/server.app1.company1.com 上创建一个节点来进行域名配置。给这个 znode 上写入几个 ip:port。
当域名解析发生变化时，可以告知其他所有订阅者，订阅者知道后，可以再次进行域名配置的获取操作。
Register 负责域名的动态注册
Dispatcher 负责域名的解析
Scanner 负责检测以及维护服务状态（探测服务可用性，屏蔽异常服务等）
SDK 负责各种语言的系统接入协议，提供服务注册以及查询接口。
Monitor 负责收集服务信息以及对 DDNS 自身状态的监控。
Controller 是一个后台管理的 Console。

## 命名服务

命名服务是分布式系统最基本的一项公共服务之一。
/jobs/type/{job-0000000001, job-0000000002, ...}

## 分布式协调通知

## 集群管理

## Master 选举

客户端集群每天定时往 zk 上创建一个临时节点，在这个过程中，只有一个客户端能成功，它就成了 master 节点。而其他节点就在这个 znode 上注册一个 watcher。用于监控当前 master 机器是否还活着，如果 Master 挂了，那么其余客户端将会重新进行 master 选举。

## 分布式锁

#### 一种简单的实现

排他锁： 试图创建一个 znode,创建成功的那个节点获得锁，其他的客户端注册一个 watcher 监听，当发现锁被释放后，其他节点可以再来竞争锁。
共享锁： 类似/shared_lock/host1-R-0000000001,/shared_lock/host1-W-0000000002，在需要获取锁的时候，所有客户端都去/shared_lock 下面创建一个临时顺序节点。然后关注/shared_lock 下面所有子节点的变化。
对于读，如果比自己序号小的都是读请求，则可以开始读取逻辑；如果比自己小的有写请求，则需要等待。
对于写请求，只要有比自己序号小的请求，就要等待。
这种实现可能导致羊群效应，在集群规模较大时可能导致灾难。

#### 改进版本

每个锁竞争者，只需要关注/shared_lock 节点下序号比自己小的节点就可以了。

#### 分布式队列与分布式屏障（barrier）

## zk 在 hadoop 中的应用

在 Hadoop 中，zk 主要用于实现 HA,HDFS 的 NameNode 和 YARN 的 ResourceManager 都是基于 HA 模块来实现的。
