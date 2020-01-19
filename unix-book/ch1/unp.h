#ifndef __unp_h
#define __unp_h

#include <sys/types.h>  /* basic system data types */
#include <sys/socket.h> /* basic socket definitions */
#include <stdio.h>
#include <string.h>
#include <errno.h>

#include <sys/time.h> /* timeval{} for select() */
#include <time.h>     /* timespec{} for pselect() */
#include <unistd.h>

#include <netinet/in.h> /* sockaddr_in{} and other Internet defns */

#define LISTENQ 1024 /* 2nd argument to listen() */
#define MAXLINE 4096 /* max text line length */

#define SA struct sockaddr
#define bzero(ptr, n) memset(ptr, 0, n)
int Socket(int, int, int);
int Accept(int, SA *, socklen_t *);
void Bind(int, const SA *, socklen_t);
void Listen(int, int);
void Write(int, void *, size_t);
void Close(int);
#endif