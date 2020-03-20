### 1.仔细选择你的容器
```
vector, string, deque, list
set, multiset, map, multimap
slist, rope
hash_set, hash_multiset, hash_map, hash_multimap
vector
bitset, stack, queue, pripority_queue
```

区分连续内存容器和基于节点的容器。连续内存容器也叫基于数组的容器，通常查询速度较快而插入删除效率较低。基于节点的容器在每个内存块中只保存一个元素，插入删除不需要移动元素因而效率较高，但是查询效率较低。

```
你需要在任意位置插入一个元素吗？
你关心元素在容器中的位置吗？
你必须使用标准c++中的容器吗？
你需要哪种迭代器？
容器中数据的内存布局需要兼容c吗？
查找速度很重要吗？如果是，你需要散列
你需要插入和删除的事务性语义吗？
```

### 2.小心对“容器无关代码”的幻想
STL是建立在泛化上的，数组泛化为容器，函数泛化为算法，指针泛化为迭代器。

标准的连续内存容器都提供随机访问迭代器，标准的基于节点的容器都提供双向迭代器。序列容器都提供push_front和push_back。关联容器提供对数时间复杂度的lower_bound,upper_bound和equal_range成员函数。

### 3.使容器里对象的拷贝操作轻量而正确

### 4.用empty来代替检查size()是否为0
调用empty总是比检查size()为0更好，因为empty总是常数时间操作，而size则不一定。

### 5.尽量使用区间成员函数代替它们的单元素兄弟
尽量避免手写显示循环[item43]

```
vector<Widget> v1,v2;
v1.clear();
for (vector<Widget>::const_iterator ci = v2.begin() + v2.size()/2; ci != v2.end(); ++ci)
  v1.push_back(*ci);

v1.assign(v2.begin() + v2.size()/2, v2.end());

v1.claer();
copy(v2.begin() + v2.size()/2,v2.end(), back_inserter(v1));
```

### 6.警惕c++最令人恼怒的解析


### 7.当使用new得指针的容器时，记得在销毁容器前delete那些指针


### 8.永不建立auto_ptr的容器


### 9.在删除选项中仔细选择

### 10.注意分配器的协定和约束


### 11.理解自定义分配器的正确用法


### 12.对stl容器的线程安全性的期待现实一点


### 13.尽量使用vector和string来代替动态分配的数组


### 14.使用reserve避免不必要的重新分配

### 15.小心string实现的多样性

### 17.使用“交换技巧”来修整过剩容量


### 18.不要使用vector<bool>