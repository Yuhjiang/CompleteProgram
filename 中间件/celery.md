# Celery

## 相关资料
1. [知乎 Celery使用](https://zhuanlan.zhihu.com/p/22304455)

## bind
- 在tasks上加`bind=True`即可以在tasks的第一个参数使用`self`，通过self获取task本身的一些属性
- 主要有两个作用，比如手动调用任务重新执行和查看更新任务的状态
```python
@celery.task(bind=True, max_retries=5)
def retrying(self):
    try:
        return 1/0
    except Exception:
        self.retry(countdown=5)
```

```python
@celery.task(bind=True)
def show_progress(self, n):
    for i in range(n):
        self.update_state(state='PROGRESS', meta={'current': i, 'total': n})
```



