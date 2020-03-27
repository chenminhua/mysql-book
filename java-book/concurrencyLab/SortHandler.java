package com.company;

@FunctionalInterface
public interface SortHandler<T> {
    void sort(T t);
}
