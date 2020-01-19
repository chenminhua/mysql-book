在unix操作系统中，一切皆文件，所有的IO都是通过读写文件来实现的。在程序可以读写文件之前，程序必须打开文件来告知操作系统自己将对文件进行操作。打开文件的系统调用如果成功，操作系统会返回一个非负整数（文件描述符）给操作系统。当程序开始运行时，自动会打开三个文件：stdin,stdout,stderr，文件描述符分别为0，1，2

```c
// 打开文件，获取文件描述符
int open(const char *path, int oflag,...);
int openat(int fd, const char *path, int oflag,...);
int creat(const char *path, mode_t mode);  创建并打开文件

// 将标准输入写入标准输出
char buf[100];
int n;
while ((n = read(0, buf, 100)) > 0)
  write(1, buf, n);

// 关闭文件，释放文件描述符（断开程序与文件间的关联）
int close(int fd);
int read(int fd, void *buf, size_t nbytes);

unlink 移除文件，可以使用这个系统调用一行实现rm

off_t lseek(int fd, off_t offset, int whence);
// 定位到文件末尾
lseek(fd, 0L, 2);
//定位到文件开头
lseek(fd, 0L, 0);
```

大多数文件系统都会采用某种预读技术，当检测到正在进行顺序读取，系统会试图读入比应用所要求的更多数据。

思考题：如果两个进程同时打开同一个文件，并且开始写，会发生什么?

假如你没有使用O_APPEND选项打开文件，此时每个进程都有一个文件表项，但是共享一个v节点表项。假设现在文件有1500字节，此时A进程调用了lseek，将进程A的该文件当前偏移量设置为1500字节。然后内核切换进程，进程B也将偏移量设置在1500字节处，B向文件写入100字节，所以偏移量来到了1600。此时进程再次切换回了A，A不知道偏移量来到了1600，因此它开始从1500位置写，就覆盖了B写的东西。
问题出在先定位到文件末尾在写，这是两个分开的系统调用。解决这个问题的方法是将这两个操作合并成一个原子操作。只需要在打开文件时使用O_APPEND选项即可。

```c
#include <unistd.h>
// 复制文件描述符
int dup(int fd);
int dup2(int fd, intfd2);
```

## sync, fsync, fdatasync 缓冲区同步到磁盘
内核中设有缓冲区，大多数磁盘IO都在缓冲区进行，当我们向文件写入东西时会先写到缓冲区，然后排入队列，晚些时候再写入磁盘(delayed write)。为了保证磁盘上实际文件系统与缓冲区内容一致，Unix提供了下面三个函数。

```c
#include<unistd.h>
int fsync(int fd);
int fdatasync(int fd);
void sync(void);
```

## fcntl 改变打开文件的属性
```c
#include<fcntl.h>
int fcntl(int fd, int cmd, ...);
复制文件描述符
获取、设置文件描述符
获取、设置文件状态标志
获取、设置异步IO所有权
获取、设置记录锁
```

14章会用fcntl记录锁

## ioctl
```c
#include <sys/ioctl.h>
#inclued <termios.h>   // 终端io需要此头文件
int ioctl(int fd, int request, ...);

IO杂物箱，终端IO是ioctl使用最多的地方。18，19章会将ioctl用于终端设备。
```


# code time
实现一个cp

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

#define log_err(M, ...) fprintf(stderr, "[ERROR] (%s:%d: ) " M "\n", __FILE__, __LINE__, ##__VA_ARGS__)

int main(int argc, char *argv[]) {
	int f1, f2, n;
	char buf[100];
	if (argc != 3) 
		log_err("usage: cp from to");
	if ((f1 = open(argv[1], O_RDONLY, 0)) == -1)
		log_err("cp cant't open %s", argv[1]);
	if ((f2 = creat(argv[2], 0666)) == -1)
		log_err("cp: can't create %s, mode %03o", argv[2], 0666);
	while ((n = read(f1, buf, 100)) > 0) {
		if (write(f2, buf, n) != n) {
			log_err("cp: write error on file %s", argv[2]);
		}
	}
	return 0;
}
```

实现一个wc
```c
#define IN 1
#define OUT 0

int main() {
    int c, nl, nw, nc, state;
    state = OUT;
    nl = nw = nc = 0;
    while ((c = getchar()) != EOF) {
        ++nc;
        if (c == '\n') ++nl;
        if (c == ' ' || c == '\n' || c == '\t') {
            state = OUT;
        } else if (state == OUT) {
            state = IN;
            ++nw;
        }
    }
}
```
