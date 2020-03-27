package com.company;

public class DeadLockSample2 {
    public static String s1 = "first";
    public static String s2 = "second";

    public static void main(String[] args) {

        Thread t1 = new Thread(() -> {
            synchronized (s1) {
                try {
                    System.out.println(Thread.currentThread().getName() + " obtained: " + s1);
                    Thread.sleep(1000);
                } catch (Exception e){
                    e.printStackTrace();
                }
                synchronized (s2) {
                    System.out.println(Thread.currentThread().getName() + " obtained: " + s2);
                    System.out.println("hhh");
                }
            }
        });

        Thread t2 = new Thread(() -> {
            synchronized (s2) {
                try {
                    System.out.println(Thread.currentThread().getName() + " obtained: " + s2);
                    Thread.sleep(1000);
                } catch (Exception e){
                    e.printStackTrace();
                }
                synchronized (s1) {
                    System.out.println(Thread.currentThread().getName() + " obtained: " + s1);
                    System.out.println("ddh");
                }
            }
        });

        t1.start();
        t2.start();
        try {
            t1.join();
            t2.join();
        } catch (Exception e) {}
    }
}
