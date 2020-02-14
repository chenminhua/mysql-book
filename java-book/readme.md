## final, finally, finalize

- final 修饰的 class： 不可继承扩展
- final 修饰变量： 不可修改。但 final 不是 immutable.
- final 修饰方法： 不可 override
- finalize 在垃圾回收前执行，不推荐使用，已被 java9 deprecated，会导致垃圾回收变慢。

## zero copy

![](https://static001.geekbang.org/resource/image/6d/85/6d2368424431f1b0d2b935386324b585.png)

而基于 NIO transferTo 的实现方式，在 Linux 和 Unix 上，则会使用到零拷贝技术，数据传输并不需要用户态参与，省去了上下文切换的开销和不必要的内存拷贝，进而可能提高应用拷贝性能。

![](https://static001.geekbang.org/resource/image/b0/ea/b0c8226992bb97adda5ad84fe25372ea.png)

## NIO Buffer

Buffer 是 NIO 操作数据的基本工具，Java 为每种原始数据类型都提供了相应的 Buffer 实现（布尔除外）.

![](https://static001.geekbang.org/resource/image/52/6e/5220029e92bc21e99920937a8210276e.png)

Buffer 有几个基本属性：

- capcity，也就是数组的长度。
- position，要操作的数据起始位置。
- limit，相当于操作的限额。在读取或者写入时，limit 的意义很明显是不一样的。比如，读取操作时，很可能将 limit 设置到所容纳数据的上限；而在写入时，则会设置容量或容量以下的可写限度。
- mark，记录上一次 postion 的位置，默认是 0，算是一个便利性的考虑，往往不是必须的。

前面三个是我们日常使用最频繁的，我简单梳理下 Buffer 的基本操作：

- 我们创建了一个 ByteBuffer，准备放入数据，capcity 当然就是缓冲区大小，而 position 就是 0，limit 默认就是 capcity 的大小。
- 当我们写入几个字节的数据时，position 就会跟着水涨船高，但是它不可能超过 limit 的大小。
- 如果我们想把前面写入的数据读出来，需要调用 flip 方法，将 position 设置为 0，limit 设置为以前的 position 那里。
- 如果还想从头再读一遍，可以调用 rewind，让 limit 不变，position 再次设置为 0。

## Direct Buffer 和垃圾收集

- Direct Buffer：Java 提供了堆内和堆外（Direct）Buffer，我们可以以它的 allocate 或者 allocateDirect 方法直接创建。

- MappedByteBuffer：它将文件按照指定大小直接映射为内存区域，当程序访问这个内存区域时将直接操作这块儿文件数据，省去了将数据从内核空间向用户空间传输的损耗。我们可以使用[FileChannel.map](https://docs.oracle.com/javase/9/docs/api/java/nio/channels/FileChannel.html#map-java.nio.channels.FileChannel.MapMode-long-long-)创建 MappedByteBuffer，它本质上也是种 Direct Buffer。

在实际使用中，Java 会尽量对 Direct Buffer 仅做本地 IO 操作，对于很多大数据量的 IO 密集操作，可能会带来非常大的性能优势。但是请注意，Direct Buffer 创建和销毁过程中，都会比一般的堆内 Buffer 增加部分开销，所以通常都建议用于长期使用、数据较大的场景。

使用 Direct Buffer，我们需要清楚它对内存和 JVM 参数的影响。首先，因为它不在堆上，所以 Xmx 之类参数，其实并不能影响 Direct Buffer 等堆外成员所使用的内存额度，我们可以使用下面参数设置大小：

    -XX:MaxDirectMemorySize=512M

这意味着我们在计算 Java 可以使用的内存大小的时候，不能只考虑堆的需要，还有 Direct Buffer 等一系列堆外因素。
另外，大多数垃圾收集过程中，都不会主动收集 Direct Buffer，它的销毁往往要拖到 full GC 的时候，所以使用不当很容易导致 OutOfMemoryError。对于 Direct Buffer 的回收，我有几个建议：

- 在应用程序中，显式地调用 System.gc()来强制触发。
- 另外一种思路是，**在大量使用 Direct Buffer 的部分框架中，框架会自己在程序中调用释放方法，Netty 就是这么做的（PlatformDependent0）**。
- 重复使用 Direct Buffer。

### object 类中的方法

clone, equals, hashCode, notify, notifyAll, 三个 wait，getClass, finalize
