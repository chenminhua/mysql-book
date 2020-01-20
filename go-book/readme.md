https://peter.bourgon.org/go-best-practices-2016/

# 编写地道的 golang

1.声明 slice 的方法 var t []string 而不是 t := []string{}

2.尽可能处理 error，而不是 panic 或者忽略

3.包名单数小写，比如 model

4.通常会把自定义的 Error 放在 package 级别中，统一进行维护

5.省略不必要的变量，比如

```golang
var whitespaceRegex, _ = regexp.Compile("\\s+")
// 可以简写为 (错误在内部处理了，而不是返回出来)
var whitespaceRegex = regexp.MustCompile(`\s+`)
```

6.使用类型转换而不是 struct 字面量

7.复制 slice 可以使用 copy 函数

8.化简 range for range m {}

9.errors are values

10.使用 log.Println(err) 提供更加直观的上下文信息

11.使用 errors 包来处理错误

# go question

## slice 和 array 的区别

由于长度也是数组类型的一部分，因此[3]int 与[4]int 是不同的类型，数组也就不能改变长度。
数组之间的赋值**是值的赋值**，即当把一个数组作为参数传入函数的时候，**传入的其实是该数组的副本，而不是它的指针**。

slice 并不是真正意义上的动态数组，而是一个引用类型。其底层指向一个 array。
注意！！slice 是引用类型，所以当引用改变其中元素的值时，其它的所有引用都会改变。
当 append 操作超过 slice 的 capacity 时,double 它的 capacity。

```go
mySlice := []string{"mon","tue"}
myOther := []string{"wed","thu","fri"}
mySlice = append(mySlice, myOther...)   //注意这三个点
```

## map

map 也是一种引用类型，**如果两个 map 同时指向一个底层，那么一个改变，另一个也相应的改变**

## make 和 new 的区别

make 用于内建类型（map,slice,channel）的内存分配;new 用于各种类型的内存分配，new 返回指针。

## interface

依赖于接口而不是实现，优先使用组合而不是继承
interface 是一组 method 签名的组合，我们通过 interface 来定义对象的一组行为
interface 可以被任意的对象实现。一个对象可以实现任意多个 interface。任意的类型都实现了空 interface
空接口可以存储任何类型的值。
模块间尽可能通过接口来依赖，而不是通过 struct

## 断言

```go
value, ok := element.(T)
list := make(List, 3)
list[0] = 1
list[1] = "hello"

for index, element := range list {
  switch value := element.(type) {
  case int:
    fmt.Printf("list[%d] is an int and its value is %d\n", index, value)
  case string:
    fmt.Printf("list[%d] is a string and its value is %s\n", index, value)
  default:
    fmt.Println("list[%d] is of a different type", index)
  }
}
```

## 类型转换与反射

T(n)可以实现类型转换
fmt.Printf("%T\n", val)可以查看变量类型
或者可以使用 reflect.TypeOf
fmt.Println(reflect.TypeOf(b)) //int

## 函数可以接受未知个数的参数（可变参数）

```go
func average(sf ...float64) float64 {
	total := 0.0
	for _, v := range sf{
		total += v
	}
	return total / float64(len(sf))
}
//下面三种方法都可以
n := average(43,44,65,24,16)
data := []float64{12,43,43,22,424}
m := average(data...)
m2 := average(data)
```

## channel

定义一个 channel 时，也需要定义发送到 channel 的值的类型。
ci := make(chan int)
cf := make(chan interface{})

默认情况下，channel 接收和发送数据都是阻塞的，除非另一端已经准备好，这样就使得 Goroutines 同步变的更加的简单，而不需要显式的 lock。所谓阻塞，也就是如果读取（value := <-ch）它将会被阻塞，直到有数据接收。其次，任何发送（ch<-5）将会被阻塞，直到数据被读出。无缓冲 channel 是在多个 goroutine 之间同步很棒的工具。

## golang 的 gc 是如何实现的

## gc 的策略

## goroutine 是如何实现的

执行 goroutine 只需要极小的栈内存（大概 4-5kb）
runtime.Gosched() 可以让一个 goroutine 让出 CPU 时间片

## channel 是如何实现的

## 如何调度 goroutine

## 如何理解不要通过共享内存来通信，要通过通信来共享内存？

## package organization

按职责组织，而不是使用 models，types 这样的包
UserType 应该放在一个 service-layer 的包里面
使用 godoc, godoc -http=<hostport>
use doc.go file
