# 重要资料
[twitter](twitter.github.io/scala_school)

# 流程控制
```scala
for (i <- 0 until s.length) // Last value for i is s.length - 1
for (ch <- "Hello") sum += ch
for (i <- 1 to 3; j <- 1 to 3 if i != j) print((10 * i + j) + " ")
for (c <- "Hello"; i <- 0 to 1) yield (c + i).toChar
```

# 函数
```scala
def abs(x: Double) = if (x >= 0) x else -x

def fac(n : Int) = {
  var r = 1
  for (i <- 1 to n) r = r * i
  r
}

//如果是reursive函数，需要指明函数的返回值类型
def fac(n: Int): Int = if (n <= 0) 1 else n * fac(n - 1)

def adder(m: Int, n:Int) = m + n
val add2 = adder(2, _:Int)
add2(3)  //5

//默认参数和命名参数
def decorate(str: String, left: String = "[", right: String = "]") = left + str + right
decorate(left = "<<<", str = "Hello", right = ">>>")

//可变参数
def capitalizeAll(args: String*) = {
  args.map { arg =>
    arg.capitalize
  }
}
```

# 异常处理
```scala
if (x >= 0) { sqrt(x)
} else throw new IllegalArgumentException("x should not be negative")

try {
  process(new URL("http://horstmann.com/fred-tiny.gif"))
} catch {
  case _: MalformedURLException => println("Bad URL: " + url)
  case ex: IOException => ex.printStackTrace()
}

var in = new URL("http://horstmann.com/fred.gif").openStream()
try {
  process(in)
} finally {
  in.close()
}
```

# array and array buffer
```scala
val nums = new Array[Int](10)  //定长array
import scala.collection.mutable.ArrayBuffer //array buffer
val b = ArrayBuffer[Int]()

0 until (a.length, 2)  // Range(0, 2, 4, ...)
(0 until a.length).reverse  // Range(..., 2, 1, 0)

val a = Array(2, 3, 5, 7, 11)
val result = for (elem <- a) yield 2 * elem
for (elem <- a if elem % 2 == 0) yield 2 * elem  //Array(4)
a.filter(_ % 2 == 0).map(2 * _)  //Array(4)
a filter { _ % 2 == 0 } map { 2 * _ }  //Array(4)

Array(1,2,3).sum //求和
ArrayBuffer("Mary", "had", "a", "little", "lamb").max  // little
val b = ArrayBuffer(1, 7, 2, 9) val bSorted = b.sorted(_ < _)  //ArrayBuffer(1, 2, 7, 9)
val a = Array(1, 7, 2, 9)
scala.util.Sorting.quickSort(a)  // a is now Array(1, 2, 7, 9)
```

# map
```scala
val scores = Map("alice" -> 10, "bob" -> 20) // immutable map
val scores = Map(("alice", 10), ("bob", 3))  // immutable map
val scores = scala.collection.mutable.Map("Alice" -> 10, "Bob" -> 3, "Cindy" -> 8)  // mutable map
scores("alice")
val bobsScore = if (scores.contains("Bob")) scores("Bob") else 0  //检查是否有值
val bobsScore = scores.getOrElse("Bob", 0)   //getOrElse更加直接有效

// 对于mutable map,可以 Update
scores("Fred") = 12
// 对于immutable map,不可以update,但是可以创建新的map来实现
val newScores = scores + ("Fred" -> 10, "Bob" -> 13)
// 如果你的scores是var,则更简单
scores = scores + ("Fred" -> 10, "Bob" -> 13)

scores.keySet // Set("Bob", "Cindy", "Fred", "Alice")
for (v <- scores.values) println(v)
// 键值互换
for ((k, v) <- scores) yield (v, k)
```

# tuple
```scala
val t = (1, 3.14, "Fred")
t._2 // 3.14
val (first, second, third) = t
val (first, second, _) = t

//zip
val symbols = Array("<", "-", ">")
val counts = Array(2, 10, 2)
val pairs = symbols.zip(counts)  // Array(("<", 2), ("-", 10), (">", 2))
```

### currying
```scala
def multiply(m: Int)(n: Int): Int = m * n
myltiply(2)(3)  //6
```

# 类
```scala
class Calculator {
  val brand: String = "HP"
  def add(m: Int, n: Int): Int = m + n
}

val calc = new Calculator
calc.add(1, 2)   //3
calc.brand
```

```scala
class Calculator(brand: String) {
  val color: String = if (brand == "TI") {
    "BLUE"
  } else if (brand == "HP") {
    "BLACK"
  } else {
    "WHITE"
  }
  def add(m: Int, n: Int): Int = m + n
}

val calc = new Calculator("HP")
```

### 继承
```scala
class ScientificCalculator(brand: String) extends Calculator(brand) {
  def log(m: Double, base: Double) = math.log(m) / math.log(base)
}
```

scala的方法如果没有参数，可以不写括号

### 方法重载
```scala
class EvenMoreScientificCalculator(brand: String) extends ScientificCalculator(brand) {
  def log(m: Int): Double = log(m, math.exp(1))
}
```

### 抽象类
抽象类，它定义了一些方法但没有实现它们。取而代之是由扩展抽象类的子类定义这些方法。你不能创建抽象类的实例。

```scala
abstract class Shape {
  def getArea():Int    // subclass should define this
}

class Circle(r: Int) extends Shape {
  def getArea():Int = { r * r * 3 }
}
```

### traits
```scala
trait Car {
  val brand: String
}

trait Shiny {
  val shineRefraction: Int
}

class BMW extends Car with Shiny {
  val brand = "BMW"
  val shineRefraction = 12
}
```
什么时候应该使用特质而不是抽象类？如果你想定义一个类似接口的类型，你可能会在特质和抽象类之间难以取舍。这两种形式都可以让你定义一个类型的一些行为，并要求继承者定义一些其他行为。一些经验法则：

优先使用特质。一个类扩展多个特质是很方便的，但却只能扩展一个抽象类。
如果你需要构造函数参数，使用抽象类。因为抽象类可以定义带参数的构造函数，而特质不行。

### apply 方法
当类或对象有一个主要用途的时候，apply方法为你提供了一个很好的语法糖。

```scala
class Foo{}
object FooMaker{
  def apply() = new Foo
}
val newFoo = FooMaker()
```

# 单例对象
```scala
object Timer {
  var count = 0

  def currentCount(): Long = {
    count += 1
    count
  }
}
Timer.currentCount()
```

# type checks and casts
```scala
if (p.isInstanceOf[Employee]) {  //如果p是Employee或者其子类则为true
  val s = p.asInstanceOf[Employee] //转为Employee
  ...
}
if (p.getClass == classOf[Employee])  //p为Employee的实例而不是其子类的实例

// 模式匹配往往是更好的选择
p match {
  case s: Employee => ... // Process s as a Employee
  case _ => ... // p wasn’t a Employee
}
```

# scala中的函数
scala中的函数是一些特质（traits）的集合，具有一个参数的函数是Function1特质的一个实例。这个特征定义了apply()语法糖。apply语法糖有助于统一对象和函数式编程的二重性。你可以传递类，并把它们当做函数使用，而函数本质上是类的实例。

# 模式匹配
```scala
val times = 1

times match {
  case 1 => "one"
  case 2 => "two"
  case _ => "some other number"
}
```

# 匹配类型
```scala
def bigger(o: Any): Any = {
  o match {
    case i: Int if i < 0 => i - 1
    case i: Int => i + 1
    case d: Double if d < 0.0 => d - 0.1
    case d: Double => d + 0.1
    case text: String => text + "s"
  }
}
```

# 样本类
样本类基于构造函数的参数，自动地实现了相等性和易读的toString方法。

```scala
case class Calculator(brand: String, model: String)

val hp20b = Calculator("HP", "20B")
val hp30b = Calculator("HP", "30B")

def calcType(calc: Calculator) = calc match {
  case Calculator("HP", "20B") => "financial"
  case Calculator("HP", "48G") => "scientific"
  case Calculator("HP", "30B") => "business"
  case Calculator(ourBrand, ourModel) => "Calculator: %s %s is of unknown type".format(ourBrand, ourModel)
}
```

# 异常
```scala
try {
  remoteCalculatorService.add(1, 2)
} catch {
  case e: ServerIsDownException => log.error(e, "the remote calculator service is unavailable. should have kept your trusty HP.")
} finally {
  remoteCalculatorService.close()
}
```

# 列表
```scala
val numbers = List(1, 2, 3, 4)
```

# set
```scala
Set(1, 1, 2)
```

# tuple
```scala
val hostPort = ("localhost", 80)
hostPort._1
hostPort._2

hostPort match {
  case ("localhost", port) => ...
  case (host, port) => ...
}
```

# map
```scala
Map(1 -> 2)
Map("foo" -> "bar")
Map(1 -> Map("foo" -> "bar"))
```

# option
Option本身是泛型的，并且有两个子类： Some[T] 或 None.
好多新的语言里面都加入了optional值的概念，比如swift

```scala
trait Option[T] {
  def isDefined: Boolean
  def get: T
  def getOrElse(t: T): T
}

val result = res1.getOrElse(0) * 2
或者
val result = res1 match {
  case Some(n) => n * 2
  case None => 0
}
```

# 函数组合子
```scala
numbers.map((i: Int) => i * 2)
def timesTwo(i: Int): Int = i * 2
numbers.map(timesTwo _)
numbers.foreach((i: Int) => i * 2)
numbers.filter((i: Int) => i % 2 == 0)
def isEven(i: Int): Boolean = i % 2 == 0
numbers.filter(isEven _)
List(1, 2, 3).zip(List("a", "b", "c"))  //List((1,a), (2,b), (3,c))
val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
numbers.partition(_ % 2 == 0)  //(List(2, 4, 6, 8, 10),List(1, 3, 5, 7, 9))
numbers.find((i: Int) => i > 5)   //Option[Int] = Some(6), 返回集合中第一个匹配谓词函数的元素。
numbers.drop(5)  //删除前5个元素
numbers.dropWhile(_ % 2 != 0)  //删除第一个匹配的元素
numbers.foldLeft(0)((m: Int, n: Int) => m + n)  //55
numbers.foldRight(0) { (m: Int, n: Int) => println("m: " + m + " n: " + n); m + n } //55
List(List(1, 2), List(3, 4)).flatten  //扁平化，List(1, 2, 3, 4)
val nestedNumbers = List(List(1, 2), List(3, 4))
nestedNumbers.flatMap(x => x.map(_ * 2))  //List(2, 4, 6, 8)
```

# 扩展函数组合子
```scala
def ourMap(numbers: List[Int], fn: Int => Int): List[Int] = {
  numbers.foldRight(List[Int]()) { (x: Int, xs: List[Int]) =>
    fn(x) :: xs
  }
}

ourMap(numbers, timesTwo(_))  //List(2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
```

# Map?
```scala
val extensions = Map("steve" -> 100, "bob" -> 101, "joe" -> 201) //Map((steve,100), (bob,101), (joe,201))
extensions.filter((namePhone: (String, Int)) => namePhone._2 < 200)
extensions.filter({case (name, extension) => extension < 200})
```

# 函数组合
```scala
def f(s: String) = "f(" + s + ")"
def g(s: String) = "g(" + s + ")"

val fComposeG = f _ compose g _
fComposeG("yay")   //f(g(yay))

val fAndThenG = f _ andThen g _
fAndThenG("yay")   //g(f(yay))
```

# case语句
case语句是一个名为PartialFunction的函数的子类。
多个case语句是共同组合在一起的多个PartialFunction
对给定的输入参数类型，函数可接受该类型的任何值。换句话说，一个(Int) => String 的函数可以接收任意Int值，并返回一个字符串。
对给定的输入参数类型，偏函数只能接受该类型的某些特定的值。一个定义为(Int) => String 的偏函数可能不能接受所有Int值为输入。
isDefinedAt是PartialFunction的一个方法，用来确定PartialFunction是否能接受一个给定的参数。

```scala
val one: PartialFunction[Int, String] = { case 1 => "one" }
one.isDefinedAt(1)  //true
one.isDefinedAt(2)  //false
one(1)  //one

val two: PartialFunction[Int, String] = { case 2 => "two" }
val three: PartialFunction[Int, String] = { case 3 => "three" }
val wildcard: PartialFunction[Int, String] = { case _ => "something else" }
val partial = one orElse two orElse three orElse wildcard
partial(5)  //something else
partial(3)  //three
```


