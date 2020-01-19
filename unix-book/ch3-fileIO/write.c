#include <fcntl.h>
#include <unistd.h>
#include <string.h>
int main(int argc, char **argv)
{
  int fd;
  fd = open("test", O_WRONLY | O_CREAT | O_APPEND, 00644);
  while (1)
  {
    write(fd, strcat(argv[1], "\n"), 2);
    sleep(1);
  }
}