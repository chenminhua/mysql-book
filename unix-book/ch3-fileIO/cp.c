#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

#define BUFFSIZE 4096
int main(int argc, char **argv)
{
  int fdr, fdw;
  char buffer[BUFFSIZE];
  int n;
  if ((fdr = open(argv[1], O_RDONLY)) < 0)
  {
    perror("can't open file");
  }
  if ((fdw = open(argv[2], O_WRONLY | O_CREAT, 00644)) < 0)
  {
    perror("can't open file");
  }
  while ((n = read(fdr, buffer, BUFFSIZE)) > 0)
  {
    n = write(fdw, buffer, n);
    if (n < BUFFSIZE)
    {
      break;
    }
  }
  close(fdr);
  close(fdw);
}