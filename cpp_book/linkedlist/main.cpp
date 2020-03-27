#include <stdio.h>
#include "LinkedList.hh"

int main()
{
  Node<int> n1(10);
  printf("value %d\n", n1.getValue());
  Node<double> n2(12.2);
  printf("value %f\n", n2.getValue());
  LinkedList<int> l;
  l.insertIntoHead(12);
  l.insertIntoHead(11);
  l.insertIntoHead(9);
  l.insertIntoIndex(10, 1);
  l.display();
}
