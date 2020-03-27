package com.company;

class MonitorObject {};

public class ThreadSingalExample {
    MonitorObject mo = new MonitorObject();

    public void doWait() {
        synchronized (mo) {
            try {
                mo.wait();
            } catch (InterruptedException e) {}
        }
    }

    public void doNotify() {
        synchronized (mo) {
            mo.notify();
        }
    }

    public static void main(String[] args) {
        ThreadSingalExample tst = new ThreadSingalExample();

        Thread t1 = new Thread() {
            @Override
            public void run() {
                try {
                    System.out.println("before notify");
                    Thread.sleep(10000);
                    System.out.println("starting notify");
                    tst.doNotify();
                    System.out.println("after notify");
                } catch (Exception e){}
            }
        };

        Thread t2 = new Thread() {
            @Override
            public void run() {
                System.out.println("before notified");
                tst.doWait();
                System.out.println("after notified");
            }
        };

        t1.start();
        t2.start();
    }
}
