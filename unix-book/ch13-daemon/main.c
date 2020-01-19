#include <syslog.h>
#include <fcntl.h>
#include <sys/resource.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

void daemonize(const char *cmd) {
  int i, fd0, fd1, fd2;
  pid_t pid;
  struct rlimit r1;
  struct sigaction sa;

  // clear file creation mask
  umask(0);

  // get maximum number of fd
  if (getrlimit(RLIMIT_NOFILE, &r1) < 0){
    printf("%s, can't get file limit", cmd);
    exit(1);
  }

  if ((pid = fork()) < 0) {
    printf("%s, can't fork", cmd);  
  } else if (pid != 0){
    exit(0);
  }
  setsid();
  sa.sa_handler = SIG_IGN;
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = 0;
  if(sigaction(SIGHUP, &sa, NULL) < 0) {
    printf("%s: can't ignore SIGHUP", cmd);
  }
  if ((pid = fork()) < 0) {
    printf("%s: can't fork", cmd);
  } else if (pid != 0) {
    exit(0);
  }

  if (r1.rlim_max == RLIM_INFINITY) {
    r1.rlim_max = 1024;
  }

  // 关闭所有文件描述符
  for (i = 0; i < r1.rlim_max; i++) {
    close(i);
  }

  // attach fd 0,1,2 to /dev/null
  fd0 = open("/dev/null", O_RDWR);
  fd1 = dup(0);
  fd2 = dup(0);

  openlog(cmd, LOG_CONS, LOG_DAEMON);
  if(fd0 != 0 || fd1 != 1 || fd2 != 2) {
    syslog(LOG_ERR, "unexpected fd %d, %d, %d", fd0, fd1, fd2);
    exit(1);
  }
}

int main() {
  daemonize("test daemon");
  sleep(100000);
  return 0;
}

