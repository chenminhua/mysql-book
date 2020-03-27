#ifndef __LINKEDLIST_H__
#define __LINKEDLIST_H__

#include <stdio.h>
template <class T>
class Node
{
  T value;
  Node<T> *next;

public:
  Node();
  Node(const T value) : value(value)
  {
    this->next = NULL;
  };
  T getValue() const
  {
    return this->value;
  }
  Node<T> *getNext() const
  {
    return this->next;
  }
  void setNext(Node<T> *next)
  {
    this->next = next;
  }
};

template <class T>
class LinkedList
{
public:
  Node<T> *head;

  LinkedList()
  {
    this->head = NULL;
  }

  Node<T> *getNodeByIndex(int index)
  {
    int i;
    Node<T> *cur = this->head;
    for (i = 0; i < index; i++)
    {
      cur = cur->getNext();
    }
    return cur;
  }

  void insertIntoHead(T value)
  {
    this->insertIntoIndex(value, 0);
  }

  void insertIntoIndex(T value, int index)
  {
    Node<T> *np = new Node<T>(value);
    if (index == 0)
    {
      np->setNext(this->head);
      this->head = np;
    }
    else
    {
      Node<T> *cur = this->getNodeByIndex(index - 1);
      np->setNext(cur->getNext());
      cur->setNext(np);
    }
  }

  void display() const
  {
    Node<T> *n = this->head;
    while (n != NULL)
    {
      printf("%d -> ", n->getValue());
      n = n->getNext();
    }
    printf("NULL\n");
  }
};
#endif
