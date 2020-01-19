#include <stdio.h>
#include <unistd.h>
int globalVar = 0;
int main()
{
    pid_t pid;
    int var = 0;

    printf("before fork\n");
    if ((pid = fork()) < 0)
    {
        perror("fork failed");
    }
    else if (pid == 0)
    { // child process
        var++;
        globalVar++;
    }
    else
    { // parrent process
        sleep(2);
    }

    printf("pid = %d, var = %d, globalVar = %d\n", (int)getpid(), var, globalVar);
    return 0;
}
