1) 阻塞 I/O（blocking I/O）
2) 非阻塞 I/O （nonblocking I/O）
3)  I/O 复用 (select 和poll) （I/O multiplexing）
4) 信号驱动 I/O （signal driven I/O (SIGIO)）
5) 异步 I/O （asynchronous I/O (the POSIX aio_functions)）
前四种都是同步，只有最后一种才是异步 IO。
同步 IO 和异步 IO 的区别就在于：数据拷贝的时候进程是否阻塞！
阻塞 IO 和非阻塞 IO 的区别就在于：应用程序的调用是否立即返回！

在处理 IO 的时候，阻塞和非阻塞都是同步 IO。只有使用了特殊的 API 才是异步 IO。

