编排是容器云的灵魂，也是 k8s 社区持久生命力的源泉。

Cloud Foundry 等项目开启了以 pass 为核心的构建平台层服务能力的变革。CF 的核心就是一套应用的打包和分发机制，利用 cgroups 和 namespace 为每个应用单独建立隔离运行环境。这种隔离运行环境的应用托管能力就是 Pass 项目的核心能力，而这个隔离环境就是容器。而 docker 容器的致胜法宝是 Docker 镜像，把程序和运行环境打包起来。

- 2014 年，Kubernetes 诞生。
- 2015 年，Docker 公司将 Libcontainer 捐出，并改名为 RunC 项目，交由一个完全中立的基金会管理。
- 以 RunC 为依据，制定一套容器和镜像的标准和规范，OCI（ Open Container Initiative ），将容器运行时和镜像的实现从 Docker 项目中剥离出来。
- CNCF 基金会：以 K8s 为基础，建立一个由开源基础设施领域厂商主导的、按照独立基金会方式运营的平台级社区。
- CNCF 成员项目： prometheus, fluentd, opentracing, CNI 等。
- k8s 推进民主化架构：从 API 到容器运行时的每一层，k8s 都提供了可扩展的插件机制。

容器社区中大量的、基于 Kubernetes API 和扩展接口的二次创新工作，比如：目前热度极高的微服务治理项目 Istio；被广泛采用的有状态应用部署框架 Operator；还有像 Rook 这样的开源创业项目，它通过 Kubernetes 的可扩展接口，把 Ceph 这样的重量级产品封装成了简单易用的容器存储插件。

## cgroups 与 namespace

Cgroups 用来制造约束，而 Namespace 则用来修改进程视图。Docker 容器，其实就是启用了多个 Namespace 的进程，而进程能够使用的资源则受到 Cgroups 限制。

#### namespace

```sh
# -it 表示要分配一个tty，跟容器的标准输入关联，而 /bin/bash 则是docker里面的程序
docker run -it busybox /bin/sh
```

Namespace 的使用方式也很有意思，比如 PID Namespace。

```c
// 在 Linux 中创建进程的系统调用 clone。
int pid = clone(main_function, stack_size, SIGCHLD, NULL);

//如果我们制定 CLONE_NEWPID 参数，这时候新的进程将会看到一个全新的进程空间。他们都会认为自己是 1 号进程，当然其实并不是。
int pid = clone(main_function, stack_size, CLONE_NEWPID | SIGCHLD, NULL);
```

除了 PID Namespace，linux 还提供了 Mount, UTS, IPC, Network, User 这些 Namespace。比如 Mount Namespace 用于让被隔离进程只看见当前 Namespace 挂载点信息，Network Namespace 用于让被隔离进程只看到当前 Namespace 里的网络设备和配置。在创建容器进程时，指定了一组 Namespace 参数，这样容器就只能看到当前 Namespace 限定的资源和状态。

- 对于虚拟机来说，Hypervisor 软件通过硬件虚拟化模拟出操作系统需要的各种硬件，然后在其上安装了一个新操作系统。
- 而在使用 Docker 的时候，并没有一个真正的虚拟机的存在，只是通过 Namespace 隔离了不同进程，Docker 项目在这里只是一些辅助工作，甚至是可以去掉的。
- 相比于虚拟机，docker 启动更快，内存占用更少，还省下了系统调用经过虚拟化软件拦截的开销。

#### Cgroups（Control Groups）

Cgroups 最主要的作用是限制一个进程组能够使用的资源上限，包括 CPU, 内存，磁盘，网络等。Linux 中，Cgroups 给用户暴露出来的接口是文件系统，/sys/fs/cgroup 路径下。

```sh
mount -t cgroup
```

可以看到，/sys/fs/cgroup 下面有很多诸如 cpuset, cpu, memory 这样的子目录（子系统）。这些都是可以被 Cgroups 限制的资源种类。比如对 cpu 子系统来说

```sh
ls /sys/fs/cgroup/cpu
```

下面我们试着手动创建一个控制组

```sh
cd /sys/fs/cgroup/cpu
mkdir container
```

然后我们进入 container 目录，可以看到操作系统在这个目录下自动生成该子系统对应的资源限制文件。下面我们试着执行一个会把 cpu 打满的脚本, 看到其 pid 为 10805

```sh
while : ; do : ; done &
```

我们查看下 container 组下的 cpu.cfs_quota_us，发现是-1，表示没有什么限制。我们将其改成 20000, 而 cpu.cfs_quota_us 依旧是 100000。（表示每 100ms 只能使用 20ms 的 cpu 时间，也就是 20%的 cpu 利用率）

```sh
echo 20000 > /sys/fs/cgroup/cpu/container/cpu.cfs_quota_us
```

在然后，我们把上面的死循环进程的进程号 10805 写入 container 组的 tasks 文件下，将其加入资源限制组。

```sh
echo 10805 > /sys/fs/cgroup/cpu/container/tasks
```

说白了，Cgroups 就是一个子系统目录加上一组资源限制文件的组合。

```
docker run -it --cpu-period=100000 --cpu-quota=20000 ubuntu /bin/bash
```

- 在 k8s 中如何看资源使用情况？ 使用 metrics-server，然后 k top pod。

## rootfs 与容器镜像

https://coolshell.cn/articles/17010.html

容器三驾马车： namespace, Cgroups, changeRoot。rootfs 只是操作系统包含的文件，不包含内核，容器共享 OS 内核。

这就意味着，如果你的应用程序需要配置内核参数、加载额外的内核模块，以及跟内核进行直接的交互，你就需要注意了：这些操作和依赖的对象，都是宿主机操作系统的内核，它对于该机器上的所有容器来说是一个“全局变量”，牵一发而动全身。这也是容器相比于虚拟机的主要缺陷之一。

docker 引入了 layer 的概念。用户制作镜像的每一步都会生成一个层，也就是一个增量 rootfs。这用到了 Union File System。Docker 默认使用 AuFS 这个联合文件系统。你可以通过 docker info 命令查看到这个信息。

```
docker image inspect ubuntu:latest
"RootFS": {
    "Type": "layers",
    "Layers": [
        "sha256:cc967c529ced563b7746b663d98248bc571afdb3c012019d7f54d6c092793b8b",
        "sha256:2c6ac8e5063e35e91ab79dfb7330c6154b82f3a7e4724fb1b4475c0a95dfdd33",
        "sha256:6c01b5a53aac53c66f02ea711295c7586061cbe083b110d54dafbeb6cf7636bf",
        "sha256:e0b3afb09dc386786d49d6443bdfb20bc74d77dcf68e152db7e5bb36b1cca638"
    ]
}
```

可以看到，每层都是 ubuntu 操作系统文件与目录的一部分，而在使用镜像时，docker 会把这些增量联合挂载在一个统一的挂载点上。这个挂载点就是 /var/lib/docker/aufs/mnt/，比如 /var/lib/docker/aufs/mnt/6e3be5d2ecccae7cc0fcfa2a2f5c89dc21ee30e166be823ceaeba15dce645b3e，这个目录下面就是一个 ubuntu 操作系统。而至于这五个镜像如何被挂载成一个完整的 ubuntu 文件系统的？则可以在 /sys/fs/aufs 下面找到。

```sh
cat /proc/mounts | grep aufs
```

我们可以看到，镜像的层都放在 /var/lib/docker/aufs/diff 目录下，然后被联合挂载到 /var/lib/docker/aufs/mnt 里面。

## Pod
