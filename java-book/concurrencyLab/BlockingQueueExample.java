package com.company;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.PriorityBlockingQueue;

public class BlockingQueueExample {
    public static void main(String[] args) {
        //ArrayBlockingQueueTest();
        //LinkedBlockingQueueTest();
        PriorityBlockingQueueTest();
        //DelayQueueTest();
    }

    public static void LinkedBlockingQueueTest() {
        LinkedBlockingQueue fairQueue = new LinkedBlockingQueue(10);

        new Thread(() -> {
            for (int i = 0; i < 9; i++) {
                fairQueue.add(i);
                try {
                    Thread.sleep(100L);
                } catch (Exception e) {}
            }
        }).start();

        new Thread(() -> {
            while (true) {
                try {
                    Object o = fairQueue.take();
                    System.out.println(o);
                } catch (Exception e) {}
            }
        }).start();
    }

    public static void ArrayBlockingQueueTest() {
        ArrayBlockingQueue fairQueue = new ArrayBlockingQueue(10, true);

        new Thread(() -> {
            for (int i = 0; i < 9; i++) {
                fairQueue.add(i);
                try {
                    Thread.sleep(100L);
                } catch (Exception e) {}
            }
        }).start();

        new Thread(() -> {
            while (true) {
                try {
                    Object o = fairQueue.take();
                    System.out.println(o);
                } catch (Exception e) {}
            }
        }).start();
    }

    static class User implements Comparable<User> {

        private final int age;
        private final String name;

        public User(int age, String name) {
            this.age = age;
            this.name = name;
        }

        @Override
        public int compareTo(User o) {
            return this.age > o.age ? -1 : 1;
        }
    }

    public static void PriorityBlockingQueueTest() {
        PriorityBlockingQueue queue = new PriorityBlockingQueue();

        queue.add(new User(1, "ch"));
        queue.add(new User(12, "chenminhua"));
        queue.add(new User(6, "chenmin"));
        queue.add(new User(4, "chen"));

        while (true) {
            try {
                User u = (User) queue.take();
                System.out.println(u.name);
            } catch (Exception e) {}
        }
    }

    public static void DelayQueueTest() {

    }
}
