### 构造函数
构造函数用于构建类的对象。如果用户没有提供构造函数，c++将自动提供默认构造函数。
**在设计类时，最好主动提供对所有类成员做隐式初始化的构造函数，而不要使用编译器提供的默认构造函数。**

```cpp
class Stock {
public: 
  // 声明构造函数
  Stock(const std::string &company, int shares, double share_val);
private:
  std::string company;
  int shares;
  double share_val;
}
// 定义构造函数
Stock::Stock(const std::string &company, int shares, double share_val) 
    : company(company), shares(shares), share_val(share_val) {}

Stock s0 = Stock("nano", 20, 12.5);  // 显式调用构造函数
Stock s1("nano", 20, 12.5);          // 隐式调用构造函数
s1.show();

Stock *s2 = new Stock("nano", 20, 12.5);   // 构造函数与new结合使用,返回对象指针。这种情况下对象没有名称，但可以通过指针操作对象
s2->show();
```

tip: **如果既可以通过初始化，也可以通过赋值来设置对象的值，则应该采用初始化方式。通常效率更高**

### 析构函数
对象过期时，程序将自动调用一个特殊的成员函数：析构函数。析构函数负责save our ass。比如说你在构造函数里面使用new分配了一些内存，就需要在析构函数中调用delete来释放这些内存。上面的代码中，我们没有在构造函数中通过new分配内存，所以也不需要在析构函数中执行delete操作，这时候我们直接使用编译器生成的什么都不做的析构函数。

通常不应该在代码中显式调用析构函数（有例外情况），而应该让编译器决定什么时候调用析构函数。如果是静态存储变量，则析构函数在程序结束时调用。如果是自动变量，则在程序执行完代码块时调用。如果对象是通过new创建的，则析构函数在使用delete释放内存时调用。

### 隐式成员函数
c++自动提供了下面这些成员函数：
  默认构造函数，
  复制构造函数，
  赋值操作符，
  默认析构函数，
  地址操作符

### 复制构造函数
复制构造函数用于将一个对象复制到一个新对象中，它用于初始化过程。原型为Class_name (const Class_name &);新建一个对象并将其初始化为同类对象的时候，复制构造函数都会被调用。最常见的情况还是将新对象显示初始化为现有对象的时候。
比如 StringBad sailer = sports； 
实际调用了 StringBad sailor = StringBad(sports);
除此之外，当函数按值传递对象时，或者函数返回对象时，也都将调用复制构造函数。
使用默认复制构造函数存在一些危险，比如你希望在构造函数里面搞点黑科技，但是忘了重写复制构造函数。。。可以考虑使用显式复制构造函数来解决。

### const成员函数
const成员函数表明该函数不能修改对象。我们应该尽量将成员函数标记为const成员函数。

### this指针
每个成员函数(包括构造函数和析构函数)都有一个this指针，指向调用对象。如果函数需要使用整个对象而非地址（比如要返回对象引用），则可以使用*this解引用。

```cpp
class Stock {
public:
  const Stock & topval(const Stock & s) const;
}
const Stock & Stock::topval(const Stock & s) const {
  return s.total_val > total_val ? s : *this;
}
```

### 静态类成员
？？

### 操作符重载
operator overloading是一种形式的多态。c++允许将操作符重载扩展到用户定义的类型，比如让两个对象相加。

```h
// time.h
class Time {
private:
    int hours;
    int minutes;
public:
    Time();
    Time(int h, int m=0);

    // 重载
    Time operator+ (const Time & t) const;
    Time operator* (double n) const;

    void Show() const;
};
```

```cpp
// time.cpp
Time::Time() {
    hours = minutes = 0;
}

Time::Time(int h, int m) {
    hours = h;
    minutes = m;
}

Time Time::operator+ (const Time & t) const {
    Time sum;
    sum.minutes = minutes + t.minutes;
    sum.hours = hours + t.hours + sum.minutes / 60;
    sum.minutes %= 60;
    return sum;
}

Time Time::operator* (double mult) const {
        Time result;
        long totalminutes = hours * mult * 60 + minutes * mult;
        result.hours = totalminutes / 60;
        result.minutes = totalminutes % 60;
        return result;
}

void Time::Show() const {
        cout << hours << ":" << minutes << endl;
}
```

```cpp
// main.cpp
Time coding(2, 40);
Time fixing(5, 55);
Time total;

coding.Show();
total = coding + fixing;
total.Show();
```

### 友元
c++控制对类对象私有部分的访问。通常，公有类方法提供唯一的访问途径，但是有时候这种限制太严格。此时c++提供了另一种形式的访问权限：友元。

友元有三种：友元函数，友元类，友元成员函数。

在函数重载的例子中，我们希望 time * 10 和 10 * time 相同，但是通过函数重载是做不到的。

```cpp
// 友元函数，处理 10 * time 这种情况
friend Time operator* (double n, const Time & t) {
    // 调用了被重载的 * 运算符
    return t * n;
};

// 重载<<操作符是一种常用的友元
friend std::ostream & operator<< (std::ostream & os, const Time & t);

std::ostream & operator<< (std::ostream & os, const Time & t) {
    os << t.hours << ":" << t.minutes << endl;
    return os;
}
```

### 动态内存分配
让程序在运行时决定内存分配，而不是在编译时决定。这样可以根据需要来使用内存。但是在类中使用new，delete操作符会导致许多编程问题。析构函数将变得必不可少（需要在析构函数中释放内存）
