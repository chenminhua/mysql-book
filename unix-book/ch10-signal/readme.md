信号是软件中断

## signal函数
```c
#include <signal.h>
void (*signal(int signo, void (*func)(int)))(int);

更容易理解的写法
typedef void (*sig_t) (int);
sig_t signal(int sig, sig_t func);

signo为信号名
func为常量SIG_IGN(忽略信号),SIG_DFL(默认操作)或者回调函数指针
```

```c
static void sig_usr(int signo)
{
  if (signo == SIGUSR1)
    printf("received SIGUSR1\n");
}

int main()
{
  if (signal(SIGUSR1, sig_usr) == SIG_ERR)
    perror("can't catch SIGUSR1");
  for (;;)
    pause();
}
```

注意，当一个程序在后台执行时，例如 prog &,shell自动将后台进程对中断和退出信号的处理方式设置为忽略。

当一个进程调用fork时，其子进程继承父进程的信号处理方式。因为子进程在开始时复制了父进程内存，所以信号捕获函数的地址在子进程中是有意义的。

## 可重入函数
进程捕获到信号并对其处理，这时进程原本正在处理的正常指令序列就被临时中断了，它会优先执行信号处理程序中的指令。从信号处理程序返回后再继续执行捕获到信号时进程正在执行的正常序列。但是这个时候，进程不知道此前正执行到什么地方。如果进程正在执行malloc在堆内分配内存，而此时捕获到信号并处理完返回，继续malloc，会发生什么？因为malloc通常为它所分配的存储区维护一个链表，而插入信号处理程序时可能正在修改链表，导致程序被破坏。

unix说明了一些可重入的函数，这些函数是异步信号安全的，能够在信号处理程序中保证安全的调用。在使用系统函数前，最好确定你使用的函数是否可重入。下面几种函数往往是不可重入的

```
使用静态数据结构函数
调用malloc或者free的函数
标准IO库函数
```

## kill和raise

## alarm和pause

## sigprocmask

## sigpending

## 函数sigaction

## 函数sigsetjmp和siglongjmp

## 函数sigsuspend

## 函数abort

## 函数system

## sleep, nanosleep和clock_nanosleep

## sigqueue

## 作业控制信号

## 信号名和编号