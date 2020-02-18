http://jolestar.com/etcd-architecture/

# etcds

Etcd is a distributed, consistent key-value store for shared configuration and service discovery

## Etcd 能提供什么能力？

提供存储以及获取数据的接口，利用 raft 协议保证一致性。
提供监听机制，客户端可以监听某些 key 的变更。
提供 key 的过期和续约机制，客户端通过定时刷新来实现续约，用于集群监控和服务注册发现。
提供原子的 CAS（compare-and-swap）和 CAD(compare-and-delete)，用于分布式锁和 leader 选举

## Etcd 是如何实现一致性的？

raft 协议
raft 的时钟周期和超时机制
raft 的日志同步机制（一致性是通过同步 wal 日志来实现的）
golang csp 并发模型

## Etcd 的存储是如何实现的？

Etcd 的 watch 机制是如何实现的？
Etcd 的 key 过期机制是如何实现的？

go get github.com/coreos/etcd/clientv3
