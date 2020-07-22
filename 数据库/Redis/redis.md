# Redis

## 缓存雪崩
- 大量的缓存在极短时间内同时失效，导致大量的查询请求都直接去查询持久化的数据库比如Mysql，导致数据库处理不过来造成性能问题。
- 在批量设置redis缓存的时候，对不同的key，设置一个随机的上下波动的过期时间，避免同时失效
- 对缓存的写，使用锁或者队列方式保证key的顺序增加

## 缓存穿透
- 用户对缓存和数据库中都没有的数据进行大量查询，每次都能绕过缓存直接把请求压力加到了数据库上
- 解决缓存击穿的方法：对查询的条件进行校验，用户鉴权
- 也可以使用布隆过滤器，存储数据库中有的key，然后对请求的key进行校验判断是不是在数据库中存在
- 对查询结果为空的情况，把空结果也进行缓存，但是设置一个较短的过期时间

## 缓存击穿
- 存在一个热点缓存key，大量的请求不断查询这个key
- 当这个key的缓存失效时，大量的请求会到数据库
- 使用互斥锁（setnx SET if not exists)，在请求过来时，加锁，然后从db加载数据存到redis
```python
import redis

cache = redis.StrictRedis()
def get(key):
    value = cache.get(key)
    if not value:
        if cache.setnx(key_mutex, value):
            cache.expire(key_mutex, 3000)
            value = db.get(key)
            cache.set(key, value)
            cache.delete(key_mutex)
        else:
            time.sleep(0.1)
            get(key)
```
- 设置"永不过期"的key，即不对key增加expire time，而是在value里增加过期时间，获取缓存的时候人工判断是否过期
