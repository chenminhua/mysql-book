编排是容器云的灵魂，也是 k8s 社区持久生命力的源泉。

Cloud Foundry 等项目开启了以 pass 为核心的构建平台层服务能力的变革。CF 的核心就是一套应用的打包和分发机制，利用 cgroups 和 namespace 为每个应用单独建立隔离运行环境。这种隔离运行环境的应用托管能力就是 Pass 项目的核心能力，而这个隔离环境就是容器。而 docker 容器的致胜法宝是 Docker 镜像，把程序和运行环境打包起来。

- 2014 年，Kubernetes 诞生。
- 2015 年，Docker 公司将 Libcontainer 捐出，并改名为 RunC 项目，交由一个完全中立的基金会管理。
- 以 RunC 为依据，制定一套容器和镜像的标准和规范，OCI（ Open Container Initiative ），将容器运行时和镜像的实现从 Docker 项目中剥离出来。
- CNCF 基金会：以 K8s 为基础，建立一个由开源基础设施领域厂商主导的、按照独立基金会方式运营的平台级社区。
- CNCF 成员项目： prometheus, fluentd, opentracing, CNI 等。
- k8s 推进民主化架构：从 API 到容器运行时的每一层，k8s 都提供了可扩展的插件机制。

容器社区中大量的、基于 Kubernetes API 和扩展接口的二次创新工作，比如：目前热度极高的微服务治理项目 Istio；被广泛采用的有状态应用部署框架 Operator；还有像 Rook 这样的开源创业项目，它通过 Kubernetes 的可扩展接口，把 Ceph 这样的重量级产品封装成了简单易用的容器存储插件。

**容器实际上是由 namespace + Cgroups + rootfs 构建出来的进程隔离环境。Namespace + Cgroups 是容器运行时，是容器的动态视图。而一组联合挂载在 /var/lib/docker/aufs/mnt 上的 rootfs 是容器的静态视图。**

用户希望 k8s 可以做到： 我有一个容器镜像，请帮我在一个给定的集群上把这个应用运行起来，我还希望能给我提供路由网关、水平扩展、监控、备份、灾难恢复等一系列运维能力。这不就是 PaaS 吗？如果 Kubernetes 项目只停留在拉镜像、运行容器，以及提供运维功能的话，好像也没啥竞争力。

- k8s 的架构与其原型项目 Borg 非常类似，都由 Master 和 Node 两种节点组成。
- Master 由三个组件组成，分别是负责 API 服务的 kube-apiserver、负责调度的 kube-scheduler，以及负责容器编排的 kube-controller-manager。
- 整个集群的持久化数据，则由 kube-apiserver 处理后保存在 Etcd 中。而计算节点上最核心的部分，则是一个叫作 kubelet 的组件。
- kubelet 主要负责和 CRI 打交道，而不关心你使用的具体是什么容器运行时。而具体的容器运行时负责将对 CRI 的请求翻译成系统调用（namespace 和 Cgroup 等）。
- kubelet 还和 Device Plugin 交互来管理 GPU 等物理设备。
- Kubelet 另一个功能，是调用网络插件和存储插件为容器配置网络和持久化。对应接口分别是 CNI 和 CSI。

k8s 要解决的最重要问题是：处理各种任务之间的关系。比如， Web 应用与数据库间的访问关系，负载均衡和后端服务之间的代理关系，门户应用与授权组件之间的调用关系。传统虚拟机环境对这种关系的处理方法都是比较“粗粒度”的。你会经常发现很多功能并不相关的应用被一股脑儿地部署在同一台虚拟机中，只是因为它们之间偶尔会互相发起几个 HTTP 请求。更常见的情况则是，一个应用被部署在虚拟机里之后，你还得手动维护很多跟它协作的守护进程（Daemon），用来处理它的日志搜集、灾难恢复、数据备份等辅助工作。容器技术出现后，那些原先拥挤在同一个虚拟机里的各个应用、组件、守护进程，都可以被分别做成镜像，然后运行在一个个专属的容器中。它们之间互不干涉，拥有各自的资源配额，可以被调度在整个集群里的任何一台机器上。而这，正是一个 PaaS 系统最理想的工作状态，也是所谓“微服务”思想得以落地的先决条件。

**k8s 最主要的设计思想是，从更宏观的角度，以统一的方式来定义任务之间的各种关系，并且为将来支持更多种类的关系留有余地。**

- k8s 中，Pod (原型是 borg 中的 Alloc)里的容器共享同一个 Network Namespace、同一组数据卷，从而达到高效率交换信息的目的。
- 而对于另外一种更为常见的需求，比如 Web 应用与数据库之间的访问关系，k8s 提供了一种叫作 Service 的服务。
- 容器的 IP 地址等信息不是固定的，Web 怎么找到数据库 Pod 呢？k8s 通过给 pod 绑定 service 来实现。
- 这个 Service 服务的主要作用，就是作为 Pod 的代理入口（Portal），从而代替 Pod 对外暴露一个固定的网络地址。
- Service 后端真正代理的 Pod 的 IP 地址、端口等信息的自动更新、维护，则是 k8s 的职责。

路线图

- 从容器这个最基础的概念出发，首先遇到了容器间“紧密协作”关系的难题，于是就扩展到了 Pod；
- 有了 Pod 之后，我们希望能一次启动多个应用的实例，这样就需要 Deployment 这个 Pod 的多实例管理器；
- 而有了这样一组相同的 Pod 后，我们又需要通过一个固定的 IP 地址和端口以负载均衡的方式访问它，于是就有了 Service。
- 可是，如果现在两个不同 Pod 之间不仅有“访问关系”，还要求在发起时加上授权信息。于是有了 secret。
- Secret 其实是一个保存在 Etcd 里的键值对数据。k8s 会在指定 Pod 启动时，自动把 Secret 里的数据以 Volume 的方式挂载到容器里。
- **除了应用与应用之间的关系外，应用运行的形态是影响“如何容器化这个应用”的第二个重要因素。**
- Job, DaemonSet, CronJob 等等。

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

- pod 是 k8s 的原子调度单位。容器本质是进程，但不够描述“进程组”概念。
- pod 可用来描述一个“容器组”，容器组应该可以共享一些信息，比如 namespace, socket 文件等。
- Pod 只是一个逻辑上的概念，k8s 真正在处理的还是 namespace 和 cgroups。
- Pod 里的容器共享 Network Namespace，并可声明共享同一个 volume。
- 在 Pod 中，使用一个中间容器（Infra 容器），infra 容器永远是第一个被创建的，而其他容器则会以 Join Network Namespace 的方式加入。
- Infra 容器的镜像就是 k8s.gcr.io/pause。其启动后永远处于暂停状态。
- 对于同一个 pod 里面的所有用户容器来说，它们的进出流量，可以认为都是通过 infra 容器完成的。
- 当你想在一个容器里面跑多个功能不相关的应用时，应该优先考虑它们是不是更应该被描述成一个 pod 里面多个容器？
- 将来如果你要为 K8s 开发网络插件，应该重点考虑的是如何配置这个 Pod 的 network namespace。
- 有了这个设计之后，共享 Volume 就简单多了：Kubernetes 项目只要把所有 Volume 的定义都设计在 Pod 层级即可。
- 这样，一个 Volume 对应的宿主机目录对于 Pod 来说就只有一个，Pod 里的容器只要声明挂载这个 Volume，就一定可以共享这个 Volume 对应的宿主机目录。比如下面这个例子:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: two-containers
spec:
  restartPolicy: Never
  volumes:
    - name: shared-data
      hostPath:
        path: /data
  containers:
    - name: nginx-container
      image: nginx
      volumeMounts:
        - name: shared-data
          mountPath: /usr/share/nginx/html
    - name: debian-container
      image: debian
      volumeMounts:
        - name: shared-data
          mountPath: /pod-data
      command: ['/bin/sh']
      args: ['-c', 'echo Hello from the debian container > /pod-data/index.html']
```

到底哪些属性属于 Pod 对象，而又有哪些属性属于 Container 呢？ Pod 扮演的是虚拟机的角色，凡是调度、网络、存储以及安全相关的属性，基本都是 Pod 级别的。

```yaml
NodeSelector 是一个将 Pod 与 Node 进行绑定的字段

apiVersion: v1
kind: Pod
...
spec:
nodeSelector:
    disktype: ssd 表示此 Pod 要运行到 “disktype:ssd” 标签的节点。
```

NodeName 一旦被赋值，k8s 就会认为这个 pod 已经调度过了，所以这个字段一般由调度器负责，但是用户可以用它来骗调度器。

HostAliases: 定义了 Pod 的 Hosts 文件里面的内容。在 k8s 中，如果要设置 hosts 文件里的内容，就一定要通过这种方法。

shareProcessNamespace 表示这个 pod 里面的容器是否共享 PID Namespace

## “声明式 API”。

这种 API 对应的“编排对象”和“服务对象”，都是 Kubernetes 项目中的 API 对象（API Object）。这就是 Kubernetes 最核心的设计理念。

## daemonset

DaemonSet 的主要作用是，让你再 k8s 集群中运行一个 Daemon Pod：这个 Pod 运行在 K8s 集群的每一个 node 上。每个节点都只有一个这样的实例。当有新的节点加入 k8s 集群后，该 pod 会被自动创建。

DaemonSet 的用处：

- 各种网络插件的 Agent 组件，都必须运行在每个节点上，用来处理这个节点上的容器网络。
- 各种存储插件的 Agent 组件，也必须运行在每个节点上，用来在这个节点挂载远程存储目录，操作容器的 volume 目录。
- 各种监控组件和日志组件，也必须运行在每个节点上，负责节点的监控信息和日志收集。
- 怎么保证每个 node 上只有一个被管理的 Pod 的呢？DaemonSet controller 从 etcd 中获取 node 列表，然后遍历 Node 并检查其上面有没有运行此 DaemonSet。
- DaemonSet 开始运行的时机，很多时候比整个 k8s 集群都要早。
- 比如管理 fluentd-elasticsearch 的 DaemonSet，就是通过 fluentd 将 Docker 容器里面的日志转到 elasticsearch 中。

DaesomSet 的过人之处则是通过 Toleration 实现的，比如如果一个 DaemonSet 是一个网络插件，则就要面对调度这个 DaemonSet 的 pod 时，节点上可能没有网络的情况，这种情况在 k8s 中被称为污点。而 DaemonSet 中可以声明容忍这个污点。

## StatefulSet

- 分布式系统中，实例间存在关系，比如：主从关系，主备关系。还有一些数据存储类应用，如果被杀了，可能导致数据丢失。
- 这些就是有状态应用。k8s 的 StatefulSet 把状态分成拓扑状态和存储状态。
- 而 StatefulSet 的核心功能，就是通过某种方式记录这些状态，然后在 pod 被重新创建时为 Pod 恢复状态。

K8s 的 service 有两种方式

- 一种是虚拟 IP，比如我们访问某个 service 的 ip（比如 10.0.23.1）的时候，它会把请求转发到某个 Pod 上。
- 另一种是 service 的 DNS 方式。这时访问”my-svc.my-namespace.svc.cluster.local”，就可以通过 dns 访问到 my-svc 的 service 代理的某一个 pod。
- 而 DNS 的方式也分两种，一种还是先解析到 vip 然后转发，另一种是直接转发（也被称为 headless）

所谓的 headless service 其实就是在配置的时候把 clusterIP 字段设置为 none（这也是为啥它叫 headless）。headless 的 pod 的 dns 为 （dns 格式：<pod-name><svc-name><namespace>.svc.cluster.local）。所以其实 headless service 就是一个没有 vip 的 dns 记录，其绑定了它下面的所有 pod。

实际上，在部署“有状态应用”的时候，应用的每个实例拥有唯一并且稳定的“网络标识”，是一个非常重要的假设。

- StatefulSet 使用 Persistent Volume Claim 对存储状态进行管理。在 pod 里面声明 Volume，只要在 pod 里加上 spce.volumes 字段就行。然后，你就可以在这个字段里定义具体类型的 Volume 了，比如: hostPath.
- 但是作为应用开发者，可能不知道有哪些 Volume 类型可用，对持久化项目（比如 Ceph, ClusterFS）不了解。
- 这些关于 Volume 的管理和远程持久化存储只是，不仅超越了开发者知识储备，还暴露了公司基础设施秘密。
- 后来, k8s 中引入了 Persistent Volume Claim (PVC) 和 Persistent Volume (PV)的 API 对象，降低了用户声明和使用持久化 Volume 的门槛。
- 有了 PVC 后，开发人员想使用一个 Volume，只需要两步。
- 第一步，定义 PVC，声明想要的 Volume 属性： 这个 PVC 对象里面，只有描述性的属性和定义。
- 第二步，在应用的 Pod 中，声明使用这个 PVC。我们只需要声明它的类型是 persistentVolumeClaim，然后指定 PVC 的名字，而不用关系 Volume 本身的定义。
- 可是，这个 Volume 从哪里来呢？答案是，来自运维人员维护的 PV 对象。k8s 中的 PVC 和 PV，就类似于“接口”和“实现”。

这次，我们为这个 StatefulSet 额外添加了一个 volumeClaimTemplates 字段。从名字就可以看出来，它跟 Deployment 里 Pod 模板（PodTemplate）的作用类似。也就是说，凡是被这个 StatefulSet 管理的 Pod，都会声明一个对应的 PVC；而这个 PVC 的定义，就来自于 volumeClaimTemplates 这个模板字段。更重要的是，这个 PVC 的名字，会被分配一个与这个 Pod 完全一致的编号。

这个自动创建的 PVC，与 PV 绑定成功后，就会进入 Bound 状态，这就意味着这个 Pod 可以挂载并使用这个 PV 了。PVC 其实就是一种特殊的 Volume。只不过一个 PVC 具体是什么类型的 Volume，要在跟某个 PV 绑定之后才知道。

当然，PVC 与 PV 的绑定得以实现的前提是，运维人员已经在系统里创建好了符合条件的 PV（比如，我们在前面用到的 pv-volume）；或者，你的 Kubernetes 集群运行在公有云上，这样 Kubernetes 就会通过 Dynamic Provisioning 的方式，自动为你创建与 PVC 匹配的 PV。

StatefulSet 的设计思想：StatefulSet 其实就是一种特殊的 Deployment，而其独特之处在于，它的每个 Pod 都被编号了。而且，这个编号会体现在 Pod 的名字和 hostname 等标识信息上，这不仅代表了 Pod 的创建顺序，也是 Pod 的重要网络标识（即：在整个集群里唯一的、可被的访问身份）。

有了这个编号后，StatefulSet 就使用 Kubernetes 里的两个标准功能：Headless Service 和 PV/PVC，实现了对 Pod 的拓扑状态和存储状态的维护。
