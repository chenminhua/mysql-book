1号进程通常是init进程，在自举过程结束结束时由内核调用。该进程的程序文件在unix的早期版本中是/etc/init，在较新版本是/sbin/init。init通常读取与系统有关的初始化文件(/etc/rc*文件或/etc/inittab文件，以及/etc/init.d中的文件)，并将系统引导到一个状态。init进程是一个普通的用户进程，但它是以超级用户特权运行。init会成为所有孤儿进程的父进程。

```c
#include <unistd.h>
pid_t getpid();
pid_t getppid();
uid_t getuid();
uid_t geteuid();
gid_t getgid();
gid_t getegid();
```

## fork
fork函数调用一次但是返回两次。区别是子进程的返回值为0，而父进程的返回值为新建子进程的pid。

```c
int globalVar = 0;
int main() {
    pid_t pid;
    int var = 0;

    if ((pid = fork()) < 0) {
        perror("fork failed");
    } else if (pid == 0) {   // child process
        var++;
        globalVar++;
    } else {   // parrent process
        sleep(2);
    }
    
    printf("pid = %d, var = %d, globalVar = %d\n", (int)getpid(), var, globalVar);
    return 0;
}
```

注意：如果运行父进程时重定向了父进程的文件描述符（比如stdin）时，子进程相应的文件描述符也会被重定向。并且，父子进程也会共享该文件的偏移量。

思考题：上面这段代码直接执行的结果是什么？如果将程序标准输出重定向到一个文件呢？为什么结果会有区别？

父子进程分别继续执行fork之后的指令，子进程获得父进程数据空间和堆栈副本。注意，子进程获得的是副本，他们并不共享这些存储空间（只共享正文段）。但是这带来一个问题，fork的时候可能需要为子进程复制大量的副本，为了解决这个问题，现在很多系统都使用copy-on-write的方式。

一般来说fork之后先执行父进程还是子进程是不确定的，这取决于内核的调度算法。在10.16节中会说明如何使用信号使父子进程同步。

fork常用的用法有：1.网络服务中，父进程接到请求，并fork子进程继续处理，自己则继续等待其他请求。2.一个进程要执行不同的程序，比如shell。

## 退出与终止
在最后调用_exit时，内核将退出状态转换为终止状态。如果子进程正常终止，则父进程可以获得子进程的终止状态。

如果父进程在子进程之前终止，子进程的父进程会变成init进程。其操作过程大致为：内核逐个检查所有活动进程，来判断它是否正要终止进程的子进程，如果是则收养。

如果父进程没有获取得到子进程的退出状态呢？内核为每个终止的子进程保存了一定量的信息，当其父进程调用wait或者waitpid时，可以得到这些信息。如果一个进程已经完全终止，但是其父进程还没有进行善后操作，则这个进程就成了僵死进程。ps命令下看到其状态为Z。

## wait和waitpid
wait: 如果其所有子进程都还在运行，则阻塞。如果一个子进程已经终止，正在等待父进程获取其终止状态，则wait函数取得该子进程的终止状态并立即返回。如果没有子进程则立即出错并返回。

waitpid可以等待指定pid的子进程

除此之外还有 waitid, wait3, wait4

## 两次fork避免僵死进程
先生个儿子，儿子生个孙子。然后杀了儿子，让孙子去做init的儿子。

```c
int main()
{
  pid_t pid;
  if ((pid = fork()) < 0)
  {
    perror("fork error");
  }
  else if (pid == 0)
  {
    if ((pid = fork()) < 0)
    {
      perror("fork error");
    }
    else if (pid > 0)
    {
      exit(0);
    }
    sleep(2);
    printf("second child, parent pid = %ld\n", (long)getppid());
    exit(0);
  }

  if (waitpid(pid, NULL, 0) != pid)
    perror("waitpid error");

  exit(0);
}
```

## exec函数
当进程调用一种exec函数时，该进程执行的程序完全替换为新程序，而新程序从其main函数开始执行。注意，exec调用并不创建新进程，exec只是用磁盘上的一个新程序替换当前进程的正文段，数据段，堆和栈。

一共有七种exec函数，除此之外，我们还可以使用用exec函数构造的popen和system之类的函数。

## system函数
```c
system("date > file");
```
system函数调用了fork, exec, waitpid，一个简单的实现如下


```c
int system(const char *cmdstring) {
    pid_t pid;
    int status;

    if (cmdstring == NULL) {
        return(1);      // a command processor with UNIX
    }

    if ((pid = fork()) < 0) {
        status = -1;
    } else if (pid == 0) {
        execl("/bin/sh", "sh", "-c", cmdstring, (char *)0);
        _exit(127);
    } else {
        while(waitpid(pid, &status, 0) < 0) {
            if (errno != EINTR) {
                status = -1;
                break;
            }
        }
    }

    return(status);
}
```

