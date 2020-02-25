- http://tengine.taobao.org/book/chapter_03.html
- master 进程主要负责接收请求，向 worker 发信号，监控 worker,重启 worker 等等。
- 每个 worker 都是 master fork 出来的，在 Master 里面先建立需要 Listen 的 socket，然后 fork 出 worker，每个 worker 会去竞争连接，但是只有一个能够抢到锁，并 accept 请求。
- nginx 采用异步非阻塞的 IO（epoll/kqueue），好处是并发不会导致 cpu 上下文的切换，只是占用更多内存而已。
- ulimit -n 可以查看一个进程能够打开的 fd 的最大数，也就是 nofile,因为每个 socket 连接会占用一个 fd,这会限制最大连接数。
- nginx 在实现时，是通过一个连接池来管理的，每个 worker 都有一个独立的连接池，连接池大小是 worker_connections

# systemd 管理 nginx

- systemctl enable nginx
- systemctl start/stop/restart nginx
- nginx -s stop
- nginx -s reload
- nginx -t 测试配置是否正确
- nginx -v 显示 nginx 版本
- nginx -V 显示编译阶段配置参数

# 配置

```
user nginx; 用户和用户组
worker_processes 8; worker 数，默认是 cpu 核数
error_log /var/log/nginx/error.log crit; 错误日志路径和错误级别
pid /run/nginx.pid; pid 存放地址
include /path/to/custom/config;
events {
    use epoll; 使用的 IO 模型
    worker_connections 51200; 每个 worker 的最大连接数
}
http {
    server{
        location / {
        }
    }
}

```

# 虚拟主机

## 给网卡加 ip

使用 ip 命令即可，但是因为重启会失效，可以将命令写到/etc/rc.local 文件中，这样在开机时可以自动运行。
一个 server 就是一个虚拟主机

```
http {
    server{
        listen 192.168.8.43:80; 监听的 ip 和端口
        server_name 192.168.8.438.43; 主机名
        access_log logs/server1.access.log combined; 访问日志
        location / {
            index index.html;
            root /data/server1; 文件存放路径
        }
    }
    server {
        listen 192.168.8.44:80;
        server_name 192.168.8.44;
        access_log logs/server2.access.log combined;
        location / {
            index index.html;
            root /data/server2;
        }
    }
}
```

也可以配置基于域名的虚拟主机，只需要配置好 DNS 服务器，将每个主机名映射到正确的 ip 地址。

```

http {
    server {
        listen 80;
        server_name aaa.domain.com;
        ...
    }
    server {
        listen 80;
        server_name bbb.domain.com;
        ...
    }
}

```

## 日志文件配置和切割

设置日志格式

```

log_format combined '$remote_addr - $remote_user [$time_local] '
'"$request" $status $body_bytes_sent '
                '"$http_referer" "$http_user_agent"';
log_format mylogFormat '$http_x_forward_for - $remote_user [$time_local] '

```

```
#!/bin/bash #每天 00:00 运行并生成新的 nginx 日志
logs_path="/data/logs"
mkdir -p ${logs_path}$(date -d "yesterday" + "%Y")/\$(date -d "yesterday" + "%m")/
mv balabala
kill -USR1 `cat \run\nginx.pid`
```

## gzip

```
gzip on
gzip_min_length 1k;
```

## 浏览器本地缓存设置

```
expires 1h;
```

## 负载均衡

第四层和第七层，nginx 是第七层的负载均衡

## nginx Rewrite 规则相关指令

## 使用 tls 加密 tcp 流量

https://www.yanxurui.cc/posts/server/2017-09-13-secure-TCP-Data-using-TLS/
