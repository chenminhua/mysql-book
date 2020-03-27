package com.company;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ConditionDemo {
    public static void main(String[] args) {
        ProducerQueue<String> q = new ProducerQueue<>();
        Runnable p = () -> {
            for (int i = 0; i < 100; i++) {
                try {
                    Thread.sleep(500);
                    q.put("task" + i);
                } catch (Exception e) {}
            }
        };

        Runnable c = () -> {
            try {
                while(true) {
                    System.out.println("try");
                    System.out.println(q.take());
                }

            } catch (Exception e) {

            }
        };
        new Thread(p).start();
        new Thread(c).start();
    }
}

class ProducerQueue<T> {
    private final T[] items;
    private final Lock lock = new ReentrantLock();
    private Condition notFull = lock.newCondition();
    private Condition notEmpty = lock.newCondition();

    private int head, tail, count;

    public ProducerQueue(int maxSize) {
        items = (T[]) new Object[maxSize];
    }

    public ProducerQueue() {this(10);}

    public void put(T t) throws InterruptedException {
        lock.lock();
        try {
            while (count == getCapacity()) {
                notFull.await();
            }
            items[tail] = t;
            if (++tail == getCapacity()) {
                tail = 0;
            }
            ++count;
            notEmpty.signalAll();
        } finally {
            lock.unlock();
        }
    }

    public T take() throws InterruptedException {
        lock.lock();
        try {
            while(count == 0) {
                notEmpty.await();
            }
            T ret = items[head];
            items[head] = null;
            if (++head == getCapacity()) {
                head = 0;
            }
            --count;
            notFull.signalAll();
            return ret;
        } finally {
            lock.unlock();
        }
    }

    public int getCapacity() {
        return items.length;
    }

    public int size() {
        lock.lock();
        try {
            return count;
        } finally {
            lock.unlock();
        }
    }


}
