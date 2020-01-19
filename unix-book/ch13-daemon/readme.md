## 守护进程的特征

ps -efj 查看进程，内核守护进程用[]括起来。比如[kthreadd]内核守护进程就是用来创建其他内核进程的，所以其他内核进程的父进程都为[kthreadd]。对于需要在进程上下文执行工作但是却不被用户层进程上下文调用的每一个内核组件，通常都会有它自己的内核守护进程。比如[kswapd]守护进程就是负责内存换页的，[flush]就是负责将内存脏页面冲洗至磁盘的。比如 rsyslogd 被用于记录日志,inetd 用于侦听网络接口。nfsd,nfsiod,lockd,rpciod 等提供对网络文件系统（NFS）的支持。cron 也是守护进程。

## 编程规则

1.调用 umask 将文件模式创建屏蔽字设置成一个已知值（通常为 0）。由继承得来的文件模式创建屏蔽字可能会被设置为拒绝某些权限。 2.调用 fork,然后使父进程 exit。 3.调用 setsid 创建一个新会话，使得调用进程称为新会话的首进程，以及进程组组织，并且没有控制终端。 4.将当前工作目录更改为根目录。 5.关闭不再需要的文件描述符

## 出错记录

守护进程大多使用 syslog 记录日志和错误信息。有以下 3 中产生日志消息的方法：1.内核进程调用 Log 函数。2.大多数用户进程都通过调用 syslog 函数来产生日志消息，这些消息会被发送到/dev/log。3.用户进程可以将日志消息发向 UDP 端口 514。

通常 syslogd 守护进程会读取这三种日志，它会在启动时读取配置文件（通常在/etc/syslog.conf），并决定不同种类消息被发往何处。

```c
void openlog(const char *ident, int option, int facility);
void syslog(int priority, const char *format, ...);
void closelog(void);
int setlogmask(int maskpri);
```

## 守护进程的惯例

如果守护进程使用锁文件，锁通常放在/var/run 目录，名字通常是 name.pid，例如 cron 进程锁文件就是/var/run/crond.pid。

守护进程的配置文件通常在/etc 目录下。

守护文件可以用命令行启动，但是通常它们由系统初始化脚本启动（etc/rc*或者/etc/init.d/*）,如果希望守护进程能够自动重启，则可以在/etc/inittab 中为该守护进程维护 respawn 记录，这样 init 就会重启它。
