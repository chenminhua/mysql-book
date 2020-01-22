# CPU

## 平均负载

```sh
yum install sysstat / apt-get install sysstat

-P用于指定处理器，-P ALL表示查看所有cpu，1表示每秒打印一次记录
mpstat -P ALL 1

观察平均负载的变化
watch -d uptime

定位问题类型后，想要查看问题具体和哪个进程有关，使用pidstat
pidstat -u 1
```

cpu 平均负载高可能是 CPU 密集型进程导致的。但 cpu 平均负载高不代表 cpu 利用率高，也可能是 IO wait 高。uptime 可以用于查看平均负载，当发现负载高了，可以用 mpstat 查看负载升高原因，并利用 pidstat 定位导致问题的具体进程。

## 上下文切换

上下文切换类型：

- 进程切换。进程上下文包括虚拟内存、栈、全局变量等用户空间资源，还包括内核堆栈，寄存器等内核空间状态。
- 进程内系统调用，从用户态到内核态，再从内核态到用户态，发生了两次上下文切换。相比进程切换，系统调用不需要处理栈和虚拟内存等信息。
- 线程切换。不需要切换虚拟内存，但是栈和寄存器的保存和加载还是需要的。
- 中断。为了快速响应硬件的事件，中断处理会打断进程的正常调度和执行，转而调用中断处理程序。，此时需要将进程当前的状态保存下来，这样在中断结束后，进程仍可从原来的状态恢复运行。

线程是调度的基本单位，而进程是资源拥有的基本单位。

每次上下文切换都需要几十纳秒到数微秒的 cpu 时间。特别在进程上下文切换多的情况下，很容易导致大量 CPU 时间浪费，导致平均负载升高。另外，linux 通过 TLB 管理虚拟内存到物理内存的映射，进程的上下文切换需要更新虚拟内存，因此 TLB 也需要刷新，内存的访问也会变慢。特别是对于共享 TLB 的多处理器，刷新缓存不但影响了当前处理器的进程，还会影响共享缓存的其他处理器。通常 TLB 是不共享的

PS: 每个 CPU core 都可以在它的上下文下运行，每个 core 都有独立的 MMU。通常 TLB 也是每个核私有的。

**使用 vmstat 查看上下文切换**，特别关注的四列内容：

- cs（context switch）是每秒上下文切换的次数。
- in（interrupt）则是每秒中断的次数。
- r（Running or Runnable）是就绪队列的长度，也就是正在运行和等待 CPU 的进程数。
- b（Blocked）则是处于不可中断睡眠状态的进程数。

pidstat 加上 -w 选项，你就可以查看每个进程上下文切换的情况了。

```sh
wmstat 1
pidstat -w 1  # cswch 表示每秒自愿的上下文切换次数。 nvcswch表示非自愿上下文切换次数。
```

- 自愿上下文切换是指进程无法获取所需资源，导致的上下文切换。比如 IO、内存等系统资源不足，就会发生资源上下文切换。
- 非资源上下文切换则是进程被抢占等。

模拟

```sh
apt-get install sysbench / yum install sysbench

# 运行 20个线程，5分钟 的基准测试，模拟多线程切换
sysbench --threads=20 --max-time=300 threads run

# 观察上下文切换的变化情况，发现cs列飙升到100万。r列也飙升到10，
# us和sy（用户cpu使用率和内核cpu使用率）也很高，
# in上升到10000左右，说明中断处理也是潜在问题。
# 现在我们知道，系统r队列过长，运行和等待CPU的进程过多，导致大量上下文切换，引起cpu占用升高。
vmstat 1

# 从pidstat可以看出cpu使用率升高是sysbench导致的。但是看不出上下文切换的问题。是因为pidstat默认只能看到线程级别
pidstat -w -u 1

# 加上 -t 参数，可以看到线程级别
pidstat -w -u -t 1

# 观察中断变化
watch -d cat /proc/interrupts
```

每秒多少上下文切换比较正常？这取决于 CPU 性能。通常从数百到一万都是正常的，但如果出现数量级增加就有问题了。

- 如果 cswch 增加，说明在等资源，可能是 IO 问题。
- 如果是 nvcswch 增加，可能是在抢 CPU。
- 如果中断增加，说明 CPU 被中断占用增多，查看 /proc/interrupts 分析。

## CPU 使用率高

先借助 top、pidstat 等工具，确认是哪个进程引起的。再使用 perf 等工具排查具体函数。top 默认显示的是所有 CPU 的平均值，这个时候你只需要按下数字 1 ，就可以切换到每个 CPU 的使用率了。

- 用户 CPU 和 Nice CPU 高，说明用户态进程占用了较多的 CPU，所以应该着重排查进程的性能问题。
- 系统 CPU 高，说明内核态占用了较多的 CPU，所以应该着重排查内核线程或者系统调用的性能问题。
- I/O 等待 CPU 高，说明等待 I/O 的时间比较长，所以应该着重排查系统存储是不是出现了 I/O 问题。
- 软中断和硬中断高，应该着重排查内核中的中断服务程序。

top 不区分用户态和内核态，而 pidstat 可以帮助我们看得更详细。

- %usr 用户态 cpu 使用率
- %system 内核态 cpu 使用率
- %guest 虚拟机 cpu 使用率
- %wait 等待 cpu 使用率
- %cpu 总的 cpu 是有率

```sh
sudo apt-get install linux-tools-generic

# 实时查看占用cpu时钟最多的函数或指令，来查找热点函数。可以通过-g开启调用关系采样，通过-p指定采样进程。
perf top -g -p <pid>

# 录制与报告
perf record   # 会生成一个 perf.data 文件
perf report   # 打开 perf.data 文件进行分析
# 实际使用中，经常为 perf top 和 perf record 加上 -g 参数，开启调用关系的采样。
```

## 不可中断进程问题

不可中断状态，表示进程在和硬件交互，为了保护进程数据和硬件的一致性，系统不允许其他进程或中断打断这个进程。如果进程长时间处于这个状态，通常说明系统 IO 有问题。

- R 表示进程正在运行或正等待运行。
- D 是 Disk Sleep，即不可中断状态。
- Z 僵尸进程，也就是进程已经结束，但是父进程还没有回收它的资源。
- S 可中断睡眠状态，表示进程因为等待某个事件而被挂起。当事件到来它会被唤醒并进入 R 状态。
- I 空闲状态。内核线程不可中断睡眠。

不可中断进程问题常常表现为 iowait 升高，可以用 dstat 同时查看 cpu 和 IO 资源。

```sh
## dstat同时查看 cpu 和 IO
dstat

## top 观察是否有 D 状态进程
top

## 查看进程IO，-d可以查看io, -p指定进程
pidstat -d -p <pid> 1

## 跟进系统调用，如果root依然提示没有权限，很可能因为这个进程已经变成僵尸进程了
sudo strace -p <pid>

## 还可以用 perf 来查看函数调用栈
perf record -g
perf report
```

碰到 iowait 升高时，需要先用 dstat、pidstat 等工具，确认是不是磁盘 I/O 的问题，然后再找是哪些进程导致了 I/O。

## 僵尸进程问题

再看僵尸进程，这是多进程应用很容易碰到的问题。正常情况下，当一个进程创建了子进程后，它应该通过系统调用 wait() 或者 waitpid() 等待子进程结束，回收子进程的资源；而子进程在结束时，会向它的父进程发送 SIGCHLD 信号，所以，父进程还可以注册 SIGCHLD 信号的处理函数，异步回收资源。
如果父进程没这么做，或是子进程执行太快，父进程还没来得及处理子进程状态，子进程就已经提前退出，那这时的子进程就会变成僵尸进程。换句话说，父亲应该一直对儿子负责，善始善终，如果不作为或者跟不上，都会导致“问题少年”的出现。
通常，僵尸进程持续的时间都比较短，在父进程回收它的资源后就会消亡；或者在父进程退出后，由 init 进程回收后也会消亡。
一旦父进程没有处理子进程的终止，还一直保持运行状态，那么子进程就会一直处于僵尸状态。大量的僵尸进程会用尽 PID 进程号，导致新进程不能创建，所以这种情况一定要避免。

僵尸进程表示进程已经退出，但它的父进程还没有回收子进程占用的资源。短暂的僵尸状态我们通常不必理会，但进程长时间处于僵尸状态，就应该注意了，可能有应用程序没有正常处理子进程的退出。

```sh
# -a 表示输出命令行选项， -p 表示显示PID，-s 表示指定父进程
pstree -aps <pid>
```

## 软中断问题

软中断（softirq）CPU 使用率升高也是最常见的一种性能问题。为了让中断运行够快，Linux 将中断分成两部分，上半部分处理硬件相关工作，而下半部分通常交给内核线程延迟执行。

比如网卡收到数据后，会通过硬件中断通知内核，内核快速把网卡数据读到内存中并更新硬件寄存器的状态，最后再发送一个“软中断”信号。软中断信号唤醒相关的内核线程，内核线程从内存中找到网络数据，按照网络协议栈对数据进行处理，并把它发给应用程序。

上半部会打破 CPU 正在执行的任务，然后立即执行中断处理程序。而下半部以内核线程的方式执行，并且每个 CPU 都对应一个软中断内核线程，名字为 “ksoftirqd/CPU 编号”，比如说， 0 号 CPU 对应的软中断内核线程的名字就是 ksoftirqd/0。

软中断不只包括硬件设备中断处理程序的下半部，一些内核自定义的事件也属于软中断，比如内核调度和 RCU 锁（Read-Copy Update 的缩写，RCU 是 Linux 内核中最常用的锁之一）等。

- /proc/softirqs 提供了软中断的运行情况；
- /proc/interrupts 提供了硬中断的运行情况。

```sh
# 查看各种类型软中断在不同 CPU 上的累积运行次数：
cat /proc/softirqs

# 查看软中断内核线程工作情况，每个cpu core对应一个软中断内核线程
ps aux | grep softirq

# 模拟软中断升高
# hping3 模拟 SYN FLOOD 攻击，-S 表示设置 SYN包， -u100表示每隔100微秒发送一个网络帧
# hping3 是一个可以构造 TCP/IP 协议数据包的工具，可以对系统进行安全审计、防火墙测试等
hping3 -S -p 80 -i u100 192.168.0.30

# top查看发现虽然整体的cpu使用率还是很低，但是软中断升高
top

# 查看是哪个软中断升高，-d可以高亮出变化的部分，发现是网络的问题
watch -d cat /proc/softirqs

# sar 是一个系统活动报告工具，既可以实时查看系统的当前活动，又可以配置保存和报告历史统计数据。
# sar用来查看系统网络收发情况，可以看到BPS（字节吞吐），还能看到PPS(收发的网络帧数)。
# -n DEV 显示网络收发的报告。
#   IFACE 表示网卡
#   rxpck/s, txpck/s 表示每秒接收和发送的网络帧数，PPS
#   rxkB/s, txkB/s 表示每秒接收和发送的 kb 数，BPS
sar -n DEV 1

# 发现PPS很大，但BPS不大，那就 tcpdump 抓包看看
tcpdump -i eth0 -n tcp port 80

# 发现有很多SYN包，就定位到了SYN FLOOD问题，那么就封掉对应的IP就行了。
```

# 内存

- free, top 查看内存使用总体情况
- vmstat 观察内存动态变化，观看 cache/buffer 的使用，swap 的大小等等。
- 如果 cache/buffer 有异常，则使用 cachetop 观察各个进程的缓存读写命中。
- sar 查看内存总体变化情况 sar -r 1

```sh
free -h
```

- used 已经使用的内存，包含共享内存
- free 未使用内存
- shared 共享内存
- buff/cache 缓存和缓冲区大小
- available 新进程可用内存大小（包含 free 和可回收的缓存）

buffers 是内核缓冲区用到的内存，对应 /proc/meminfo 中的 buffers 的值。buffers 是对原始磁盘块的临时存储，也就是用来缓存磁盘的数据，通常不会特别大（20MB 左右）。这样，内核就可以把分散的写集中起来，统一优化磁盘的写入，比如可以把多次小的写合并成单次大的写等等。
cache 是内核页缓存和 slab 用的内存，对应 /proc/meminfo 中的 cached 与 SReclaimable 之和。Cached 是从磁盘读取文件的页缓存，也就是用来缓存从文件读取的数据。这样，下次访问这些文件数据时，就可以直接从内存中快速获取，而不需要再次访问缓慢的磁盘。SReclaimable 是 Slab 的一部分。Slab 包括两部分，其中的可回收部分，用 SReclaimable 记录；而不可回收部分，用 SUnreclaim 记录。

事实上，这里的 Buffer 是将要写入磁盘的数据的缓存，也可以用作读取磁盘数据的缓存。而 cache 是从文件读取数据的缓存，也可用作写文件的页缓存。

```sh
# cachestat 和 cachetop 都来自bcc-tools，基于内核的eBPF(extended Berkeley Packet Filters)
cachestat 1 3
# HITS，     表示缓存命中次数；
# MISSES，   表示缓存未命中的次数。
# DIRTIES    表示新增到缓存总的脏页数
# BUFFERS_MB 表示BUFFERS大小
# CACHED_MB  表示CACHE大小

## 默认按照缓存的命中次数（HITS）排序，展示了每个进程的缓存命中情况。具体到每一个指标，这里的 HITS、MISSES 和 DIRTIES
cachetop
```

磁盘是块设备文件，如果直接写磁盘则会跳过文件系统，而如果写文件则会利用文件系统，由文件系统来写磁盘。事实上这两种不同的读写方式使用的缓存就是分别为 buffer 和 cache。

```sh
top
```

- VIRT 进程虚拟内存大小，只要是进程申请过的内存，即使还没有真正分配物理内存，也会计算在内。
- RES 常驻内存大小，也就是实际使用的内存。（不包括 swap 和共享内存）。
- SHR 共享内存，比如与其他进程共同使用的内存，加载的动态链接库以及程序代码段等等。
- %MEM 进程使用的物理内存占系统总内存的百分比。

```sh
# 清理文件页，目录项，Inodes等各种缓存
echo 3 > /proc/sys/vm/drop_caches

# vmstat 查看内存使用
vmstat 1

# 读文件
dd if=/tmp/file of=/dev/null
# 直接读磁盘
dd if=/dev/sda1 of=/dev/null bs=1M count=1024
# 写文件
dd if=/dev/urandom of=/tmp/file bs=1M count=500
# 直接写磁盘
dd if=/dev/urandom of=/dev/sdb1 bs=1M count=2048
```

```sh
查看系统swappiness
sysctl vm.swappiness
或者
cat /proc/sys/vm/swappiness

临时禁用swap
sysctl -w vm.swappiness=0

永久禁用swap
echo "vm.swappiness = 0">> /etc/sysctl.conf
sysctl -p
```

# 文件系统与 IO 问题

```sh
# 查看文件系统
df -Th

# 查看inode使用情况（inode个数是有限的）
df -i /dev/nvme0n1p2

# man slabinfo
# 查看所有目录项和各种文件系统索引节点的缓存情况
cat /proc/slabinfo | grep -E '^#|dentry|inode'

# 查看占用内存最多的缓存类型
slabtop

# iostat
iosta -d -x 1

# iotop 查到 io 出问题的进程
iotop

# strace 抓对应进程的系统调用
```

# 网络问题

```
ifconfig
ip -s addr show dev eth0
```

- MTU 的默认大小是 1500.
- 网络收发的字节数，包数，错误数以及丢包情况。这些指标可以反映网络 IO 是否有问题。

ss 来查看套接字、网络栈、网络接口和路由表的信息。

```sh
# -l 表示只显示监听套接字
# -t 表示只显示 TCP 套接字
# -n 表示显示数字地址和端口（而不是名字）
# -p 表示显示进程信息
ss -ltnp
# 连接状态 Recv-Q 表示接收队列长度（套接字缓冲还没被应用程序取走的字节数）
# 连接状态 Send-Q 表示发送队列长度（还没被远端主机确认的字节数）
# 监听状态 Recv-Q 表示 syn backlog 的当前值
# 监听状态 Send-Q 表示 syn backlog 的最大值

# 查看协议栈统计信息
netstat -s
ss -s

# 查看网络吞吐
sar -n DEV 1

# 网卡带宽查看
ethtool eth0 | grep Speed

# 连通性和延迟查看
ping -c3 114.114.114.114
```