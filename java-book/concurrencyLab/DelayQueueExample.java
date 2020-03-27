package com.company;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.DelayQueue;
import java.util.concurrent.Delayed;
import java.util.concurrent.TimeUnit;

public class DelayQueueExample {

    static class DelayObject implements Delayed {

        private String data;
        private long startTime;

        public DelayObject(String data, long delayInMilliseconds) {
            this.data = data;
            this.startTime = System.currentTimeMillis() + delayInMilliseconds;
        }

        @Override
        public long getDelay(TimeUnit unit) {
            long diff = startTime - System.currentTimeMillis();
            return unit.convert(diff, TimeUnit.MILLISECONDS);
        }

        @Override
        public int compareTo(Delayed o) {
            return Long.compare(this.startTime, ((DelayObject) o).startTime);
        }
    }

    public static void main(String[] args) {
        BlockingQueue<DelayObject> queue = new DelayQueue<DelayObject>();

        try {
            queue.put(new DelayObject("1", 1000));
            queue.put(new DelayObject("2", 2000));
            queue.put(new DelayObject("5", 5000));

            DelayObject object = queue.take();
            System.out.println(object.data);
            object = queue.take();
            System.out.println(object.data);
            object = queue.take();
            System.out.println(object.data);
        } catch(Exception e) {}
    }
}
