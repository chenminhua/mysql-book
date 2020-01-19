socket 是通信端点的抽象。

<sys/socket.h>
int socket(int domain, int type, int protocol);
若成功，返回文件描述符；若失败，返回-1。

AF_INET ipv4;
AF_INET6 ipv6;
AF_UNIX unix;

SOCK_DGRAM 固定长度，无连接的，不可靠的报文。UDP
SOCK_RAW IP 协议的数据报
SOCK_SEQPACKET 固定长度的，有序的，可靠的，面向连接的报文
SOCK_STREAM 有序的，可靠的，双向的，面向连接的字节流。TCP
