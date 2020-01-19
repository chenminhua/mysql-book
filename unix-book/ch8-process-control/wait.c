#include <sys/wait.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void pr_exit(int status)
{
  if (WIFEXITED(status))
  {
    printf("normal termination, exit status = %d\n", WEXITSTATUS(status));
  }
  else if (WIFSIGNALED(status))
  {
    printf("abnormal termination, signal number = %d%s\n", WTERMSIG(status), WCOREDUMP(status) ? " (core file genetated)" : "");
  }
}

int main()
{
  pid_t pid;
  int status;

  if ((pid = fork()) < 0)
  {
    perror("fork error");
  }
  else if (pid == 0)
  {
    exit(7); // 子进程退出
  }

  if (wait(&status) != pid)
  {
    perror("wait error");
  }
  pr_exit(status);

  if ((pid = fork()) < 0)
  {
    perror("fork error");
  }
  else if (pid == 0)
  {
    abort();
  }

  if (wait(&status) != pid)
  {
    perror("wait error");
  }
  pr_exit(status);

  if ((pid = fork()) < 0)
  {
    perror("fork error");
  }
  else if (pid == 0)
  {
    status /= 0;
  }

  if (wait(&status) != pid)
  {
    perror("wait error");
  }
  pr_exit(status);

  exit(0);
}
