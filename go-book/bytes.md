深入解析 Go 语言三大基础文本类型：string, byte, rune 内部结构和转换黑魔法。

# 概览

Go 中，字符串 string 是内置类型，与文本处理相关的内置类型还有符文 rune 和字节 byte。无论是源码还是字符串的内部编码都是 UTF8。

Go 将大部分字符串处理的函数放在了 strings,bytes 这两个包里。字符串和其他基本类型的转换的功能主要在标准库 strconv 中提供。unicode 相关功能在 unicode 包中提供。encoding 包提供了一系列其他的编码支持。

- Go 使用 rune 代表 Unicode 码位。一个字符可能由一个或多个码位组成（复合字符）
- Go string 是建立在字节数组的基础上的，因此对 string 使用[]索引会得到字节 byte 而不是字符 rune。
- Go 语言的字符串不是正规化(normalized)的，因此同一个字符可能由不同的字节序列表示。使用 unicode/norm 解决此类问题。

## 基础数据结构

要讨论[]byte 和[]rune，先要理解 Go 语言中的数组(Array)与切片(Slice)，切片是对数组的引用。
数组 Array 是固定长度的数据结构，不存放任何额外的信息，很少直接使用。切片 Slice 描述了数组中一个连续的片段，Go 语言的切片操作与 Python 较为类似。

在底层实现中，切片可以看成一个由三个 word 组成的结构体，这里 word 是 CPU 的字长。这三个字分别是 ptr,len,cap，分别代表数组首元素地址，切片的长度，当前切片头位置到底层数组尾部的距离。

因此，在函数参数中传递十个元素的数组，那么就会在栈上复制这十个元素。而传递一个切片，则实际上传递的是这个 3Word 结构体。传递切片本身就是传递引用。

字节 byte 实际上是 uint8 的别名，只是为了和其他 8bit 类型相区别才单独起了别名。通常出现的更多的是字节切片[]byte 与字节数组[...]byte。

字面值，字节可以用单引号扩起的单个字符表示，不过这种字面值和 rune 的字面值很容易搞混。赋予字节变量一个超出范围的值，如果在编译期能检查出来就会报 overflows byte 编译错误。

字节数组的本体结构定义如下：

```go
type SliceHeader struct {
    Data uintptr
    Len int
    Cap int
}
```

string 通常是 UTF8 编码的文本，由一系列 8bit 字节组成。raw string literal 和不含转义符号的 string literal 一定是 UTF-8 编码的，但 string 其实可以含有任意的字节序列。字符串是不可变对象，可以空(s="")，但不会是 nil。

string 在 Go 中的实现与 Slice 类似，但因为字符串是不可变类型，因此底层数组的长度就是字符串的长度，所以相比切片，string 结构的本体少了一个 Cap 字段。只有一个指针和一个长度值，由两个 Word 组成。64 位机器上占用 16 个字节。

```go
type StringHeader struct {
    Data uintptr
    Len int
}
```

虽然字符串是不可变类型，但通过指针和强制转换，还是可以进行一些危险但高效的操作的。不过要注意，编译器作为常量确定的 string 会写入只读段，是不可以修改的。相比之下,fmt.Sprintf 生成的字符串分配在堆上，就可以通过黑魔法进行修改。
关于 string，有这么几点需要注意。

- string 常量会在编译期分配到只读段，对应数据地址不可写入。
- 常量空字符串有数据地址，动态生成的字符串没有设置数据地址 ，只有动态生成的 string 可以 unsafe 魔改。
- string 和[]byte 转换，会将数据复制到堆上，返回数据指向复制的数据。所以 string(bytes)存在开销
- string 和[]byte 通过复制转换，性能损失接近 4 倍
  符文 rune
  符文 rune 其实是 int32 的别名，表示一个 Unicode 的码位。
  注意一个字符(Character)可以由一个或多个码位(Code Point)构成。例如带音调的 e，即 é,既可以由\u00e9 单个码位表示，也可以由 e 和口音符号\u0301 复合而成。这涉及到 normalization 的问题。但通常情况下一个字符就是一个码位。
  > > > print u'\u00e9', u'e\u0301',u'e\u0301\u0301\u0301'
  > > > é é é́́
  > > > 符文的字面值是用单引号括起的一个或多个字符，例如 a,啊,\a,\141,\x61,\u0061,\U00000061，都是合法的 rune literal。其格式定义如下：
  > > > rune_lit = "'" ( unicode_value | byte_value ) "'" .
  > > > unicode_value = unicode_char | little_u_value | big_u_value | escaped_char .
  > > > byte_value = octal_byte_value | hex_byte_value .
  > > > octal_byte_value = `\` octal_digit octal_digit octal_digit .
  > > > hex_byte_value = `\` "x" hex_digit hex_digit .
  > > > little_u_value = `\` "u" hex_digit hex_digit hex_digit hex_digit .
  > > > big_u_value = `\` "U" hex_digit hex_digit hex_digit hex_digit
                               hex_digit hex_digit hex_digit hex_digit .
  escaped_char = `\` ( "a" | "b" | "f" | "n" | "r" | "t" | "v" | `\` | "'" | `"` ) .
  其中，八进制的数字范围是 0~255，Unicode 转义字符通常要排除 0x10FFFF 以上的字符和 surrogate 字符。
  看上去这样用单引号括起来的字面值像是一个字符串，但当源代码转换为内部表示时，它其实就是一个 int32。所以 var b byte = '蛤'，其实就是为 uint8 赋了一个 int32 的值，会导致溢出。相应的，一个 rune 也可以在不产生溢出的条件下赋值给 byte。
  文本类型转换
  三种基本文本类型之间可以相互转换，当然，有常规的做法，也有指针黑魔法。
  string 与[]byte 的转换
  string 和 bytes 的转换是最常见的，因为通常通过 IO 得到的都是[]byte，例如 io.Reader 接口的方法签名为：Read(p []byte) (n int, err error)。但日常字符串操作使用的都是 string，这就需要在两者之间进行转换。
  常规做法
  通常[]byte 和 string 可以直接通过类型名强制转化，但实质上执行了一次堆复制。理论上 stringHeader 只是比 sliceHeader 少一个 cap 字段，但因为 string 需要满足不可变的约束，而[]byte 是可变的，因此在执行[]byte 到 string 的操作时会进行一次复制，在堆上新分配一次内存。
  // byte to string
  s := string(b)
  // string index -> byte
  s[i] = b
  // []byte to string
  s := string(bytes)
  // string to []byte
  bytes := []byte(s)
  黑魔法
  利用 unsafe.Pointer 和 reflect 包可以实现很多禁忌的黑魔法，但这些操作对 GC 并不友好。最好不要尝试。
  type Bytes []byte
  // 将 string 转换为[]byte，'可以修改'，很危险，因为[]byte 结构要多一个 cap 字段。
  func StringBytes(s string) Bytes {
  return *(*Bytes)(unsafe.Pointer(&s))
  }
  // 不拷贝地将[]byte 转换为 string
  func BytesString(b []byte) String {
  // 因为[]byte 的 Header 只比 string 的 Header 多一个 Cap 字段。可以直接强制成`*String`
  return *(*String)(unsafe.Pointer(&b))
  }
  // 获取&s[0]，即存储字符串的字节数组的地址指针，Go 里不允许这种操作。
  func StringPointer(s string) unsafe.Pointer {
  p := (*reflect.StringHeader)(unsafe.Pointer(&s))
  return unsafe.Pointer(p.Data)
  }
  // r 获取&b[0]，即[]byte 底层数组的地址指针，Go 里不允许这种操作
  func BytesPointer(b []byte) unsafe.Pointer {
  p := (*reflect.SliceHeader)(unsafe.Pointer(&b))
  return unsafe.Pointer(p.Data)
  }
  string 与 rune 的转换
  string 是 UTF8 编码的字符串，因此对于非含有 ASCII 字符的字符串，是没法简单的直接索引的。例如
  fmt.Printf("%x","hello"[0])，会取出第一个字节 h 的相应字节表示 uint8，值为：0x68。然而
  fmt.Printf("%s","你好"[0])，也是同理，在 UTF-8 编码中，汉字”你”被编码为 0xeE4BDA0 由三个字节组成，因此使用下标 0 去索引字符串，并不会取出第一个汉字字符的 int32 码位值 0x4f60 来，而是这三个字节中的第一个 0xE4。
  没有办法随机访问一个中文汉字是一件很蛋疼的事情。曾经 Java 和 Javascript 之类的语言就出于性能考虑使用 UCS2/UTF-16 来平衡时间和空间开销。但现在 Unicode 字符远远超过 65535 个了，这点优势已经荡然无存，想要准确的索引一个字符（尤其是带 Emoji 的），也需要用特制的 API 从头解码啦，啪啪啪打脸苍天饶过谁……。
  常规方式
  string 和 rune 之间也可以通过类型名直接转换，不过 string 不能直接转换成单个的 rune。
  // rune to string
  str := string(r)
  // range string -> rune
  for i,r := range str
  // string to []rune
  runes := []rune(str)
  // []rune to string
  str := string(runes)
  特殊支持
  Go 对于 UTF-8 有特殊的支持和处理（因为 UTF-8 和 Go 都是 Ken 发明的……。），这体现在对于 string 的 range 迭代上。
  const nihongo = "日本語"
  for index, runeValue := range nihongo {
  fmt.Printf("%#U starts at byte position %d\n", runeValue, index)
  }
  U+65E5 '日' starts at byte position 0
  U+672C '本' starts at byte position 3
  U+8A9E '語' starts at byte position 6
  直接索引 string 会得到字节序号和相应字节。而对 string 进行 range 迭代，获得的就是字符 rune 的索引与相应的 rune。
  byte 与 rune 的转换
  byte 其实是 uint8，而 rune 实际就是 int32，所以 uint8 和 int32 两者之间的转换就是整数的转换。
  但是[]uint8 和[]int32 是两个不同类型的整形数组，它们之间是没有直接强制转换的方法的，好在通过 string 来曲线救国：runes := []rune(string(bytes))
