cppstdlib.com
http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2011/n3242.pdf

```c
#define __cplusplus 201103L
```

## new features in c++11
#### 小变动
std::nullptr表示空指针

#### 自动类型推断
```c
auto i = 42;
auto d = f();
vector<string> v;
auto pos = v.begin();
auto l = [] (int x) -> bool {...} // l是一个接受一个整数并返回一个bool的lambda
```

#### Uniform Initialization and Initializer Lists
```c
int values[] {1,2,3,4};
std::vector<int> v {2,3,5,7,11,13,17};
int *p;   // p has undefined value
int *q{}; // q is initialized by nullptr

void print (std::initializer_list<int> vals) {
    for (auto p=vals.begin(); p!=vals.end; ++p) {...}
}
print({12,3,5,7,11,13,17});
```

#### Range-based for loops
```c
for (decl : coll) {
    statement
}

for(int i : {2,3,5,7,9,13,17,19}) {
    std::cout << i << std::endl;
}

// 如果想给一个vector里面的每个元素乘以3呢?
for (auto& elem : vec) {
    elem *= 3;
}

templete <typename T>
void printElements(const T& collection) {
    for (const auto& elem : collection)
        std::cout << elem << std::endl;
}
```

#### move和右值引用
```c
使用move可以减少函数调用时不必要的内存复制。
move将其参数变成所谓的右值引用，其类型为X&&
... insert(const T& x);
... insert(const T&& x);
collection.insert(std::move(x));
```

#### 字符串字面量
```c
"\\\\n" 等价于 R"(\\n)"
还可以通过加前缀设置编码方式
```

#### noexcept关键字
表示一个函数不能抛异常，如果抛了则程序终止

```c
void foo () noexcept;
```

#### constexpr关键字
编译时求值

#### alias templates
```c
template <typename T>
using Vec = std::vector<T, MyAlloc<T>>;

Vec<int> coll; 等价于
std::vector<int, MyAlloc<int>> coll;
```

#### lambdas
```c
auto lam = [] {std::cout << "hello lambda" << std::endl};
lam();

// 你也可以直接调用
[] {std::cout << "hello lambda" << std::endl}();

// 完整类型
[] (参数列表) mutable execption -> returnType {body}
lambda可以捕获外层参数
```

```c
#include <functional>
#include <iostream>

std::function<int(int, int)> returnLambda() {
    return [] (int x, int y) {
        return x*y;
    };
}

int main() {
    auto lf = returnLambda();
    std::cout << lf(6,7) << std::endl;
}
```

#### decltype关键字
当你需要某个表达式的返回值类型而又不想实际执行它时用decltype。

```c
int a=8, b=3;
decltype(a+b) d; //编译期类型推导
```

#### 新的函数定义语法
```
template <typename T1, typename T2>
auto add(T1 x, T2 y) -> decltype(x+y);
```

#### scoped enumerations

#### 新的基础数据类型
```c
char16_t, char32_t
long long, unsigned long long
std::nullptr_t
```


# template 
### template function
```cpp
template <typename T>
void swapit(T & a, T & b) {
    T tmp = a;
    a = b;
    b = tmp;
}

string s = "abc";
string t = "cba";
swipit(a, b);
```