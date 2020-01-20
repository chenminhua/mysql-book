## panic 和 recover 机制

go 不能够抛出异常，而是使用了 panic 和 recover 机制。记住，**你的代码中应当没有或者很少有 panic 的东西**

```go
func main() {
  defer func () {
    if err:=recover(); err!=nil{
      fmt.Println(err) // 这里的err其实就是panic传入的内容
    }
  }()

  fmt.Println("start")
  panic("err stuff")
  fmt.Println("won't display")
}
```
