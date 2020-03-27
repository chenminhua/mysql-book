package com.company;

import java.util.concurrent.*;

public class ExecutorFutureExample {

    static class Task implements Callable<Integer> {
        Integer value;
        Task(int i) {
            this.value = i;
        }

        @Override
        public Integer call() throws Exception {
            return value;
        }
    }

    public static void main(String[] args) {

        ExecutorService es = Executors.newCachedThreadPool();
        Future<Integer> r = es.submit(new Task(5));
        try {
          System.out.println(r.get());
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }
        es.shutdown();
    }
}
