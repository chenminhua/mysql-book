#### object 类中的方法

clone, equals, hashCode, notify, notifyAll, 三个 wait，getClass, finalize

#### treeMap

```java
// 升序排列，基于红黑树。
TreeMap<String, String> map = new TreeMap<>((s1, s2) -> s1.compareTo(s2));
map.put("golang", ".go");
map.put("java", ".java");
```

#### int 和 Integer 的区别是什么?

原始数据类型和 Java 泛型并不能配合使用。Java 的泛型是伪泛型，是一种编译期的技巧，Java 编译期会自动将类型转换为对应的特定类型，这就决定了使用泛型，必须保证相应类型可以转换为 Object。

#### String, StringBuffer, StringBuilder 有什么区别？

- String 不可变，final class,所有的拼接操作都会生成新的 String，所以性能不好。
- StringBuffer 是一个线程安全的可修改字符序列。由于有线程安全的保证，相对性能开销也较大。
- StringBuilder 去掉了线程安全的部分，减小了开销，是绝大部分情况下拼接字符串的首选。
- 在 JDK 8 中，字符串拼接操作会自动被 javac 转换为 StringBuilder 操作.

#### Vector、ArrayList、LinkedList

- Vector:线程安全的动态数组(适合随机访问的场合)。内部使用对象数组来保存数据，性能差。
- ArrayList 是应用更加广泛的动态数组实现，非线程安全的，性能要好很多。
- LinkedList 双向链表(适合插入删除)，不需要扩容，非线程安全的。

#### Set

- TreeSet 代码里实际默认是利用 TreeMap 实现的。有序
- HashSet 是以 HashMap 为基础实现的。高效
- LinkedHashSet，内部构建了一个记录插入顺序的双向链表，因此提供了按照插入顺序遍历的能力，与此同时，也保证了常数时间的添加、删除、包含等操作，这些操作性能略低于 HashSet，因为需要维护链表的开销。
- 在遍历元素时，HashSet 性能受自身容量影响，所以初始化时，除非有必要，不然不要将其背后的 HashMap 容量设置过大。而对于 LinkedHashSet，由于其内部链表提供的方便，遍历性能只和元素多少有关系。

#### Hashtable, HashMap, TreeMap 有什么不同？

- Hashtable： 哈希表，同步，不支持 null，不推荐使用（性能问题）
- HashMap： 非同步，支持 null 的键和值，常数时间性能（首选）,线程不安全
- LinkedHashMap： 为键值对维护一个双向链表，遍历顺序符合插入顺序。
- TreeMap： 红黑树，可顺序访问的 map。整体顺序由键的顺序决定。

#### 为什么说 perfer Lists to arrays

数组是协变的，Sub[]是 Super[]的子类型。而泛型则是逆变的。换句话说，泛型（比如 List）能带来更好的类型安全。

```java
Object[] objectArray = new Long[1];
objectArray[0] = "I don't fit in"; // 编译通过，运行时抛错
List<Object> ol = new ArrayList<Long>(); // 直接抛错
```

另外，数组是具体化的，在运行时检查类型错误。而泛型在运行时已经擦除了类型。

### 为什么不能创建一个泛型数组呢？比如 List<String>[],或者 E[]

因为它不是类型安全的。泛型在运行时没有类型，而数组在编译时又是协变的，因此可能会导致把一组不同的泛型放入同一个泛型数组，从而破坏类型安全。泛型 List<E>, List<String>这种被称为 non-reifiable(非具体化)，它们在运行时的信息要少于编译时。

### 枚举到底是什么？

一个枚举在经过编译器编译过后，变成了一个抽象类，它继承了 java.lang.Enum；枚举常量，变成了相应的 public static final 属性，而且其类型就抽象类的类型，名字就是枚举常量的名字，同时我们可以看到 n 个内部类的.也就是说这 n 个命名字段分别使用了内部类来实现的；

### 深拷贝和浅拷贝

### lambda & stream

“A Stream is a tool for building up complex operations on collections using a functional approach.”

```java
int londonArtistCount = allArtists.stream().filter(artist -> artist.isFrom(“London”)).count();
```
