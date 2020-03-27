## 简介
强类型，静态类型，类型推导，显式地使用类型转。编译器负责检查类型错误。
在其他语言里，类型系统为编译器服务；而在 Haskell 里，类型系统为你服务。
程序是类型上的证明。

:?, :info (+), :type 'a'
:set +t, :unset +t
:m +Data.Ratio    载入模块

## 列表与元组
[1..10], ['a'..'z'], [10, 9..1]
[1,2] ++ [3,4]           // [1,2,3,4]
1 : [2,3]                // [1,2,3]
head [1,2,3,4]           // 1
tail [1,2,3,4]           // [2,3,4]
init [1,2,3,4]           // [1,2,3]
last [1,2,3,4]           // 4
length [1,2,3,4]         // 4
null [1,2,3]             // False
null []                  // True
reverse [1,2,3,4]        // [4,3,2,1]
maximum [3,1,4,2]        // 4
minimum [3,1,4,2]        // 1
sum [1,2,3]              // 6 
elem 4 [1,2,3,4]         // True
take 2 [1,2,3,4,5]       // [1,2]
drop 2 [1,2,3,4,5]       // [3,4,5]
字符串就是字符的列表 [Char]
"" == []                 // True
'a':"bcd"                // "abcd"
"abc"++"bcd"             // "abcbcd"

take 3 (repeat 5)      // [5,5,5]
replicate 3 5          // [5,5,5]

[x*2 | x <- [1..10]]   // [2,4,6,8,10,12,14,16,18,20]
[x*2 | x <- [1..10], x>=6]    // [12,14,16,18,20]

boomBangs xs = [if x < 10 then "boom" else "bang" | x <- xs, odd x]
boomBangs [7..13]         // ["boom","boom","bang","bang"]

笛卡尔积
[x*y | x <- [2,5,10], y <- [8,10,11]]    // [16,20,22,40,50,55,80,100,110]

自己实现一个length
length' xs = sum [1 | _ <- xs]

去除所有非大写字母
removeNonUppercase st = [c | c <- st, elem c ['A'..'Z']]


:type (True, "hello")        // (True, "hello") :: (Bool, [Char])
Haskell有一个特殊的类型(),它的作用相当于包含零个元素的元组,类似于void
fst (1, 'a')  // 1
snd (1, 'a')  // 'a'

zip [1..5] ['A'..'E']        // [(1,'A'),(2,'B'),(3,'C'),(4,'D'),(5,'E')]

寻找直角边长小于等于10的直角三角形
[(a,b,c) | c <- [1..10], b <- [1..c], a <- [1..b], a^2+b^2==c^2]   // [(3,4,5),(6,8,10)]


## 类型
Prelude Data.Ratio> 11 % 29     // Integral a => Ratio a
:t 3 + 2                        // Num a => a

:t addThree                     // addThree :: Num a => a -> a -> a -> a


## 调用函数
odd 3
odd 6
compare 2 3
  返回  LT : Ordering
compare (sqrt 3) (sqrt 6)
  返回  LT : Ordering

factorial n = product [1..n]
factorial 50          // 30414093201713378043612608166064768844377641568960512000000000000


从类型签名可以看出一个 Haskell 函数是否带有副作用 —— 不纯函数的类型签名都以 IO 开头：
Prelude> :type readFile
readFile :: FilePath -> IO String

定义函数
add a b = a + b

## 分支
myDrop n xs = if n <= 0 || null xs
              then xs
              else myDrop (n - 1) (tail xs)

myDropX n xs = if n <= 0 || null xs then xs else myDropX (n - 1) (tail xs)

## 自定义数据类型
data BookInfo = Book Int String [String]
                deriving (Show)
-- 类型构造器名 BookInfo， 值构造器名 Book
myInfo = Book 23 "programing" ["foo", "bar"]

-- 类型别名
type CustomerID = Int
type ReviewBody = String
type BookRecord = (BookInfo, BookReview)
-- 类型别名只是为已有类型提供了一个新名字，创建值的工作还是由原来类型的值构造器进行。
-- 注：如果你熟悉 C 或者 C++ ，可以将 Haskell 的类型别名看作是 typedef 。

-- 代数数据类型
type CardHolder = String
type CardNumber = String
type Address = [String]
data BillingInfo = CreditCard CardNumber CardHolder Address
                 | CashOnDelivery
                 | Invoice CustomerID
                   deriving (Show)
--这个程序提供了三种付款的方式。如果使用信用卡付款，就要使用 CreditCard 作为值构造器，并输入信用卡卡号、信用卡持有人和地址作为参数。如果即时支付现金，就不用接受任何参数。最后，可以通过货到付款的方式来收款，在这种情况下，只需要填写客户的 ID 就可以了。
-- 类型构造器BillingInfo对应了三个值构造器。

## 模式匹配
sayMe :: (Integral a) => a -> String  
sayMe 1 = "One!"  
sayMe 2 = "Two!"  
sayMe 3 = "Three!"  
sayMe 4 = "Four!"  
sayMe 5 = "Five!"  
sayMe x = "Not between 1 and 5"

## guards
模式用来检查一个值是否合适并从中取值，而guard用来检查一个值的某个属性是否为真。
bmiTell weight height
  | weight / height^2 <= 18.5 = "you're underweight"
  | weight / height^2 <= 25.0 = "you're supposedly normal"
  | weight / height^2 <= 30.0 = "you're fat"
  | otherwise = "you're a whale"

max' a b
  | a > b = a
  | otherwise = b

## where
bmiTell weight height
  | bmi <= skinny = "you're underweight"
  | bmi <= normal = "you're supposedly normal"
  | bmi <= fat = "you're fat"
  | otherwise = "you're a whale"
  where bmi = weight / height^2
        (skinny, normal, fat) = (18.5, 25.0, 30.0)

## let
cylinder :: (RealFloat a) => a -> a -> a
cylinder r h = 
  let sideArea = 2 * pi * r * h
      topArea = pi * r^2
  in sideArea + 2 * topArea

## 递归 quicksort
quicksort [] = []
quicksort (x:xs) = 
  let smallerSorted = quicksort [a | a <- xs, a<=x]
      biggerSorted = quicksort[a | a <- xs, a > x]
  in smallerSorted ++ [x] ++ biggerSorted

## 高阶函数
本质上,haskell的所有函数都只有一个参数，所有多个参数的函数都是curried functions
applyTwice :: (a -> a) -> a -> a
applyTwice f x = f (f x)
applyTwice (+3) 10      // 16

map (+3) [1,5,3,1,6]      // [4,8,6,4,9]
filter (>3) [1,5,3,2,1,6]  // [5,6]
foldl (\acc x -> acc + x) 0 [2,3,4] // 9
foldl (+) 0 [2,3,4]   // 9
foldl是左折叠，当然还有右折叠foldr
思考： 用foldl实现map

## lambda
zipWith (\a b -> (a * 30 + 3) / b) [5,4,3,2,1] [1,2,3,4,5]  // [153.0,61.5,31.0,15.75,6.6]

map (\(a, b) -> a + b) [(1,2), (3,4), (5,6)]   // [3,7,11]

## 函数组合 composite
map (\x -> negate (abs x)) [5,-3,-6,7,-3,2,-19,24]
map (negate . abs) [5,-3,-6,7,-3,2,-19,24]


## point free
fn x = ceiling (negate (tan (cos (max 50 x))))
变成point free就是
fn = ceiling . negate . tan . cos . max 50


## modules
交互模式下  :m Data.List
源代码中    import Data.List
部分引入    import Data.List (nub, sort)


## typeclass
Eq, Ord, Show, Read, Enum, Range, Bounded, Num, Floating

class Eq a where
  (==) :: a -> a -> Bool
  (/=) :: a -> a -> Bool
  x == y = not (x /= y)
  x /= y = not (x == y)

data TrafficLight = Red | Yellow | Green

instance Eq TrafficLight where
  Red == Red = True
  Green == Green = True
  Yellow == Yellow = True
  _ == _ = False

## IO
main = do
  putStrLn "hello, what's your name"
  name <- getLine
  putStrLn ("hey " ++ name)

getLine :: IO String
putStrLn :: String -> IO ()