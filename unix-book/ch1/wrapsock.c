
#include "unp.h"

int Accept(int fd, struct sockaddr *sa, socklen_t *salenptr)
{
  int n;

again:
  if ((n = accept(fd, sa, salenptr)) < 0)
  {
#ifdef EPROTO
    if (errno == EPROTO || errno == ECONNABORTED)
#else
    if (errno == ECONNABORTED)
#endif
      goto again;
    else
      err_sys("accept error");
  }
  return (n);
}

void Bind(int fd, const struct sockaddr *sa, socklen_t salen)
{
  if (bind(fd, sa, salen) < 0)
    err_sys("bind error");
}

void Connect(int fd, const struct sockaddr *sa, socklen_t salen)
{
  if (connect(fd, sa, salen) < 0)
    err_sys("connect error");
}

/* include Listen */
void Listen(int fd, int backlog)
{
  char *ptr;

  /*4can override 2nd argument with environment variable */
  if ((ptr = getenv("LISTENQ")) != NULL)
    backlog = atoi(ptr);

  if (listen(fd, backlog) < 0)
    err_sys("listen error");
}
/* end Listen */