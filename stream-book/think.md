《Streaming system》本书比较抽象地讲了讲”流处理系统应该是什么样的“，可以作为系统设计时的参考。可以和 google 的 dataflow 论文结合着看。

为什么以前 storm 一片繁荣，但是面对 flink 败下阵来？如果直接对比功能特性，我们当然能列举出很多：window 啊、exactly-once 啊、event-time 啊。

框架的意义在于屏蔽底层细节，flink 由于支持 dataflow 模型，其抽象程度更高一些。

## 流 vs 批

流处理和批处理到底差别在哪里？

- 批处理的数据是已知的、不可变的，流处理的数据往往是未知的、实时输入的
- 流处理结果更实时，但相对并不准确，所以才会有所谓的 lambda 架构
- 流处理需要有 daemon 进程常驻
- 批处理往往是无状态的，而流往往是有状态的
- 因为没有状态，批处理的 failover 只要重跑就可，而流的错误处理会更麻烦
- 批处理由于能获取一些“全局”状态，可以做一些针对性优化，吞吐量更高
- 批处理的 join 实现已经比较完善了，而流的 join 一直是个大难题

但所有这些区别，更像是“结果”，是工程实现的差别，而不是本源。大家之所以觉得流处理系统不准确、吞吐量不高等等，只是因为它被实现成了那个样子。

本书最重要的一个理念，就是从更高的抽象层面，论证了批和流实际上是能统一的。我们不应该从工程实现的角度来分类，而应该从处理的问题域来划分。在真实的场景中，大多数数据其实都是无界（unbounded）+ 无序（unordered）的。很多我们用批处理系统（比如 MR）去处理的有界数据，其实是一种“劣化”。亲身经历的场景：

- late data 问题。以前用 MR 去计算各种报表，由于移动端的特殊性，上传必然是有延迟的。计算 T+1 报表也必然会少一部分数据，于是需要每天重跑过去 3 天的数据。为什么是 3 天呢，拍脑袋定的。。。日志延迟半个月都有可能，但重跑半个月之前的报表已经没啥意义了。
- session 计算问题。以前通过 MR 去计算 T+1 的 session，但用户的 session 很可能是跨天的，甚至可能跨几天。一般会多取几个小时的日志，但我也不知道应该多取多久的。只能“一刀切”：凌晨 2 点之后的日志全部不算在内。

从这个角度来讲，面对这种 unbounded 数据，批处理只能划分成一个个小的 batch 来处理，结果其实是不准确的。而流处理天生就考虑到了数据的无界性，理论上准确性应该是优于批的。

那为啥大家还会留下批处理结果准确、流处理结果不准确的印象嘞？这其实是两个层面的概念：**accuracy 和 completeness**。

- 批处理的“准确”，指的是计算的 accuracy，更多是系统层面：恒定的数据+恒定的计算逻辑=恒定的结果，就像不可变函数一样。即使这个最终结果不准确，也是计算逻辑或者数据的锅，而且误差也是相对恒定可接受的；
- 流处理的“准确”，指的是数据的 completeness，理论上能计算更准确的结果，但以前的各种流处理系统由于不能保证（或是实现代价很高）exactly-once，所以实际上算出来的可能不准。即使是同样的数据+同样的处理逻辑，你跑多次结果都可能是不一样的。。。但这不是流处理语义上的锅。

所以 stream 和 batch 更像是处理同一个问题的两种方式，真正的区别在于 latency 和 throughput，这是一种 trade-off

- latency：用 stream 的方式去处理时，你可以提前观察到结果，虽然这个结果可能不准，是一个提前观测甚至预测。但流处理语义保证当数据完整时结果是正确的（所谓的 refinements of results）。而用 batch 的方式去处理时，如果想要正确的结果，必须保证数据完整后才能开始计算。
- throughput：batch 方式吞吐量更高，因为有全局的数据，可以对 shuffle 做更多优化。而且 failover 简单，也就不需要持久化很多状态。而 stream 的方式需要提前计算结果，消耗更多资源，而且 failover 需要保存更多中间状态，所以吞吐相对没有 batch 高。

问题域统一后，流和批的 API 也是可以统一的（Dataflow/Beam）。
真正麻烦的在于引擎层面（或者说 runner），目前还没有一个很好的解，估计很长一段时间内也都很难统一。现阶段 Beam 这套 API，还是用于流处理更实际一点。即使 flink 宣称同时支持流和批，实际上批处理那套 API 也没啥人用。

## stream vs table

stream 和 table 是针对数据的两种视角，最直接的例子就是 mysql 的 binlog。

作者提出了 stream 和 table 的相关性（streams and tables are really just two different sides of the same coin）：

- Streams → tables：The aggregation of a stream of updates over time yields a table.
- Tables → streams：The observation of changes to a table over time yields a stream.
- Tables are data at rest.
- Streams are data in motion.

operation 会导致 stream 和 table 之间的变换，共有 4 种情况：

- stream → stream：nongrouping operation，或者说是对单个元素的处理（filter/map 等），很好理解，storm 等传统意义上的流处理都是针对的这种情况
- stream → table：grouping operation，或者说是需要 shuffle 的操作，shuffle 后每个 operator 需要保存一个 internal state，其实就是这个所谓的 table，典型的就是各种聚合（参考 spark 中的 stage 划分策略）
- table → stream：ungrouping operation，典型的就是 dataflow 中的各种 trigger
- table → table：不存在，所有对 table 的修改都是通过先 ungroup 再 group 实现的

关于 StreamSQL，本书中有专门的一章来讨论，作者描述了一种比较完善的流式 SQL 语义。其大概思想就是在传统的关系代数（RDBMS 的理论基础）中加上时间这一维度，用所谓的 TVR（Time-Varying Relations）来描述各种变换，进而扩展现有的 SQL 语法（前提是尽量精简，保证一个最小集）以支持流式处理。感觉上，有一点像数仓理论中的拉链表？表中的每条数据，其实都是有生命周期的。
不过作者也承认，这是一个比较理想的模型，现有的各种系统没有一个真正实现了这套完备的 SQL 语义。好像 ANSI 也在讨论流式 SQL 的标准，准备制定规范了？不知道最终的规范会是什么样。
