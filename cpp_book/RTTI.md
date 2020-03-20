# RTTI (Runtime Type Identification)
运行时类型识别，旨在为程序在运行阶段确定对象的类型。很多类库已经为其类对象提供了实现RTTI功能的方式。警告： RTTI只适应于包含虚函数的类。

假设有一个类层次结构，其中的类都是从同一个基类派生的，则可以让基类指针指向其中任何一个类的对象。问题是，如何知道指针指向的是哪个类的对象呢？？

### dynamic_cast
dynamic_cast是最常用的RTTI组件，它不能回答“指针指向的是哪类对象”的问题，但可以回答“是否可以安全地将对象的地址赋给特定类型的指针”的问题。

```c
class Grand{ // has virtual methods }
class Superb: public Grand {...};
class Magnificant: public Superb{...};
Grand *pg = new Grand;
...

Superb *pm = dynamic_cast<Superb *>(pb);
```

### typeid操作符和type_info类
```c
typeid (Magnificant) == typeid(*pg)
```

### 类型转换操作符
dynamic_cast;
const_cast;
static_cast;
reinterpret_cast;
