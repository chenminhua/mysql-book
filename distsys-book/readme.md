分布式系统的特点： 分布性，对等性，并发性，缺乏全局时钟，故障总会发生

分布式系统环境问题： 通信异常，节点故障，网络分区，三态问题。

BASE: basically available, soft state and eventually consistent。 基本可用，软状态，最终一致。

- 基本可用：响应时间上的损失，功能上的损失。
- 弱状态：允许系统在不同节点的副本间同步数据过程中存在延时。
- 最终一致：系统中所有副本在经过一段时间同步后，最终能够达到一致的状态。

## 一致性协议

2PC, 先准备后提交。

2PC 的缺点：1. 同步阻塞，2. 存在单点，如果有人没收到提交请求，则还是会有数据不一致问题。

3PC, CanCommit -> PreCommit -> Commit

Paxos, 1990 年由 leslie lamport（2013 年图灵奖得主） 提出。拜占庭将军问题。《Paxos made simple》。
在古希腊有个叫 paxos 的岛，岛上采用议会形式来通过法令，议员们通过信使来传递消息。议员和信使都可能随时离开，并且信使可能传递重复的消息或丢弃消息。

Raft

## chubby: paxos 的工程实践

chubby 是 google 推出的分布式锁服务，GFS 和 Big Table 等大型系统都用它来解决分布式协作，元数据存储和 master 选举等问题。

《the chubby lock service for loosly-coupled distributed systems》

通过投票选举产生一个获得过半投票的服务器为 master，一旦产生了 master，chubby 就会保证在这段时间内不会再有其他服务器成为 master，这段时间称为租期（master lease）。

在运行过程中，master 会不停通过续租的方式来延长租期，如果 master 服务器出现故障，就会发生新一轮的 Master 选举。

集群中每个服务器都维护一个副本，但是只有 master 有权利 update，其他服务器只能从 master 同步更新。

chubby 客户端只和 master 进行通信，所有请求都发到 master,针对写，master 会广播给其他服务器，而读则由 master 亲自搞定。

## Quorum 机制： 过半机制
