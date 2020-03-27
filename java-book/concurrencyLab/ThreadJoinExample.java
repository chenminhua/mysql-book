package com.company;

public class ThreadJoinExample {

    public static void main(String[] args) {
//	    Thread t1 = createNewThread(1);
//        Thread t2 = createNewThread(2);
//        Thread t3 = createNewThread(3);
//        try {
//            t1.start();
//            t1.join();
//            t2.start();
//            t2.join();
//            t3.start();
//
//
//        } catch (Exception e) {}


        for (int i = 0; i < 10; i++) {
            int j = i;
            Thread t = new Thread(() -> {
                System.out.println("thread " + j + " is running");
            });
            t.start();
            try {
                t.join();
            } catch (Exception e) {}

        }

    }

    static Thread createNewThread(final int i) {
        Runnable task1 = new Runnable(){

            @Override
            public void run(){
                System.out.println("thread " + i + " is running");
                try {
                    Thread.sleep(1000L);
                } catch (Exception e) {}
            }
        };
        return new Thread(task1);
    }


}
