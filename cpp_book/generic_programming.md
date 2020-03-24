Bjarne 在《The Design and Evolution of C++》一书中，详细的解释了 C++为什么会变成如今（C++98/03）的模样。
模板作为 C++中最有特色的语言特性，它堪称玄学的语法和语义，理所应当的成为初学者的梦魇。但是实际上 C++模板远没有想象的那么复杂。我们只需要换一个视角：在 C++03 的时候，模板本身就可以独立成为一门“语言”。

# template function

```cpp
// 注意class关键字可以替换为typename关键字
template <class Any>
void Swap(Any &a, Any &b) {
  Any temp;
  temp = a;
  a = b;
  b = temp;
}
int x,y;
...
swap(x,y);
```

如上，在编译时，当遇到一个调用两个 int 引用参数时，编译器生成 swap 函数的 int 版本。

为了进一步了解模板，必须理解实例化和具体化。在代码中编写函数模板并不会生成函数定义，它只是一个用于生成函数定义的方案。而当编译器发现程序调用 swap(x,y)时，会生成一个 swap(int &, int &)的实例。这种实例化被称为**隐式实例化**。

现在 c++还允许显示实例化，可以直接命令编译器创建特定的实例，如 Swap<int>()。编译器看到这个声明将直接创建函数实例。

```cpp
template void Swap<int> (int, int);
```

除此之外，还可以使用显示具体化方法，让编译器不按照 swap()模板来生成函数定义。

```cpp
template <> void Swap<int> (int &, int &);
```

编译器在选择函数原型时，遵循的规则是：非模板版本 优先于 显示具体化 优先于 模板版本。
