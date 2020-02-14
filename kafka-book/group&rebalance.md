提升了消费端的吞吐。Consumer Group 共享一个 Group ID，组内所有消费者协调在一起来消费订阅的 Topic 的所有分区。每个分区只能由同一个消费者组内的一个 Consumer 来消费。

**理想情况下 Consumer 实例数应该等于该 Group 订阅主题的分区数**。假设一个 Consumer Group 订阅了 3 个主题，分别是 A,B,C, 它们的分区数依次是 1,2,3， 通常为该 Group 设置 6 个 consumer 是比较理想的。如果你设置的 consumer 实例数超过了分区数，比如说 8 个，那么其中两个 consumer 不会被分配任何分区。

## Consumer Group 如何管理 offset

通过一组 kv 来管理，Key 是分区，V 对应消费到的最新位移。采用了内部主题 \_consumer_offsets 来保存位移，类似 Map<TopicPartition, Long>这样的结构。这个位移称为消费者位移，区别于分区位移。

协调者（coordinator）专门为 consumer group 服务，负责为 group 执行 rebalance 以及提供位移管理和组成员管理等。具体来说，Consumer 提交位移的时候，其实是向 Coordinator 所在的 broker 提交位移。当 Consumer 启动的时候，也是向 Coordinator 所在 broker 发送请求，然后由 coordinator 负责执行消费者组的注册、成员管理等。所有 broker 启动时都会创建和开启相应的 coordinator 组件。

Consumer Group 如何确定为它服务的 coordinator 在哪个 broker 呢？答案就在 \_consumer_offsets 上。

第一步，确定由位移主题的哪个分区来保存 group 数据。

```
partitionId=Math.abs(groupId.hashCode() % offsetsTopicPartitionCount)
```

第二步，找出该分区 leader 副本所在的 broker，该 broker 就是 coordinator。在实际使用过程中，Consumer 应用程序，能够自动发现并连接正确的 Coordinator。当 Consumer Group 出现问题，我们能够根据这个算法准确定位 Coordinator 对应的 Broker。

## Rebalance

当组内成员发生变化，订阅主题数发生变化，订阅主题分区数发生变化等情况发生时，rebalance 就会发生。此时 Group 下所有 Consumer 会协调在一起共同参与。Rebalance 的过程对消费过程有很大影响。所有 Consumer 都会停止消费，并且涉及到连接等大量资源的回收与重建。曾有过 Group 内有几百个 Consumer 实例，成功 Rebalance 一次要几个小时！

Rebalance 慢和影响 TPS 的问题，目前无解。我们应当减少 group 下实例数减少导致的 rebalance。

Coordinator 会在什么时候认为某个 consumer 实例挂了从而要求退组呢？当 Consumer Group 完成 Rebalance 后，每个 Consumer 都会定期向 Coordinator 发送心跳。有个参数 session.timeout.ms 就是用来干这个的，默认是 10s,即 coordinator 在 10s 内没有收到 Group 下某 Consumer 的心跳，它就认为这个 Consumer 已经挂了。

Consumer 还提供了一个允许你控制发送心跳请求频率的参数，就是 heartbeat.interval.ms。目前 coordinator 通知各个 consumer 实例开启 rebalance 的方法就是将 rebalance_needed 标志封装进心跳请求的响应中。

Consumer 还有一个 max.poll.interval.ms 参数用于限定 Consumer 端应用程序两次调用 poll 方法的最大时间间隔，默认是 5 分钟。表示如果 Consumer 程序如果在 5 分钟内无法消费完 poll 方法返回的消息，Consumer 会主动发起“离开组”的请求。

推荐设置

```
session.timeout.ms = 6s
heartbeat.interval.ms = 2s
```

确保 Consumer 被踢出前至少能发送 3 轮心跳请求。

此外我们还应该避免由于 Consumer 消费时间过长导致 Rebalance，可以考虑将 max.poll.interval.ms 调大。

如果还是出现了意料之外的 Rebalance，建议你去排查一下 Consumer 端的 GC 表现，比如是否出现了频繁的 Full GC 导致的长时间停顿，从而引发了 Rebalance。为什么特意说 GC？那是因为在实际场景中，我见过太多因为 GC 设置不合理导致程序频发 Full GC 而引发的非预期 Rebalance 了。
