# Kafka

## Kafka的体系结构

### 三个基本构成
- Producer: 生产者，发送消息方
- Consumer: 消费者，接收消息方。消费者连接到Kafka上并接收消息，进行响应的业务逻辑处理
- Broker: 服务代理节点。

### Topic和Partition
- kafka中的消息以主题为单位进行归类，生产者负责将消息发送到特定的主题(Topic)中，消费者订阅主题并进行消费
- 主题可以细分成多个分区(Partition)，一个分区只属于单个主题，同一个主题下不同分区包含的信息是不同的。
- 分区可以看作一个可追加的日志文件，消息被追加到分区日志文件的时候会分配一个特定的偏移量(offset)，offset是消息在分区中的唯一标识，可以保证消息在分区内的顺序性，但是不同分区是不一样的

## Kafka分区多副本机制
- 同一个分区的不同副本中保存的是相同的消息（同一时刻，副本之间信息可能不同步），是一主多从关系，leader副本处理读写请求，follower副本只负责与leader副本的消息同步
- leader出现故障时，会从follower重新选举新的leader副本
- 分区中所有的副本统称为AR(Assigned Replicas)，所有与leader副本保持一致的是ISR(In-Sync Replicas)消息会先发送到leader，replicas再从leader拉取消息同步，所以有滞后。与leader同步滞后过多的副本集称为OSR(Out-of-Sync Replicas)
- leader负责维护跟踪ISR的同步状态，滞后过多的，会踢出ISR，同步跟上来的从OSR移到ISR。

## 什么是HW高水位和LEO
- 高水位标识了一个特定的offset，消费者只能消费这个之前的消息
- LEO标识当前日志文件中下一条待写入的消息的offset，分区ISR集合中每个副本都会维护自身的LEO，最小的LEO作为HW
- 同步复制要求所有能工作的leader副本都复制完，一条消息才能被确认为已成功提交。而异步复制，消息写入leader就被认为成功提交，但是如果发生宕机，消息还没同步完，就会造成数据丢失。Kafka通过HW和LEO机制权衡了数据可靠性和性能。

## Kafka参数设置
- zookeeper.connect: 指明broker连接的Zookeeper集群的地址，多个节点使用","隔开，例如"localhost1:2181,localhost2:2181,localhost3:2181"
- listeners: 指明broker监听客户端连接的地址列表，配置格式为"protocol1://hostname1:port1,protocol2://hostname2:port2"，protocol代表协议类型，支持PLAINTEXT、SSL、SASL_SS。如果不指定主机，默认是网卡。
    - advertised.listeners: 主要用于IaaS，包含公网网卡和私网网卡时，advertise.listeners绑定公网IP供外部客户端使用，listeners绑定内网IP供broker间通信
- broker.id: kafka集群broker唯一标识
- log.dir&log.dirs: Kafka把所有消息存到磁盘上，这两个参数用来设置消息日志存储的位置。log.dirs的优先级比log.dir高。
- message.max.bytes: 用来设置broker所能接收消息的最大值，默认值是1000012（B），约等于976.6KB。如果Producer发送的数据大于这个参数，会报RecordToolLargeException异常。

## Kafka消息消费模式
- 如果所有消费者隶属于同一个消费组，所有的消息都会被均衡地投递给每一个消费者，**即每个消费只会被一个消费者处理**
- 如果所有的消费者隶属于不同的消费组，所有的消息都会被广播给所有的消费者，每条消息都会被所有的消费者处理。

## Kafka消费再均衡
- 再均衡是指分区所属权从一个消费者转移到另一个消费者的行为。它为消费组具备高可用行和伸缩性提供保障，使用户可以方便安全地删除消费组内的消费者或者往消费组添加消费者。
- 再均衡期间，消费组内的消费者无法读取消息。
- 再均衡可能会造成重复消费，如果A正在消费，并且还没有提交位移，分区被分配给了B，B又从被消费过地方开始重新消费
- 再均衡前，需要提交已经消费的位移。

## Kafka中ProducerBatch是什么？
- 主线程创建的消息会被缓存到消息累加器RecordAccumulator，Sender线程负责从累加器中获取信息发送给Kafka
- 生产者的消息会被追加到RecordAccumulator中的某个双端队列，队列中的内容是ProducerBatch。
- ProducerBatch包含了一个或多个ProducerRecord，这样可以节省信息的尺寸，减少网络请求的次数提升整体的吞吐量

## (Java Kafka)生产者参数配置
- bootstrap.servers: 用来指定生产者连接Kafka集群的地址，多个地址逗号隔开
- key.serializer/value.serializer: broker接收的消息必须以字节数组形式存在，在发往broker前需要做序列化操作
- client.id: 设置生产者的id
- acks: 指定分区中必须要有多少个副本收到这条消息之后生产者才会认为这条消息是成功写入的。
- max.request.size: 限制生产者客户端发送的消息的最大值
- retries&retry.backoff.ms: retries用来配置生产者重试的次数，默认为0；retry.backoff.ms限制了两次重试的间隔
- compression.type: 消息的压缩方式，对消息压缩可以减少网络传输量，降低网络I/O
- connection.max.idle.ms: 指定多久后关闭闲置的连接
- linger.ms: 指定生产者发送ProducerBatch之前等待更多的消息加入ProducerBatch的时间。生产者会在ProductorBatch被填满或超时后发送。
- receive.buffer.bytes: 设置Socket接收消息缓冲区的大小，默认是32KB。当kafka和producer处于不同机房时建议调大参数
- send.buffer.bytes: 设置Socket发送消息缓冲区大小，默认是128KB。
- request.timeout.ms: 设置Producer等待请求响应的最长时间，默认是30000ms，请求超时后可以进行重试。
- max.in.flight.requests.per.connection: 闲置每个连接最多缓存的请求数

## (Java Kafka)消费者参数配置
- bootstrap.servers: 指定连接kafka集群的broker地址
- group.id: 消费者隶属的消费组id
- key.serializer&value.serializer: 消费者从broker取消息要用的反序列化格式
- fetch.min.bytes: 配置消费者一次拉取请求中能从kafka拉取的最小数据量。如果返回给消费者的数据量小于设置值，会等待直到满足这个参数
- fetch.max.bytes: 用来配置消费者一次拉取请求中从kafka中拉取的最大数据量，如果第一个非空分区中拉取的第一条消息大于该值，消息会返回。想要限制消费者最大能接受的数据量通过message.max.bytes设置
- fetch.max.wait.ms: 指定Kafka的等待时间，默认是500ms
- max.partition.fetch.bytes: 配置从每个分区里返回给消费者的最大数据量
- max.poll.records: 配置消费者在一次拉取请求中拉取的最大消息数
- connections.max.idle.ms: 指定多久之后关闭闲置的连接
- exclude.internal.topics: kafka内部主题__consumer_offsets&__transaction_state是否向消费者公开
- receive.buffer.bytes: 设置Socket接收消息缓冲区大小，消费者和kafka不同机房情况下适当调大
- send.buffer.bytes: 设置Socket发送消息缓冲区大小，默认128KB
- request.timeout.ms: 配置消费者请求响应的最长时间
- metadata.max.age.ms: 配置元数据的过期时间，如果元素在参数限定时间范围内没有进行更新，会被强制更新
- reconnect.backoff.ms: 配置尝试重新连接指定主机之前的等待时间
- retry.backoff.ms: 配置尝试重新发送失败的请求到指定主题分区之前的等待时间
- isolation.level: 配置消费者事务隔离级别
- max.poll.interval.ms: 通过消费组管理消费者时，该配置指定拉取消息线程最长的空闲时间
- auto.offset.reset: 每当消费者查找不到所记录的消费位移时，根据参数选择是从最新还是最旧一条消息开始读
- enable.auto.commit: 是否要自动提交位移
- auto.commit.interval.ms: 配置自动提交消费位移的时间间隔