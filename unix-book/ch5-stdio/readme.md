标准IO库是dennis ritchie在1975年左右编写的。令人惊讶的是，35年来，几乎没有对标准IO库进行修改。

在第三章，所有的IO都是围绕文件描述符的。而标准IO库则是围绕流(stream)进行的。

对一个进程预定义了三个流：标准输入，标准输出，标准错误，分别对应的文件描述符为STDIN_FILENO,STDOUT_FILENO,STDERR_FILENO；并且可以通过预定义文件指针stdin,stdout,stderr来引用(在stdio.h中)。

标准IO提供了3种缓冲：

```c
1.全缓冲，在填满标准IO缓冲区后才进行实际IO操作。stdin和stdout如果不指向交互式设备，则是全缓冲的。
2.行缓冲，当遇到换行符的时候进行实际IO操作。终端设备是行缓冲的。
3.无缓冲，标准错误是不带缓冲的

#include <stdio.h>
// setbuf可以用于打开和关闭缓冲机制，其中buf必须指向长度为BUFSIZ的缓冲区，BUFSIZ定义在<stdio.h>
void setbuf(FILE *restrict fp, char *restrict buf);
// 使用setvbuf可以精确地说明所需的缓冲类型
int setvbuf(FILE *restrict fp, char *restrict buf, int mode, size_t size);

// 通过fflush可以在任何时候强制冲洗一个流，将流中所有未写的数据传送至内核。如果fp为NULL,会导致所有输出流全部被冲洗。
int fflush(FILE *fp);
```

## 打开(关闭)流
```c
#include <stdio.h>
// 打开一个流
FILE *fopen(const char *restrict pathname, const char *restrict type);

// 在一个指定流上打开一个指定文件，如果这个流已经打开则先关闭这个流。一般用于将一个指定文件打开为一个预定义的流
FILE *freopen(const char *restrict pathname, const char *restrict type, FILE *restrict fp);

// 取一个已有的文件描述符，并使一个标准IO流与其结合。常常用于创建管道和网络通信函数返回的文件描述符(不在文件系统中)。
FILE *fdopen(int fd, const char *type);

// 关闭流，成功返回0，出错返回EOF
int fclose(FILE *fp);
```

## 读写流
```c
#include<stdio.h>
// 一次读一个字符
int getc(FILE *fp);
int fgetc(FILE *fp);
int getchar(void);  //等同于 getc(stdin)

// 一次写一个字符
int putc(int c, FILE *fp);
int fputc(int c, FILE *fp);
int putchar(int c);  //等同与 putc(c, stdout)

// 每次读一行
char *fgets(char *restrict buf, int n, FILE *restrict fp); // 从指定流读取，n为指定缓冲区大小
char *gets(char *buf);   // 从标准输入读取，不推荐使用

// 每次写一行
int fputs(const char *restrict str, FILE *restrict fp);
int puts(const char *str);
```

动手题：分别使用 read,wirte; fgetc,fputc; getc,putc; fgets,fputs测试从stdin复制内容到stdout的效率。

## 二进制IO
```c
#include <stdio.h>
size_t fread(void *restrict ptr, size_t size, size_t nobj, FILE *restrict fp);
size_t fwrite(const void *restrict ptr, size_t size, size_t nobj, FILE *restrict fp);
```

## 定位流
ftell, fseek, fgetpos, fsetpos

## 格式化IO
```c
int printf(const char *restrict format, ...);  // 格式化写入stdout
int fprintf(FILE *restrict fp, const char *restrict format, ...);  // 写入指定流
int dprintf(int fd, const char *restrict format, ...);   // 写入指定文件描述符

int sprintf(char *restrict buf, const *restrict format, ...);    // 格式化字符数组写入buf数组(可能会导致缓冲区溢出)
int snprintf(char *restrict buf, size_t n, const char *restrict format, ...);  //防溢出版本的sprintf
```

## 临时文件
```c
// 每次调用tmpnam都会返回一个有效路径名
char *tmpnam(char *ptr);

// tmpfile创建一个临时二进制文件，在关闭该文件或程序结束时自动删除这种文件。
FILE *tmpfile(void);
```

## 内存流

## 标准IO的不足与替代软件
标准IO的一个不足是效率不高，这与它需要复制的数据量有关。当使用fgets和fputs时，通常需要复制两次数据：一次是在内核和标准IO缓冲区之间，一次是在标准IO缓冲区和用户程序行缓冲之间。快速io库fio避免了这一点，其方法是使读一行的函数返回指向该行的指针，而不是复制到另一个缓冲区。标准IO的另一个替代软件是ASI(Alloc Stream Interface)，其使用了映射文件(mmap,见第18章)。

# code time
基于stdio实现一个cat

```c
int main(int argc, char *argv[]) {
    FILE *fp;
    void filecopy(FILE *, FILE *);

    if (argc == 1) {
        filecopy(stdin, stdout);
    }else {
        while (--argc > 0) {
            if ((fp = fopen(*++argv, "r")) == NULL) {
                printf("can't open %s\n", *argv);
                exit(1);
            } else {
                filecopy(fp, stdout);
                fclose(fp);
            }
        }
    }
    return 0;
}

void filecopy(FILE *ifp, FILE *ofp) {
    int c;
    while ((c = getc(ifp)) != EOF)
        putc(c, ofp);
}
```
