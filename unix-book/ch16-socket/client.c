#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
  // 声明变量
  int sockfd;
  struct sockaddr_in server;
  struct hostent *hp;

  // 打开socket
  if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
  {
    printf("can't open socket");
    exit(1);
  }

  server.sin_family = AF_INET;
  server.sin_port = htons(5000);

  if ((hp = gethostbyname(argv[1])) == 0)
  {
    printf("gethostbyname failed");
    close(sockfd);
    exit(1);
  }

  memcpy(&server.sin_addr, hp->h_addr, hp->h_length);

  // connect
  if (connect(sockfd, (struct sockaddr *)&server, sizeof(server)) < 0)
  {
    perror("connect failed");
    close(sockfd);
    exit(1);
  }

  // send
  if (send(sockfd, argv[2], 100, 0) < 0)
  {
    perror("send failed");
    close(sockfd);
    exit(1);
  }
  close(sockfd);
  return 0;
}
