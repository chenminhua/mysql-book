package com.company;

import java.util.concurrent.*;

public class CyclicBarrierExample {

    static class CyclicWorker implements Runnable {
        private CyclicBarrier barrier;

        public CyclicWorker(CyclicBarrier barrier) {
            this.barrier = barrier;
        }

        @Override
        public void run() {
            try {
                for (int i=0; i<3; i++) {
                    System.out.println("executed " + Thread.currentThread().getName());
                    barrier.await();
                }
            } catch (BrokenBarrierException | InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {

        CyclicBarrier barrier = new CyclicBarrier(5, new Runnable() {
            @Override
            public void run() {
                System.out.println("action... go again");
            }
        });

        for (int i = 0; i < 5; i++) {
            Thread t = new Thread(new CyclicWorker(barrier));
            t.start();
        }


    }
}



