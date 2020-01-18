# 类型与值
```lua
print(type("hello world"))  --string
print(type(10.4*3))         --number
print(type(print))          --function
print(type(type))           --function
print(type(true))           --boolean
print(type(nil))            --nil
```

### 字符串
```lua
a = "one string"
print(#a)             -- 10 字符串长度
b = string.gsub(a, "one", "another") -- another string
print("a" .. "b")      -- ab 字符串拼接

"10" + 1   -- 10.0
"-5.3e-10" * "2"   -- -10.06e-09
print(10 .. 20)    -- 1020

line = io.read()
n = tonumber(line)      -- 将字符串转为数字
if n == nil then
  error(line .. " is not a valid number")
else
  print(n * 2)
end

tostring(10) == "10"      -- true
```

### 表 table
```lua
days = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"}
print(days[4])    --"Wednesday"

a = {x = 10, y=20}
a.x      -- 10

w = {x=0,y=0,label="console"}

for line in io.lines() do
  list = {next=list, value=line}
end

polyline = {color="blue", thickness=2, npoints=4, 
  {x = 0, y = 0},
  {x = -10, y = 0},
  {x = -10, y = 1},
  {x = 0, y = 1}}
polyline[2].x      -- -10
```

function, userdata(自定义类型)，thread(线程)

# 表达式
+,-,*,/,^,%;
<,>,<=,>=,==,~=;
and,or,not; 

false和nil为假，其他都是真。

# 语句
```lua
if ... then ... else ... end
if ... then ... end
while ... do ...end
repeat ... until ...
for ... do ... end

for i = 10,1,-1 do print(i) end
for i=1,10 do print(i) end
```

# 函数
```lua
s, e = string.find("hello lua users", "lua") -- 7,9

function maximum(a)
  local mi = 1      -- 最大值的索引
  local m = a[mi]   -- 最大值
  for i, val in ipairs(a) do
    if val > m then
      mi = i
      m = val
    end
  end
  return m, mi      -- 多返回值
end
print(maximum({8,10,23,12,5}))      -- 23 3

-- 变长参数
function add (...)
  local s = 0
  for i, v in ipairs{...} do      -- ipairs迭代数组元素
    s = s + v
  end
  return s
end
print(add(1,2,3,4,5))   -- 15

function fwrite (fmt, ...)
  return io.write(string.format(fmt, ...))
end
```

# 深入函数

# 迭代器与泛型 for

# 编译、执行与错误

# coroutine

# 完整的示例

