package com.company;

import java.util.Arrays;

public class FunctionalInterfaceExample {
    public static void main(String[] args) {
        Integer[] array = {1, 4, 3, 2};
        Arrays.sort(array, (v1, v2) -> v1 - v2);        // 正序排序
        for (Integer i : array) {
            System.out.print(i);
        }
    }
}
