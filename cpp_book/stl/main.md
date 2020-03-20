http://cppstdlib.com

check docs in dash

### history
c++98, c++03, TR1, c++11

### vector
```
std::vector<int> v {7,5,16,8};

assign(), get_allocator(), operator=, constructor
access: front(), back(), at, operator[], data
迭代器：begin, cbegin, end, cend, rbegin, crbegin, rend, crend
capacity: empty, size, max_size, reverse, capacity, shrink_to_fit
modifiers: clear, insert, emplace, erase, push_back, pop_back, resize, swap

for (int a : v){}
```

### stack
```
stack<int> s;
element access: top
capacity: empty, size
modifiers: push, pop, emplace, swap
```