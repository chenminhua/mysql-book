# rabbitMQ

AMQP： 高级消息队列协议

## 理解消息通信

生产者创建消息，然后发布到代理服务器。消费者连接到代理服务器，并订阅到队列上。
消息包括了 label 和 payload
应用程序和 rabbit server 之间有一条 tcp 连接，一旦 tcp 连接打开，应用程序就可以创建一条 channel(一个虚拟连接),每个 channel 都会有一个唯一的 ID。引入 channel 的概念是为了减少 tcp 连接的巨大开销，同时保证各个线程的独立性。

#### 队列

如果有至少一个消费者订阅了队列，消息会立刻发给消费者。
如果没有人订阅队列，消息会在队列中等待。
如果有多个消费者订阅了同一个队列，消息会发给其中的一个消费者(round robin)。
消费者对消息的读取进行 ack 后，rabbit 会删除这条消息。消费者可以选择 auto_ack，或者手动 ack。
消费者可以拒收一条消息。

#### exchange

队列通过 routing key 绑定到 exchange。why?
exchange 共有四种类型：direct, fanout, topic, headers。
direct exchange：如果路由键匹配的话，消息就被投递到对应的队列。
fanout exchange：将收到的消息广播到绑定的队列上。消息通信模式很简单：将消息投递到所有附加在此 exchange 上的队列。
topic exchange：使得不同源头的消息能够到达同一个队列。

rabbitmqctl list_bindings

#### 多租户模式：虚拟主机与隔离

每个 vhost 本质上是一个 mini 版的 rabbitMQ 服务器，它拥有自己的权限机制。

#### 持久化

消息的投递模式(delivery mode)设置为 2；
exchange 设为持久化(durable 为 true)
队列设为持久化(durable 为 true)

rabbitmq 会把消息写入磁盘上一个持久化日志文件。
当发布一条持久性消息到持久 exchange 上时，rabbit 会在提交到日志文件后才发送响应。
一旦你消费了一条持久性消息，rabbitmq 会把这条消息标记为等待垃圾回收。
如果 rabbitmq 重启的话，服务器会自动重建 exchange 和队列，重播持久性日志文件上的消息到合适的队列或者交换机上。

#### AMQP 事务

## 运行和管理 rabbitMQ

如何干净利落地停止 rabbitmq？
如何限制 rabbitmq 的内存消耗？
权限控制

#### 服务器管理

erlang 也有虚拟机，而虚拟机的每个实例称为 node。
干净地关闭 rabbit: rabbitmqctl stop
停止和启动 rabbit(不关闭 erlang 节点): rabbitmqctl stop_app/start_app

#### 配置 rabbitmq

/etc/rabbitmq/rabbitmq.config

#### 权限管理

```
rabbitmqctl add_user bigtom 1234qwer
rabbitmqctl delete_user bigtom
rabbitmqctl list_users
rabbitmqctl change_password bigtom 12345678

读、写、配置权限
rabbitmqctl set_permissions bigtom ".*" ".*" ".*"
rabbitmqctl list_user_permissions bigtom
```

#### 检查

rabbitmqctl list_queues name messages consumers memory durable auto_delete
rabbitmqctl list_exchanges name type durable auto_delete
rabbitmqctl list_bindings

#### 日志

rabbit.log
rabbit-sasl.log

## cluster

允许消费者和生产者在 rabbit 节点崩溃的情况下继续运行；可以通过添加更多节点来线性扩展消息通信的吞吐量。
当一个 rabbit 集群节点崩溃时，该节点上队列的消息也会消失。

在单一节点内，rabbitmq 会把所有信息存储在内存中，同时将那些标记为可持久化的信息存储在硬盘上。存储在硬盘上的数据可以在重启节点时重新创建。
默认情况下，rabbitmq 不会将队列内容和状态复制到所有的节点上去。

## recover from failure

## fail over and replication

## web admin

## rest api

## monitor

## performance and security

## extension
