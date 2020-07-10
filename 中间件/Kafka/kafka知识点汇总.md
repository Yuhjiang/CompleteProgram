# Kafka

## Kafka的体系结构

### 三个基本构成
- Producer: 生产者，发送消息方
- Consumer: 消费者，接收消息方。消费者连接到Kafka上并接收消息，进行响应的业务逻辑处理
- Broker: 服务代理节点。

### Topic和Partition
- kafka中的消息以主题为单位进行归类，生产者负责将消息发送到特定的主题(Topic)中，消费者订阅
主题并进行消费
- 主题可以细分成多个分区(Partition)，一个分区只属于单个主题，同一个主题下不同分区包含的信息
是不同的。
- 分区可以看作一个可追加的日志文件，消息被追加到分区日志文件的时候会分配一个特定的偏移量(offset)，
offset是消息在分区中的唯一标识，可以保证消息在分区内的顺序性，但是不同分区是不一样的

## Kafka分区多副本机制
- 同一个分区的不同副本中保存的是相同的消息（同一时刻，副本之间信息可能不同步），是一主多从
关系，leader副本处理读写请求，follower副本只负责与leader副本的消息同步
- leader出现故障时，会从follower从重新选举新的leader副本
- 分区中所有的副本统称为AR(Assigned Replicas)，所有与leader副本保持一致的是ISR(In-Sync Replicas)
消息会先发送到leader，replicas再从leader拉取消息同步，所以有滞后。与leader同步滞后过多
的副本集称为OSR(Out-of-Sync Replicas)
- leader负责维护跟踪ISR的同步状态，滞后过多的，会踢出ISR，同步跟上来的从OSR移到ISR。

## 什么是HW高水位和LEO
- 高水位标识了一个特定的offset，消费者只能消费这个之前的消息
- LEO标识当前日志文件中下一条待写入的消息的offset，分区ISR集合中每个副本都会维护自身的LEO，
最小的LEO作为HW
- 同步复制要求所有能工作的leader副本都复制完，一条消息才能被确认为已成功提交。而异步复制，
消息写入leader就被认为成功提交，但是如果发生宕机，消息还没同步完，就会造成数据丢失。Kafka通过
HW和LEO机制权衡了数据可靠性和性能。

## Kafka参数设置
- zookeeper.connect: 指明broker连接的Zookeeper集群的地址，多个节点使用","隔开，例如"
localhost1:2181,localhost2:2181,localhost3:2181"
- listeners: 指明broker监听客户端连接的地址列表，配置格式为"protocol1://hostname1:port1,
protocol2://hostname2:port2"，protocol代表协议类型，支持PLAINTEXT、SSL、SASL_SS。如果
不指定主机，默认是网卡。
    - advertised.listeners: 主要用于IaaS，包含公网网卡和私网网卡时，advertise.listeners绑定
    公网IP供外部客户端使用，listeners绑定内网IP供broker间通信
- broker.id: kafka集群broker唯一标识
- log.dir&log.dirs: Kafka把所有消息存到磁盘上，这两个参数用来设置消息日志存储的位置。log.dirs的
优先级比log.dir高。
- message.max.bytes: 用来设置broker所能接收消息的最大值，默认值是1000012（B），约等于976.6KB。
如果Producer发送的数据大于这个参数，会报RecordToolLargeException异常。

## Kafka消息消费模式
- 如果所有消费者隶属于同一个消费组，所有的消息都会被均衡地投递给每一个消费者，**即每个消费
只会被一个消费者处理**
- 如果所有的消费者隶属于不同的消费组，所有的消息都会被广播给所有的消费者，每条消息都会被所有
得分消费者处理。