#include <iostream>
#include <stack>

int main()
{
  std::stack<int> s;
  s.push(11);
  s.push(12);
  s.push(13);
  s.push(14);

  std::cout << s.top() << std::endl;
  s.pop();
  std::cout << s.top() << std::endl;
}