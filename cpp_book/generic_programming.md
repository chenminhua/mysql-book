Bjarne在《The Design and Evolution of C++》一书中，详细的解释了C++为什么会变成如今（C++98/03）的模样。
模板作为C++中最有特色的语言特性，它堪称玄学的语法和语义，理所应当的成为初学者的梦魇。但是实际上C++模板远没有想象的那么复杂。我们只需要换一个视角：在C++03的时候，模板本身就可以独立成为一门“语言”。

87年的时候，泛型（Generic Programming）便被纳入了C++的考虑范畴。92年的时候，Alexander Stepanov开始研究利用模板语法制作程序库，后来这一程序库发展成STL，并在93年被接纳入标准中。在95年的《C++ Report》上，John Barton和Lee Nackman提出了一个矩阵乘法的模板示例。自此篇文章发表之后，很多大牛都开始对模板产生了浓厚的兴趣。其中对元编程技法贡献最大的当属Alexandrescu的《Modern C++ Design》及模板程序库Loki。这一2001年发表的图书间接地导致了模板元编程库的出现。书中所使用的Typelist等泛型组件，和Policy等设计方法令人耳目一新。

2002年出版的另一本书《C++ Templates》，可以说是在Template方面的集大成之作。它详细阐述了模板的语法、提供了和模板有关的语言细节信息，举了很多有代表性例子。但是对于模板新手来说，这本书细节如此丰富，让他们随随便便就打了退堂鼓缴械投降。

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

如上，在编译时，当遇到一个调用两个int引用参数时，编译器生成swap函数的int版本。

为了进一步了解模板，必须理解实例化和具体化。在代码中编写函数模板并不会生成函数定义，它只是一个用于生成函数定义的方案。而当编译器发现程序调用swap(x,y)时，会生成一个swap(int &, int &)的实例。这种实例化被称为**隐式实例化**。

现在c++还允许显示实例化，可以直接命令编译器创建特定的实例，如Swap<int>()。编译器看到这个声明将直接创建函数实例。

```cpp
template void Swap<int> (int, int);
```

除此之外，还可以使用显示具体化方法，让编译器不按照swap()模板来生成函数定义。

```cpp
template <> void Swap<int> (int &, int &);
```

编译器在选择函数原型时，遵循的规则是：非模板版本 优先于 显示具体化 优先于 模板版本。
