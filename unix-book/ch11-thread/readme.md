每个线程都包含有表示执行环境所必需的信息，其中包括线程ID，一组寄存器值，栈，调度优先级和策略，信号屏蔽字，errno变量，线程私有数据。进程的所有信息对该进程的所有线程都是共享的。

## 线程标识 (pthread_t结构体)
```c
#include <pthread.h>
int pthread_equal(pthread_t tid1, pthread_t tid2);

// 获取线程自身id
pthread_t pthread_self(void);
```

## 线程创建
```c
#include <pthread.h>
int pthread_create(
  pthread_t *restrict tidp,
  const pthread_attr_r *restrict attr,   // 用于定制不同的线程属性
  void *(*start_rtn)(void *),        // 线程执行入口函数
  void *restrict arg);               // 线程执行入口函数参数
```

## 线程终止
如果进程中的任意线程调用了exit、_Exit或者_exit，那么整个进程就会终止。而单个线程的退出有3种方式

```
线程可以简单的从其启动函数中返回，返回值是线程的退出码。
线程可以被同一个进程中的其他线程取消。
线程调用pthread_exit。

void pthread_exit(void *rval_ptr)
```

## pthread_join

```c
可以通过pthread_join自动把线程置于分离状态，这样资源就可以恢复。如果线程已经处于分离状态，pthread_join调用就会失败。
int pthread_join(pthread_t thread, void **rval_ptr)
rval_ptr可以让其他线程用来拿到该线程的退出状态
```

## pthread_cancel
```c
线程可以取消同一个进程中的其他线程
int pthread_cancel(pthread_t tid);

线程可以安排它退出时需要调用的函数，这样的函数称为线程清理处理程序
void pthread_cleanup_push(void(*rtn)(void *), void *arg);
void pthread_cleanup_pop(int execute);
```

## 线程同步
当多个线程共享相同内存时，需要确保每个线程看到一致的数据视图。如果每个线程都不共享内存，或者共享的内存都是只读的，就不会有一致性问题。但是当一个线程修改其他线程可能读写的变量时，我们就需要对这些线程进行同步。

#### 互斥量(mutex)
互斥量在本质上是一把锁，在访问共享资源前加锁，在访问完成后释放锁。加锁成功后，其他任何试图加锁的线程都会被阻塞直到当前线程释放该锁。

```c
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_trylock(pthread_mutex_t *mutex);
int pthread_mutex_unlock(pthread_mutex_t *mutex);
```

思考题：什么是死锁，如何避免死锁？
trylock，锁不上则释放已经加上的锁。使用timeout锁


#### 读写锁
当数据明显读多写少的时候，读写锁比互斥量要好很多。读写锁分为读锁和写锁。当一个线程获取读锁后，其他线程不能再获取这边锁的读锁或写锁；而几个线程可以同时获取读锁，但此时将不能加写锁。

```c
int pthread_rwlock_init(pthread_rwlock_t *lock, const pthread_rwlockattr_t *attr);

int pthread_rwlock_destroy(pthread_rwlock_t *lock);

int pthread_rwlock_rdlock(pthread_rwlock_t *rwlock);
int pthread_rwlock_wrlock(pthread_rwlock_t *rwlock);
int pthread_rwlock_unlock(pthread_rwlock_t *rwlock);

int pthread_rwlock_tryrdlock(pthread_rwlock_t *rwlock);
int pthread_rwlock_trywrlock(pthread_rwlock_t *rwlock);

带有超时的读写锁
pthread_rwlock_timedrdlock
pthread_rwlock_timedwrlock
```



#### 条件变量

#### 自旋锁
自旋锁与互斥量类似，但它不是通过休眠使进程阻塞，而是在获取锁之前一直处于忙等阻塞状态。自旋锁可用于以下情况：锁被持有时间短，而且线程不希望在重新调度上花太多时间。

自旋锁在非抢占式内核中非常有用，除了提供互斥机制外，自旋锁会阻塞中断，避免系统陷入死锁。但是在用户层，自旋锁并不是非常有用，除非运行在非抢占式实时调度中。否则，如果线程拥有自旋锁而且被调度离开cpu，进入休眠状态时，其他试图获得锁的线程都会被阻塞更长的时间。

事实上，很多互斥量的实现在试图获取互斥量的时候会自旋一段时间，当达到一定自旋次数仍然没有获取锁时才会休眠。另外，由于上下文切换越来越快，也使得自旋锁只在特定情况下有用。

```c
int pthread_spin_init(pthread_spinlock_t *lock, int pshared);
int pthread_spin_destroy(pthread_spinlock_t *lock);

int pthread_spin_lock(pthread_spinlock_t *lock);
int pthread_spin_trylock(pthread_spinlock_t *lock);
int pthread_spin_unlock(pthread_spinlock_t *lock);
```

#### barrier
屏障是用户协调多个线程并行工作的同步机制。屏障允许每个线程等待，直到所有合作线程都达到某个点，然后从该点继续执行。pthread_join函数就是一种屏障，允许一个线程等待，直到另一个线程退出。

但是屏障对象概念更广，其允许任意数量的线程等待，直到所有线程处理完成工作，而线程不需要退出。所有线程到达屏障后可以接着工作。