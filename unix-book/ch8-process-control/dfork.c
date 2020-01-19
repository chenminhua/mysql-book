#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

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