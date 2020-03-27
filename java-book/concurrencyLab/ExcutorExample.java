package com.company;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class ExcutorExample {
    static class Task implements Runnable {
        int id;
        public Task(int id) {
            this.id = id;
        }

        @Override
        public void run() {
            System.out.println("hello cachedThread " + id + " "
                    + Thread.currentThread().getName());
        }
    }

    // 周期任务
    static void singleThreadScheduledTest() {
        ScheduledExecutorService es = Executors.newSingleThreadScheduledExecutor();
        es.scheduleAtFixedRate(new Task(1), 0, 1, TimeUnit.SECONDS);
    }

    // 周期任务with pool
    static void threadPoolScheduledTest() {
        ScheduledExecutorService es = Executors.newScheduledThreadPool(3);
        es.scheduleAtFixedRate(new Task(1), 0, 1, TimeUnit.SECONDS);
    }

    static void threadPoolExecutorTest() {
        ThreadPoolExecutor tpe = new ThreadPoolExecutor(
                5,
                5,
                60, TimeUnit.SECONDS,
                new LinkedBlockingQueue<Runnable>());
        // 注意，如果这里用的是arrayBlockingQueue的话可能会遇到RejectExecution
        for (int i = 0; i < 100; i++) {
            //tpe.execute(new Task(i));
            tpe.execute(() -> {
                System.out.println("ok");
            });
        }
        //tpe.shutdown();
    }

    public static void main(String[] args) {
        threadPoolExecutorTest();

        List<Integer> list = new ArrayList<>();
        list.add(100);
        list.add(10);
        list.add(1000);
        List<Integer> l = list.stream().filter(it -> it != 10).collect(Collectors.toList());
        System.out.println(l);
    }
}
