## 查看文件及目录stat

```c
#include <sys/stat.h>
int stat(const char *restrict pathname, struct stat *restrict buf);
int fstat(int fd, struct stat *buf);
int lstat(const cahr *restrict pathname, struct stat *restrict buf);
int fstatat(int fd, const char *restrict pathname, struct stat *restrict buf, int flag);

struct stat {
  mode_t    st_mode;    // 文件类型和模式
  ino_t     st_ino;     // i-node number
  dev_t     st_dev;     // device number
  dev_t     st_rdev;    // device number for special files
  nlink_t   st_nlink;   // number of links
  uid_t     st_uid;     // user id of owner
  git_t     st_gid;     // group id of owner
  off_t     st_size;    // size in bytes
  struct timespec   st_atime;    // last access time
  struct timespec   st_mtime;    // last modify time
  struct timespec   st_ctime;    // last file status change time
  blksize_t  st_blksize;         // best I/O block size
  blkcnt_t   st_blocks;          // num of disk blocks allocated
}
```

## access和faccessat
```c
#include <unistd.h>
int access(const char *pathname, int mode);
int faccessat(int fd, const char *pathname, int mode, int flag);
```

## chmod, fchmod, fchmodat

## 文件截断 truncate, ftruncate

## 文件系统
每一种文件系统都有其各自特征。例如，大部分unix文件系统支持大小写敏感的文件名，但是在mac osx上，hfs的文件系统是大小写不敏感的。

我们可以把一个磁盘分成一个或多个分区，每个分区一个文件系统。i节点是固定长度的记录项，其中记录有关文件的大部分信息。可以有多个文件指向同一个i节点，每个i节点都有一个链接计数，只有当链接计数为0时，才可以删除文件（释放文件占用的数据块）。这也是为什么删除一个文件的函数被称为unlink而不是delete的原因。

ln不能跨文件系统。

当不更换文件系统时，对文件进行重命名（比如mv）,只需要构造一个新的符号链接，并将老的符号链接删掉就行（这就是为啥mv比cp快）。

每个目录都有一个本身的链接，一个.链接，如果其还有子目录，则每个子目录都会有一个..链接指向这个父目录。（这就是为啥不能直接删除目录）

## 函数link, linkat, unlink, unlinkat, remove
对于文件,remove等于unlink; 对于目录,remove等于rmdir

## rename和renameat