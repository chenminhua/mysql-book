TR1是一份规范，描述加入c++标准程序库的诸多新机能。
boost是个组织，也是一个网站 http://boost.org, 提供开放的c++程序库。

### 尽量以const, enum, inline替换 define

### 尽可能使用const
const 最具威力的用法是面对函数声明时的应用。在一个函数声明式内，const可以和函数返回值，参数，函数自身产生关联。

将const 应用于成员函数的目的是为了区分哪个函数可以改动对象内容而哪个函数不行。

改善c++程序效率的一个根本办法是以pass by reference-to-const方式传递对象。

### 确定对象在使用前被初始化
赋值和初始化是两回事，对于const或references成员变量必须赋初始值。

```cpp
// 赋值
ABEntry::ABEntry(const std::string & name, const std::string & address, const std::list<PhoneNumber> & phones) {
    theName = name;
    theAddress = address;
    thePhone = phone;
    numTimesConsulted = 0;
}

// 初始化
ABEntry::ABEntry(const std::string & name, const std::string & address, const std::list<PhoneNumber> & phones) {
    theName(name);
    theAddress(address);
    thePhone(phone);
    numTimesConsulted(0);
}
```
许多class拥有许多构造函数，每个构造函数有自己的成员初始值列。有时候可以将构造函数中重复的部分抽取到一个private的方法中去。