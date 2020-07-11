# Zookeeper

## Zookeeper是什么？
- Zookeeper是一种"分布式协调服务"，可以在分布式系统中共享配置，协调锁资源，提供命名服务。
- Zookeeper的数据模型类似树。数据存储基于节点，节点叫做Znode
![Zookeeper数据结构](https://user-gold-cdn.xitu.io/2018/5/22/16385a1ec0628043?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
- Znode包含了数据、子节点引用、访问权限
![Znode结构](https://user-gold-cdn.xitu.io/2018/5/22/16385a1ecf740084?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
    - data: 存储了数据
    - ACL: 记录Znode的访问权限，哪些用户或IP能访问节点
    - stat: 元数据，如事务ID、版本号、时间戳、大小
    - child: 当前节点的子节点引用
    
## Zookeeper的Watch机制
1. 客户端调用getData方法，服务端收到请求，返回节点数据，并在对应的hash表里插入被watch的Znode
路径，以及watcher列表
2. 当被watch的znode被删除时，服务端会查找哈希表，找到znode对应的所有watcher，异步通知客户端，
并且删除哈希表中对应的key-value

## Zookeeper如何故障恢复
![zookeeper集群结构](https://user-gold-cdn.xitu.io/2018/5/22/16385a1ee4301aa0?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
- Zookeeper Service集群是一主多从结构，更新数据时首先更新到主节点，再同步到从节点
- 读取数据时，直接读取任意从节点
- 为保证主从节点一致性，采用了ZAB协议
    - 定义了三种节点状态:
        - Looking: 选举状态
        - Following: Follower节点从节点状态
        - Leading: Leader节点主节点状态
    - 最大ZXID:
        - 最大ZXID是节点本地的最新事务编号，包含epoch和计数两部分
    - 主节点挂掉，崩溃恢复过程
        - 选举阶段，所有节点处于Looking状态，各自向其他节点发起投票，投票包含自己的服务器ID
        和最新事务ID（ZXID）。然后节点用自身的ZXID和其他节点接收到ZXID比较，如果对方ZXID比
        自己大，就重新发起投票，投给已知的最大ZXID的节点。每次投票服务器都会统计投票数量，
        判断某个节点是否得到半数以上投票，存在的话，节点升级为准Leader，状态变为Leading，
        其他节点变为Following。
        - 发现阶段，Leader接收所有Follower发来的最新的epoch值，从中选出最大epoch，基于这个
        epoch加1，分发给Follower。Follower收到新的epoch后，返回ACK给leader，带上各自最大
        ZXID和历史事务日志，Leader选出最大ZXID，并更新自身历史日志
        - 同步阶段，Leader把收集得到的最新历史事务日志同步给集群中所有的Follower，只有当
        半数以上Follower同步成功，准leader才会成为正式的Leader
        
## Zookeeper如何保证写入一致性
1. 客户端发出写入数据的请求给任意的Follower
2. Follower把写入请求发给Leader
3. Leader采用二阶段提交方式，先发送Propose广播给Follower
4. Follower接收到Propose消息，写入日志成功后，返回ACK消息给Leader
5. Leader接收到半数以上ACK消息，返回成功给客户端，并且广播Commit请求给Follower

## Zookeeper应用场景
- 分布式锁，利用Zookeeper的临时顺序节点
- 利用Znode和Watcher实现分布式服务的注册和发现
- 共享配置和状态信息，Codis利用了Zookeeper存放数据路由表和codis-proxy节点的元信息，同时
codis-config发起的命令会通过Zookeeper同步到各个存活的codis-proxy
