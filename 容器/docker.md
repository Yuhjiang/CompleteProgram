# Docker

## Docker的网络模式
`--network` 指定网络模式
- bridge：默认的网络驱动模式，
    - 默认使用docker0网桥，容器之间的ip是互通的，但是无法使用容器名作为通信的host
    - 使用自定义网桥，需要用`docker network create`创建，指定了自定义的network的容器能使用容器名称互相通信
- host：移除容器和Docker宿主机之间的网络隔离，并直接使用主机的网络
- overlay：将多个Docker守护进程连接在一起，使集群服务能够互相通信。需要在Swarm mode下
- macvlan：允许为容器分配mac地址，使其显示为网络上的物理设备。
- none：对于此容器，禁用所有联网

## 查看容器的系统资源使用量
- docker stats
```
CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
63247eef555d        gifted_banach       0.22%               194.7MiB / 1.946GiB   9.77%               964MB / 1.48GB      0B / 0B             47
257b468f9902        jovial_payne        0.10%               2.461MiB / 1.946GiB   0.12%               5.24GB / 4.91GB     0B / 0B             4
a7c87e8ed3ba        mysql               0.03%               211.3MiB / 1.946GiB   10.60%              12.2MB / 31.8MB     0B / 0B             35
```

