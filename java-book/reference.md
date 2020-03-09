- 强引用:只要还有强引用指向一个对象，垃圾回收旧不会碰它。
- 软引用:只有当 JVM 认为内存不足时，才会去试图回收软引用指向的对象。
- 弱引用:并不能使对象豁免垃圾收集，仅是提供访问在弱引用状态下对象的途径。
- 幻象引用(虚引用):不能通过它访问对象，仅是一种确保对象 finalize 后，做某些事情的机制。

JVM 会确保在抛出 OutOfMemoryError 之前，清理软引用指向的对象。软引用通常用来实现内存敏感的缓存。弱引用则可以用来构建一种没有特定约束的关系，比如，维护一种非强制性的映射关系，如果试图获取时对象还在，就使用它，否则重现实例化。它同样是很多缓存实现的选择。

判断对象可达性，是 JVM 垃圾收集器决定如何处理对象的一部分考虑。所有引用类型，都是抽象类 java.lang.ref.Reference 的子类，除了幻象引用（因为 get 永远返回 null），如果对象还没有被销毁，都可以通过 get 方法获取原有对象。这意味着，利用软引用和弱引用，我们可以将访问到的对象，重新指向强引用，也就是人为的改变了对象的可达性状态！

```java
ReferenceQueue<String> referenceQueue = new ReferenceQueue<>();
String str = new String("abc");
// 生成一个软引用，并与一个引用队列关联，当对象被垃圾回收，就将软引用加入队列。
SoftReference<String> softReference = new SoftReference<String>(str, referenceQueue);
str = null;
System.gc();
System.out.println(softReference.get()); // abc
Reference<? extends String> reference = referenceQueue.poll();
System.out.println(reference); //null

Browser browser = new Browser();
// 从后台程序加载浏览页面
BrowserPage page = browser.getPage();
// 将浏览完毕的页面置为软引用
SoftReference softReference = new SoftReference(page);
// 回退或者再次浏览此页面时
if(softReference.get() != null) {
    // 内存充足，还没有被回收器回收，直接获取缓存
    page = softReference.get();
} else {
    // 内存不足，软引用的对象已经回收
    page = browser.getPage();
    // 重新构建软引用
    softReference = new SoftReference(page);
}
```

虚引用主要用来跟踪对象被垃圾回收器回收的活动。

虚引用必须和引用队列(ReferenceQueue)联合使用。当垃圾回收器准备回收一个对象时，如果发现它还有虚引用，就会在回收对象的内存之前，把这个虚引用加入到与之关联的引用队列中。

程序可以通过判断引用队列中是否已经加入了虚引用，来了解被引用的对象是否将要进行垃圾回收。如果程序发现某个虚引用已经被加入到引用队列，那么就可以在所引用的对象的内存被回收之前采取必要的行动。

```java
String str = new String("abc");
ReferenceQueue queue = new ReferenceQueue();
// 创建虚引用，要求必须与一个引用队列关联
PhantomReference pr = new PhantomReference(str, queue);
```

### 引用队列（ReferenceQueue）使用

- 创建引用并关联到响应对象时，可以关联引用队列，JVM 会在特定时机将引用入到队列里，可从队列里获取引用进行后续逻辑。
- 尤其是幻象引用，get 方法只返回 null，如果再不指定引用队列，基本就没有意义了。利用引用队列，我们可以在对象处于相应状态时（对于幻象引用，就是前面说的被 finalize 了，处于幻象可达状态），执行后期处理逻辑。
- 对于软引用和弱引用，我们希望当一个对象被 gc 掉的时候通知用户线程，进行额外的处理时，就需要使用引用队列了。
- ReferenceQueue 即这样的一个对象，当一个 obj 被 gc 掉之后，其相应的包装类，即 ref 对象会被放入 queue 中。我们可以从 queue 中获取到相应的对象信息，同时进行额外的处理。比如反向操作，数据清理等。

```java
Object counter = new Object();
ReferenceQueue refQueue = new ReferenceQueue<>();
PhantomReference<Object> p = new PhantomReference<>(counter, refQueue);
counter = null;
System.gc();
try {
    // Remove是一个阻塞方法，可以指定timeout，或者选择一直阻塞
    Reference<Object> ref = refQueue.remove(1000L);
    if (ref != null) {
        // do something
    }
} catch (InterruptedException e) {
    // Handle it
}
```

### 诊断 JVM 引用情况

```
-XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintReferenceGC


0.403: [GC (Allocation Failure) 0.871: [SoftReference, 0 refs, 0.0000393 secs]0.871: [WeakReference, 8 refs, 0.0000138 secs]0.871: [FinalReference, 4 refs, 0.0000094 secs]0.871: [PhantomReference, 0 refs, 0 refs, 0.0000085 secs]0.871: [JNI Weak Reference, 0.0000071 secs][PSYoungGen: 76272K->10720K(141824K)] 128286K->128422K(316928K), 0.4683919 secs] [Times: user=1.17 sys=0.03, real=0.47 secs]
```

### Reachability Fence

除了我前面介绍的几种基本引用类型，我们也可以通过底层 API 来达到强引用的效果，这就是所谓的设置 reachability fence。

为什么需要这种机制呢？考虑一下这样的场景，按照 Java 语言规范，如果一个对象没有指向强引用，就符合垃圾收集的标准，有些时候，对象本身并没有强引用，但是也许它的部分属性还在被使用，这样就导致诡异的问题，所以我们需要一个方法，在没有强引用情况下，通知 JVM 对象是在被使用的。说起来有点绕，我们来看看 Java 9 中提供的案例。

```java

class Resource {
    private static ExternalResource[] externalResourceArray = ...
    int myIndex; Resource(...) {
        myIndex = ...
        externalResourceArray[myIndex] = ...;
        ...
    }
    protected void finalize() {
        externalResourceArray[myIndex] = null;
        ...
    }
    public void action() {
    try {
        // 需要被保护的代码
        int i = myIndex;
        Resource.update(externalResourceArray[i]);
    } finally {
        // 调用reachbilityFence，明确保障对象strongly reachable
        Reference.reachabilityFence(this);
    }
    }
    private static void update(ExternalResource ext) {
        ext.status = ...;
    }
}
```

在 JDK 源码中，reachabilityFence 大多使用在 Executors 或者类似新的 HTTP/2 客户端代码中，大部分都是异步调用的情况。编程中，可以按照上面这个例子，将需要 reachability 保障的代码段利用 try-finally 包围起来，在 finally 里明确声明对象强可达。
