#include <vector>
#include <iostream>
int main()
{
  std::vector<int> a;
  a.push_back(11);
  a.push_back(12);
  a.push_back(13);
  a.push_back(14);
  for (int b : a)
  {
    std::cout << b;
  }
}