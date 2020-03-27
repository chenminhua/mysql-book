package com.company;

import java.util.concurrent.CountDownLatch;

public class CountDownLatchExample {

    static class FirstBatchWorker implements Runnable {

        private CountDownLatch latch;

        public FirstBatchWorker(CountDownLatch latch) {
            this.latch = latch;
        }

        @Override
        public void run(){
            try {
                Thread.sleep(1000);
            } catch (Exception e) {}
            System.out.println("First batch executed");
            latch.countDown();
        }
    }

    static class SecondBatchWorker implements Runnable {

        private CountDownLatch latch;

        public SecondBatchWorker(CountDownLatch latch) {
            this.latch = latch;
        }

        @Override
        public void run() {
            try {
                latch.await();
                System.out.println("second batch executed");
            } catch (Exception e) { }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        CountDownLatch latch = new CountDownLatch(5);
        for (int i = 0; i < 5; i++) {
            Thread t = new Thread(new FirstBatchWorker(latch));
            t.start();
        }
        for (int i = 0; i < 5; i++) {
            Thread t = new Thread(new SecondBatchWorker(latch));
            t.start();
        }

    }
}
