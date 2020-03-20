# auto
c++11中使用auto实现类型推导，c++98中使用auto表示变量为自动变量（现在已经废除）

# lambda表达式
在c++11之后可以使用。 （编译时使用-std=c++11）

```cpp
int a[6] = {9,8,2,3,5,4};
std::sort( a, &a[6], [](int x, int y){ return x < y;  }  );
for (int i=0; i<6; i++)
    cout << a[i] << ",";
```

# 右值引用
C++中所有的表达式和变量要么是左值，要么是右值。通俗的左值的定义就是非临时对象，那些可以在多条语句中使用的对象。所有的变量都满足这个定义，在多条代码中都可以使用，都是左值。右值是指临时的对象，它们只在当前的语句中有效。

如果临时对象通过一个接受右值的函数传递给另一个函数时，就会变成左值，因为这个临时对象在传递过程中，变成了命名对象。

右值引用是用来转移语义的。通过转移语义，临时对象中的资源可以转移到其他对象中。

如果已知一个命名对象不再被使用而想对它调用转移构造函数，可以使用std::move函数，把左值引用变成右值引用。

```cpp
// 接收左值
void process_value(int &i)
{
    cout << "LValue processed: " << i << endl;
}

// 接收右值
void process_value(int &&i)
{
    cout << "RValue processed: " << i << endl;
}

// 转发，临时对象在此过程中，由右值变成了左值。
void forward_value(int &&i)
{
    process_value(i);
}

// 通过Move减少了三次不必要的拷贝
template <typename T>
void swapit(T &a, T &b)
{
    T tmp(move(a));
    a = move(b);
    b = move(tmp);
}

int main()
{
    int a = 0;
    process_value(a);
    process_value(1);
    process_value(2);
    int x = 10;
    int y = 20;
    cout << "x=" << x << "  y=" << y << endl;
    swapit(x, y);
    cout << "x=" << x << "  y=" << y << endl;
}

// LValue processed: 0
// RValue processed: 1
// RValue processed: 2
// x=10  y=20
// x=20  y=10
```
