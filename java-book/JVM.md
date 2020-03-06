class 文件先加载到 jvm，加载后的 java 类会被放在方法区(method area)。实际运行时，虚拟机会执行方法区中的代码。

调用方法会在当前线程的方法栈中生成一个栈帧，用于存放局部变量以及字节码的操作数。退出当前执行方法时，不管是正常返回还是异常返回，jvm 都会弹出当前线程的当前栈帧。

从硬件视角看，jvm 要将字节码翻译成机器码，可以解释执行，也可以 JIT 编译。hotspot 默认采用混合模式。理论上，java 执行效率是可能超过 c++的，因为 JIT 编译比静态编译拥有更多的运行时信息，并据此优化。

hotspot 内置了多个即使编译器：C1, C2, Graal 等。从 java7 开始，hotspot 采用分层编译，先用 c1 进行简单的编译优化，如果是热点中的热点，则进行 c2 编译优化。为了不干扰应用的正常运行，HotSpot 的即时编译是放在额外的编译线程中进行的。

## 基本类型

- boolean, byte, char, short, int, long, float, double
- boolean 在 jvm 中被映射为整数，true -> 1, false -> 0。

| 类型    | 范围            | 默认值   | 虚拟机内部符号 |
| ------- | --------------- | -------- | -------------- |
| boolean | f, t            | false    | Z              |
| byte    | [-128, 127]     | 0        | B              |
| short   | [-32768, 32767] | 0        | S              |
| char    | [0, 65535]      | '\u0000' | C              |
| int     | [-2^31, 2^31-1] | 0        | I              |
| long    | [-2^63, 2^63-1] | 0L       | J              |
| float   | 32 位           | +0.0F    | F              |
| double  | 64 位           | +0.0D    | D              |

一个基本类型的数据占多大空间？在栈上和在堆上是不一样的。如果是栈上，占用空间为 8 字节（如果是 32 位 cpu 则为 4 字节），如果是堆上，则有一个字节，两个字节，四个字节，八个字节。

# GC

- GC 算法中存在的 trade-off, 吞吐量和暂停时间。
- 吞吐量是指应用程序线程用时占程序总用时的比例。
- 吞吐量优先？ ParallelGC。
- 响应时间优先？ CMS。
- Java8 默认直接用 G1。

如何进行 jvm 调优？

Java 虚拟机中的垃圾回收器采用可达性分析来探索所有存活的对象。它从一系列 GC Roots 出发，边标记边探索所有被引用的对象。为了防止在标记过程中堆栈的状态发生改变，Java 虚拟机采取安全点机制来实现 Stop-the-world 操作，暂停其他非垃圾回收线程。

垃圾回收的三种算法： 标记清除，标记压缩，标记复制。

### jvm 堆的划分

- 新生代，老生代。
- 新生代又划分为 eden 区和两个大小相同的 survivor 区（from 和 to）。
- JVM 默认采用一种动态分配策略，根据对象生成速率，以及 survivor 区的是有情况动态调整 survivor 区所占比例。你也可以选择固定这个比例。
- Survivor 区中有一个永远是空的。
- new 对象时，会在 eden 划出一块内存。（由于堆是线程共享的，此操作需要同步）
- TLAB(Thread Local Allocation Buffer)，每次线程申请空间都申请一段连续内存。
- 当 eden 区空间用完，就触发 minor GC。将 eden 区和 survivor 的 from 区中依旧存活的对象复制到 survivor 的 to 区。
- 对象如果在 survivor 区中来回被复制过多次数（默认为 15 次），则提升到老年代。如果 survivor 区已经占用了 50%，复制次数较多的对象也会被提升到老年代。

总之，Minor GC 时我们应用标记清除算法，将 Survivor 区中的老存活对象晋升到老年代，然后将剩下的存活对象和 Eden 区的存活对象复制到另一个 Survivor 区中。理想情况下，Eden 区中的对象基本都死亡了，那么需要复制的数据将非常少，因此采用这种标记 - 复制算法的效果极好。Minor GC 的另外一个好处是不用对整个堆进行垃圾回收。

但是，Minor GC 有一个问题，那就是老年代的对象可能引用新生代的对象。也就是说，在标记存活对象的时候，我们需要扫描老年代中的对象。

HotSpot 给出的解决方案是一项叫做卡表（Card Table）的技术。该技术将整个堆划分为一个个大小为 512 字节的卡，并且维护一个卡表，用来存储每张卡的一个标识位。这个标识位代表对应的卡是否可能存有指向新生代对象的引用。如果可能存在，那么我们就认为这张卡是脏的。在进行 Minor GC 的时候，我们便可以不用扫描整个老年代，而是在卡表中寻找脏卡，并将脏卡中的对象加入到 Minor GC 的 GC Roots 里。当完成所有脏卡的扫描之后，Java 虚拟机便会将所有脏卡的标识位清零。

### 垃圾收集器

- 新生代： serial, Parallel Scavenge, Parallel New。都是标记复制算法。
- Parallel New 是 serial 的多线程版本，Parallel Scavenge 更注重吞吐率。
- 老年代： serial old, parallel old, cms。 serial old 和 parallel old 都是标记压缩算法，CMS 是并发的标记清除算法。
- 由于 G1 的出现，CMS 在 java9 中被废弃。
- G1（Garbage First）是一个横跨新生代和老年代的垃圾回收器。实际上，它已经打乱了前面所说的堆结构，直接将堆分成极其多个区域。每个区域都可以充当 Eden 区、Survivor 区或者老年代中的一个。它采用的是标记 - 压缩算法，而且和 CMS 一样都能够在应用程序运行过程中并发地进行垃圾回收。
- 改用 G1 GC，-XX:+UseG1GC 改用 G1
- 即将到来的 Java 11 引入了 ZGC，宣称暂停时间不超过 10ms。
- JAVA8 默认使用 parallelGc

默认 GC

- JAVA7 - parallel GC
- JAVA8 - parallel GC
- JAVA9 - G1 GC
- JAVA10 - G1 GC

怎么看 gc 日志 -XX:+PrintGCDetails

如何在 oom 时 dump 堆信息？ -XX:+HeapDumpOnOutOfMemoryError

热部署怎么做？ [java 热部署](https://www.ibm.com/developerworks/cn/java/j-lo-hotdeploy/index.html)

# 内存布局

除了最为常见的 new 语句之外，还可以通过反射机制、Object.clone 方法、反序列化以及 Unsafe.allocateInstance 方法来新建对象。其中，Object.clone 方法和反序列化通过直接复制已有的数据，来初始化新建对象的实例字段。allocateInstance 方法则没有初始化实例字段，而 new 语句和反射机制，则是通过调用构造器来初始化实例字段。以 new 语句为例，它编译而成的字节码将包含用来请求内存的 new 指令，以及用来调用构造器的 invokespecial 指令。

通过 new 指令新建出来的对象，它的内存其实涵盖了所有父类中的实例字段。也就是说，虽然子类无法访问父类的私有实例字段，或者子类的实例字段隐藏了父类的同名实例字段，但是子类的实例还是会为这些父类实例字段分配内存的。

JVM 中，每个 Java 对象都有一个对象头，由标记字段和类型指针所构成。其中，标记字段用以存储 Java 虚拟机有关该对象的运行数据，如哈希码、GC 信息以及锁信息，而类型指针则指向该对象的类。

64 位的 JVM 中，对象头的标记字段占 64 位，而类型指针又占了 64 位。也就是说，每一个 Java 对象在内存中的额外开销就是 16 个字节。

以 Integer 类为例，它仅有一个 int 类型的私有字段，占 4 个字节。因此，每一个 Integer 对象的额外内存开销至少是 400%。

为了尽量较少对象的内存使用量，64 位 Java 虚拟机引入了压缩指针[1]的概念（对应虚拟机选项 -XX:+UseCompressedOops，默认开启），将堆中原本 64 位的 Java 对象指针压缩成 32 位的。

# happens-before

在同一个线程中，字节码的先后顺序（program order）也暗含了 happens-before 关系：在程序控制流路径中靠前的字节码 happens-before 靠后的字节码。然而，这并不意味着前者一定在后者之前执行。实际上，如果后者没有观测前者的运行结果，即后者没有数据依赖于前者，那么它们可能会被重排序。

#### 如何监控和诊断 jvm 堆内内存和堆外内存的使用？

jconsole, visualvm, jstat, jmap
生成 heapdump, 查看 gc 日志

HotSpot 内置了多个即时编译器：C1、C2 和 Graal。
C1：Client 编译器，启动快，优化简单，编译快。
C2：Server 编译器，面向的是对峰值性能有要求的服务器端程序，优化复杂，启动慢。

### java 内存泄露问题

- memory leak through static field
- unclosed resource
- improper equals() and hashcode()
- inner classes that reference outer classes
- finalize()
- threadLocal 没有 remove。

##### Memory Leak through static field

除非 ClassLoader 可以被 gc 回收，不然 static 变量是不会被回收的。

```java
public class StaticTest {
    public static List<Double> list = new ArrayList<>();
    public void populateList() {
        for (int i = 0; i < 10000000; i++) {
            list.add(Math.random());
        }
        Log.info("Debug Point 2");
    }

    public static void main(String[] args) {
        Log.info("Debug Point 1");
        new StaticTest().populateList();
        Log.info("Debug Point 3");
    }
}
```

##### Unclosed Resource

每开一个新的连接或新 stream，jvm 都会分配内存。忘记关闭它们会导致这些内存无法回收。

##### Improper equals() and hashCode() implementations

```java
public class Person {
    public String name;
    public Person(String name) {
        this.name = name;
    }
}
@Test
public void givenMap_whenEqualsAndHashCodeNotOverridden_thenMemoryLeak() {
    Map<Person, Integer> map = new HashMap<>();
    for(int i=0; i<100; i++) {
        map.put(new Person("jon"), 1);
    }
    Assert.assertFalse(map.size() == 1);
}

```

##### Inner classes that reference outer classes

- 非静态内部类总是会有一个指向其外部类的引用。
- 如果我们在应用中有一个静态内部类的对象，这会导致外部的对象无法被 GC。
- 应该考虑使用 static class。

##### finalize() methods

- 如果一个类的 finalize()被 overriden 了，这个类的对象就不能被 instantly gc 了。
- 我们应该避免 override finalize() 方法。

##### ThreadLocals

- 每个线程都有一个指向其对应 threadLocal 变量的引用。
- threadlocal 会在线程死掉后被 gc。
- 我们常常使用 thread pool，这会导致线程常常是常驻的，不会死。
- 这也导致了 threadLocal 不会被 gc。
- good practice: clean-up ThreadLocals when they’re no longer used.
- It’s even better to consider ThreadLocal as a resource that needs to be closed in a finally block just to make sure that it is always closed.
