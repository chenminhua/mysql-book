## final, finally, finalize

- final 修饰的 class： 不可继承扩展
- final 修饰变量： 不可修改。但 final 不是 immutable.
- final 修饰方法： 不可 override
- finalize 在垃圾回收前执行，不推荐使用，已被 java9 deprecated，会导致垃圾回收变慢。

### object 类中的方法

clone, equals, hashCode, notify, notifyAll, 三个 wait，getClass, finalize
