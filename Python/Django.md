# Django

## Supervisor配置文件解析
- `unix_http_server`: UNIX socket配置，是supervisor用来管理进程的接口
- `inet_http_server`: supervisor Web服务器的配置，不需要Web服务器可以不开启
- `supervisord`: supervisord 的基础配置，包括日志和pid的位置
- `rpcinterface:supervisor`: 用来配置RPC接口，supervisorctl通过这个RPC来连接socket
- `supervisorctl`: supervisorctl命令配置，它配置的socket地址以及用户名密码应该和`unix_http_server`一致
- `program:<程序名>`: 配置需要运行的程序启动命令，以及相关配置，如日志、环境变量、需要启动的进程数等

## Django、Flask&Tornado框架对比
- Django：最全能的web开发框架，功能完备，可维护性高，开发速度快。但是使用笨重，性能一般
- Tornado：天生异步，性能高。但是框架提供的功能比较少。
- Flask：自由、灵活、扩展性高，有很多第三方插件。

## Django的生命周期
- wsgi封装请求数据然后交给框架
- 中间件，对请求进行校验，添加额外的数据
- 路由匹配
- 视图函数
- 中间件，对响应数据处理
- wsgi封装响应返回给客户端

## Django的内置组件
- 认证组件、缓存、日志、邮件、分页、静态文件管理、消息框架、数据验证

## 列举Django中间件的方法，以及中间件的应用场景
- Django的中间件是一个类，在请求的到来和结束后，django会根据自己的规则在合适的时机执行中间件中相应的方法
- 中间件在settings中的`MIDDLEWARE_CLASSES`变量配置
- 中间件的方法
    - `process_request(self, request)`方法在请求到来时候调用
    - `process_view(self, request, callback, callback_args, callback_kwargs)`在本次将要执行的View函数被调用前调用本方法
    - `process_template_respose(self, request, resposne)`使用render()之后执行
    - `process_exception(self, request, exception)`视图函数在抛出异常时调用，得到的Exception参数是被抛出的异常实例。
    - `process_response(self, request, response)`执行完视图函数后准备将数据返回给客户端前被执行
- 可以修改request和response对象的内容，在视图执行前做一些操作，判断浏览器来源，做一个拦截器
- 可以判断浏览器的来源是PC还是手机
- 可以做一个拦截器，一定时间内某个ip对网页第访问次数过多，可以加入黑名单拒绝服务
- ![中间件执行顺序](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9tbWJpei5xcGljLmNuL21tYml6X3BuZy9idWFGTEZLaWNSb0M5R3pCZWliQXExVVBKMFpsM3Zsd0RpYXM2dEhhN2x5aWFKaWFmWldPbmZsMWZPUVBNT2J2SndUWEF6a1h0UjJnalBZb0JmaEdJRkRYMWJnLzY0MA?x-oss-process=image/format,png)

### 常用中间件举例
- SecurityMiddleware: XXS攻击防御，HTTPS连接相关的设置
- SessionMiddleware: session会话支持
- CommonMiddleware: 支持对URL的重写
    - APPEND_SLASH: 设置为True时，如果url没有以斜杆结尾并且找不到url配置，会形成一个斜线
    结尾的新url
    - PREPEND_WWW: 设置为True时，缺少www.的URL会被重定向到相同的但是以www.开头的URL
- AuthenticationMiddleware: 在视图函数执行前，向每个接收到的user对象添加到HttpRequest对象，
表示当前登录的用户（会存入request.user)
- MessageMiddleware: 开启基于cookie和会话的消息支持
- XFrameOptionsMiddleware: 跨站请求伪造攻击中的点击攻击，通过识别 X-Frame-Options请求头
的信息，比对是否是同源请求。
- UpdateCacheMiddleware/FetchFromCacheMiddleware: 全站缓存

### 自定义中间件
1. 基于函数的
```python
def simple_middleware(get_response):
    # One-time configuration and initialization.
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
    return middleware
```
2. 基于类的(Django3.0开始，逐渐弃用process_request, process_response)
```python
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
```

## 什么事FBV和CBV
- FBV是`function base views`基于函数视图，CBV是`class base views`基于类的视图
- FBV模式，URL匹配成功后，会直接执行对应的视图函数
- CBV模式，服务端通过路由映射表匹配成功后，自动去找dispatch方法，然后通过dispatch反射的方式找到类中对应的方法执行。所有的类视图，都继承了View类，View类里有dispatch，负责分发。
```python
def dispatch(self, request, *args, **kwargs):
    # Try to dispatch to the right method; if a method doesn't exist,
    # defer to the error handler. Also defer to the error handler if the
    # request method isn't on the approved list.
    if request.method.lower() in self.http_method_names:
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    else:
        handler = self.http_method_not_allowed
    return handler(request, *args, **kwargs)
```
- 常用的CBV类
    - ListView：展示对象的列表
    - DetailView：展示某个具体的对象或者一组对象
    
## Django的request的方法是什么时候创建的？
- 请求一个页面的时候，Django创建了一个HttpRequest对象，包含了request数据。Django会加载对应的视图，然后把request作为第一个参数传递到视图函数。
- HttpRequest对象的内容
    - scheme：请求的协议，通常是http or https
    - body: 原始的请求body数据，为字节字符串类型，可以用于自定义的转换方式比如图片，xml格式
    - POST: 格式化后的body数据，但是不包含文件
    - path: 完整的请求地址，但是不包括域名和协议
    - path_info: 去掉path的前缀，比如WSGIScriptAlias被设置成'/minfo/'，path会返回
    '/minfo/music/bands'，而path_info返回'/music/bands'
    - method: 请求的方法
    - encoding: 请求数据的编码
    - content_type: 请求头里的content_type内容，用于定义浏览器读取数据的形式和编码，例如
    'text/html, application/json, application/pdf'
    - GET: 字典化的get请求参数
    - COOKIES： 字典化的cookies，key和value都是字符串
    - FILES: 字典化存储的上传的文件。请求时必须是POST，并且`enctype="multipart/form-data"`
    - META: 请求头的内容
    - headers: 请求头的内容
    - resolver_match: 一个ResolverMatch实例
    - session: 中间件SessionMiddleware添加的，可读可写的类字典对象
    - site: 中间件CurrentSiteMiddleware，Site或RequestSite的实例，由get_current_site返回
    - user: AuthenticationMiddleware，一个AUTH_USER_MODEL指定的类的实例，代表了登录的用户
- Request对象在WSGIHandler里创建，将environ参数封装成request
```python
class WSGIHandler(base.BaseHandler):
    def __call__(self, environ, start_response):
        set_script_prefix(get_script_name(environ))
        signals.request_started.send(sender=self.__class__, environ=environ)
        request = self.request_class(environ)
        response = self.get_response(request)
        ...
```
    
## 给CBV的类方法增加装饰器
1. 在指定的方法上添加装饰器
2. 在类上添加，使用name指定方法
```python
from django.views.generic import View
from django.utils.decorators import method_decorator
def wrapper(func):
    def wrappered_function(*args, **kwargs):
        return func(*args, **kwargs)
    return wrappered_function

class Foo(View):
    @method_decorator(wrapper)
    def get(self, request):
        pass

    def post(self, request):
        pass

@method_decorator(wrapper, name='dispatch')
class Foo2(View):
    def get(self, request):
        pass
    def post(self, request):
        pass
```

## QuerySet方法
- filter(**kwargs): 过滤，简单的条件，如果要是使用复杂的条件，需要用到Q对象
- exclude(**kwargs): 选出不符合条件的数据
```sql
SELECT ... WHERE NOT (XXX)
```
- annotate(*args, **kwargs): 给每个查询出来的对象增加额外的字段，可以使用aggregation的
方法，计算新的字段的数据。比如统计每个blog的评论数量，增加到blog里
```python
from django.db.models import Count
q = Blog.obects.annoate(comments=Count('entry'))
q[0].name   # 'Hey'
q[0].comments  # 12
```
- order_by(*fields): 对结果进行排序
```python
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
# 随机排序
Entry.objects.order_by('?')
```
- reverse(): 结果倒序排序
- distinct(*fields): 去重查询
- values(*fields, **expressions): 指明返回结果的字段
```python
Blog.objects.values('id', 'name')
# <QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
from django.db.models.functions import Lower
Blog.objects.values(lower_name=Lower('name'))
# <QuerySet [{'name__lower': 'beatles blog'}]>
from django.db.models import Count
Blog.objects.values('entry_authors', entries=Count('entry'))
# <QuerySet [{'entry__authors': 1, 'entries': 20}, {'entry__authors': 1, 'entries': 13}]>
Blog.objects.values('entry_auhtors').annotate(entries=Count('entry'))
# <QuerySet [{'entry__authors': 1, 'entries': 33}]>
```
- values_list(*field, flat=False, named=False): 返回结果的tuples，筛选结果的字段
```python
Entry.objects.values_list('id', 'headline')
# <QuerySet [(1, 'First entry'), ...]>
Entry.objects.values_list('id', flat=True).order_by('id')
# <QuerySet [1, 2, 3, ...]>
# named=True，返回namedtuple
Entry.objects.values_list('id', 'headline', named=True)
# <QuerySet [Row(id=1, headline='First entry'), ...]>
```
- dates(field, kind, order='ASC')/datetimes(field, kind, order='ASC'): 
返回datetime.date/datetime.datetime格式的list
- none(): 返回空的queryset
```python
from django.db.models.query import EmptyQuerySet
isinstance(Entry.objects.none(), EmptyQuerySet)
```
- union(*other_qs, all=False): 将多个queryset查询结果合并
```python
qs1 = Author.objects.values_list('name')
qs2 = Entry.objects.values_list('headline')
qs1.union(qs2).order_by('name')
``` 
- intersection(*other_qs): 查找多个queryset相同的数据
- difference(*other_qs): 查找多个queryset的，在queryset里，但不在queryset里
```python
qs1.difference(qs2, qs3)
```
- select_related(*fields): 解决一对多问题，可以将有外键关联的，同时查出来，可以关联好几个字段
```python
from django.db import models

class City(models.Model):
    # ...
    pass

class Person(models.Model):
    # ...
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

class Book(models.Model):
    # ...
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
b = Book.objects.select_related('author__hometown').get(id=4)
```
- prefetch_related(*fields): 解决多对多问题，这个用法比较复杂，参考官方文档：
[prefetch-related](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#prefetch-related)
- extra(select=None, where=None, params=None, tales=None, order_by=None, select_params=None):用户执行复杂的sql语句
```python
qs.extra(
    select={'val': 'select col from sometable where othercol = %s'},
    select_params=(somparam, )
)
from django.db.models.expressions import RawSQL
qs.annoate(val=RawSQL('select col from sometable where othercol = %s', (someparam, )))
```
select用户增加额外的select字段
```python
Entry.objects.extra(select={'is_recent': 'pub_date > "2006-01-01"'})
# SELECT blog_entry.*, (pub_date > '2006-01-01') as is_recent FROM blog_entry;
```
where/tables: 定义where条件
```python
Entry.objects.extra(where=["foo = 'a' OR bar = 'a'", "baz = 'a'"])
# SELECT blog_entry.* FROM blog_entry WHERE (foo = 'a' OR bar ='a') AND (baz = 'a')
```
order_by
```python
q = Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"})
q = q.extra(order_by = ['-is_recent'])
```
params:
```
Entry.objects.extra(where=['headline=%s'], params=['Lennon'])
```
- defer(*fields): 不需要的字段延迟加载处理
- only（*fields): 只获取某些字段的值，不延迟加载，其他的值会延迟加载
- using(alias): 指定使用的数据库

## Django中三种原生sql语句的方法
1. 使用extra
```python
Book.objects.filter(publisher__name='XXX').extra(where=['price>50'])
```
2. Raw，查询语句必须包含主键
```python
books = Book.objects.raw('select * from blog_category')
```
3. 自定义sql
```python
from django.db import connection

cursor = connection.cursor()
cursor.execute("insert into hello_author(name) VALUES ('郭敬明')")  
cursor.execute("update hello_author set name='韩寒' WHERE name='郭敬明'")  
cursor.execute("delete from hello_author where name='韩寒'")  
cursor.execute("select * from hello_author")  
cursor.fetchone()  
cursor.fetchall() 
```

## F和Q的作用
- F: 操作表中的某一列值，允许Django不用获取对象放到内存中再对字段进行操作，而是直接执行原生sql语句操作。
```python
from django.db.models import F
Book.objects.update(price=F('price')+20)
```
- Q: 进行复杂的查询，支持&, |, ~操作符
```python
from django.db.models import Q
Book.objects.filter(Q(title__icontains=keyword) | Q(ip=keyword))
```

## Django ORM批量操作符
- bulk_create(): 需要注意，save()方法不会被调用，pre_save和post_save信号不会被发送。自增字段也不会自增，无法创建多对多关系。
```python
Entry.objects.bulk_create([
    Entry(headline='This is a test'),
    Entry(headline='This is only a test'),
])
```
- bulk_update(): 无法更新主键，save()方法不会被调用，pre_save和post_save信号不会发送，如果更新的内容有重复，只有第一个会执行。
```python
objs = [
    Entry.objects.create(headline='Entry 1'),
    Entry.objects.create(headline='Entry 2'),
]
objs[0].headline = 'This is entry 1'
objs[1].headline = 'This is entry 2'
Entry.objects.bulk_update(objs, ['headline'])
```

## FORM和ModelForm的作用
- Form是自己定义的表单结构，需要继承Django的forms.Form类，然后像Model类一样，定义字段。保存数据的时候，需要从POST里手动取出表单数据
```python
from django import forms
class Loginform(forms.Form):
    user = forms.CharField(max_length=12, min_length=3,
                           error_messages={
                               "required": "不能为空",  # 设置提示错误信息
                               "max_length": "最大长度不能超过6",
                               "min_length": "最小长度不能小于3",
                           }
                           )

    phone = forms.CharField(
        error_messages={
            "required": "不能为空",
        }
    )

    email = forms.EmailField(error_messages={
        "required": "不能为空",
        "invalid": "格式错误"}
    )
```
- ModelForm是可以使用定义好的Model类，需要继承forms.ModelForm，然后在Meta类里，包含表单要现实的字段，提示信息，错误信息等内容。保存数据时，不用手工去取数据，直接save即可
```python
from django.forms import ModelForm
class BookModelForm(ModelForm):
    class Meta:
        model=Book    　　　　　#对应model中的类
        fields="__all__" 　　  #字段“__all__”显示所有字段，["title","price"..]显示部分字段
        labels={         　　  #自定义在前端显示的名字
            "title":"书名",
            "price":"价格",
            "publish":"出版社",
            "author":"作者"
        }

def add(request):
    if request.method=="GET":
        model_form_obj=BookModelForm()
        return render(request,'add.html',locals())
    else:
        model_form_obj=BookModelForm(request.POST)
        # 校验数据
        if model_form_obj.is_valid():
            # 提交数据
            model_form_obj.save()
            return redirect("/index/")
        else:
            return render(request,"add.html",locals())
```
## Form中有choices字段，如何实现实时更新
1. 重写Form的初始化方法
```python
from django.forms import Form
from django.forms import fields

class UserForm(Form):
    name = fields.CharField(label='username', max_length=32)
    email = fields.EmailField(label='Email')
    ut_id = fields.ChoiceField(choies=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ut_id'].choices = models.UserType.objects.all().vlaues_list('id', 'title')

def user(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'user.html', {'form': form})
```
2. 使用ModelChoiceField字段
```python
from django.forms import Form, fields, models

class UserForm(Form):
    name = fields.CharField(label='Username', max_length=32)
    email = fields.EmailField(label='Email')
    ut_id = models.ModelChoiceField(queryset=models.UserType.objects.all())
```

## ForeignKey中，on_delete参数的作用
当一个ForeignKey被删除后，Django会通过指定的on_delete参数模仿sql的约束作用
- `CASCADE`: 级联删除
- `PROJECT`: 抛出ProjectedError，以阻止对象被删除
- `SET_NULL`: 设置ForeignKey为null，外键要允许为null
- `SET_DEFAULT`: 设置成默认值，必须要设置外键的默认值
- `SET`: 设置一个传入SET的值，或者一个可调用对象（会执行对象，返回结果）
```python
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class MyModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),   
    )
```

## Django中csrf_token机制
- Django使用中间件`django.middleware.csrf.CsrfViewMiddleware`来完成跨站请求伪攻击的防御
- 有两个装饰器`@csrf_protect`单独为某个视图设置csrf_token校验， `@csrf_exempt`单独为某个视图取消csrf_token校验
- 使用Django的template时，页面的表单里会有hidden的csrf_token，这个值是服务器端生成，每次都不一样的随机值，用户提交表单的时候，中间件会校验表单数据里的csrf_token和保存的是否一致。
- 在返回有表单的页面的时，cookie里会更新一个csrftoken字段，页面的表单里也有一个相同的csrftoken，处理请求的时候，中间件会验证两个csrftoken是否一致。一致。(保存分两种，settings里设置了CSRF_USE_SESSIONS，就会从session里获取，否则就从
cookies里获取)

## Django信号

### 常用信号：
- django.db.models.signals.pre_save & django.db.models.signals.post_save: ORM模型save()方法调用前后发送信号
- django.db.models.signals.pre_delete & django.db.models.signals.post_delete: delete()方法调用前后发送信号
- django.db.models.signals.m2m_changed: 多对多字段被修改时发送信号
- django.core.signals.request_started & django.core.signals.request_finished接收和关闭HTTP请求时发送信号

### 监听信号
- `Signal.connect(receiver, sender=None, weak=True, dispath_uid=None)[source]`
    - receiver: 当前信号的回调函数
    - sender: 指定从哪个发送方接收信号
    - weak: 是否弱引用
    - dispatch_uid: 信号接收器的唯一标识，避免信号多次发送
```python
def my_callback(sender, **kwargs):
    print('Request finished!')

from django.core.signals import request_finished

# 1. 手动方式连接
request_finished.connect(my_callback)
# 2. receiver装饰器
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print('Request finished!')

# 3. 接收特定发送者的信号
from django.db.models.signals import pre_save
from django.dispatch import receiver
from myapp.models import MyModel

@receiver(pre_save, sender=MyModel)
def my_handler(sender, **kwargs):
    pass

# 4. 防止重复信号
from django.core.signals import request_finished
request_finished.connect(my_callback, dispatch_uid='my_unique_identifier')
```
### 自定义信号
类原型 Signal(providing_args=list)[source], providing_args参数是一个列表，由信号提供给监听者的参数的名称组成
```python
import django.dispatch

# 向接收者提供size和topping参数
pizza_done = django.dispatch.Signal(providing_args=['toppings', 'size'])
```

### 发送信号
sender必须提供（大多数情况下是个类名），可以提供任意数量的其他关键字参数
```python
from django.core.signals import Signal
Signal.send(sender, **kwargs)[source]

Signal.send_robust(sender, **kwargs)[source]

# Example
class PizzaStore(object):
    def send_pizza(self, toppings, size):
        pizza_done.send(sender=self.__class__, toppings=toppings, size=size)
```

### 断开信号
```python
Signal.disconnect(receiver=None, sender=None, dispatch_uid=None)[source]
```

### 其他信号
[https://docs.djangoproject.com/en/3.0/ref/signals/](https://docs.djangoproject.com/en/3.0/ref/signals/)
#### pre_init
初始化一个模型前，会被触发
- sender: 创建实例的类
- args: 位置参数
- kwargs: 关键词参数
```python
q = Question(question_text="What's new?", pub_date=timezone.now())
# sender	Question (the class itself)
# args	[] (an empty list because there were no positional arguments passed to __init__())
# kwargs	{'question_text': "What's new?", 'pub_date': datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)}
```

#### post_init
初始化完成后触发
- sender: 创建实例的类
- instance: 创建好的实例

## Django使用现有的数据库生成models
- 使用inspectdb生成models.py
```shell script
python manage.py inspectdb > blogapp/models.py
```
- 后续想让修改model的字段，并可以使用django的数据库迁移功能，在Meta中设置managed=True
- 首次数据迁移migrate时，因为数据库已经存在，需要使用--fake-initial参数
```shell script
python manage.py makemigrations
python manage.py migrate --fake-initial
```

## Django migrate --fake-initial和 --fake的区别
- fake-initial 可以跳过app的初始化，如果app里的模型对应的表已经创建好，初始化项目的时候使用--fake-initial。这个命令会跳过创建表的过程，但是对已存在表的修改会被执行。
- fake 告诉Django标记某次迁移已经被应用到数据库中，不会运行sql语句去改动表。当有人工修改表结构时，可以用fake跳过这次修改

## ORM和原生SQL的优缺点
### 1. ORM
优点：
使用ORM最大的优点是快速开发，集中在业务上而不是数据库上
- 隐藏了数据访问的细节，通用数据库交互简单易行，避免了不规范，冗余，风格不一致的SQL语句，避免sql语句上的bug
- 将数据库表和对象模型关联，只需针对相关的对象模型进行编码，无法考虑对象模型和数据表之间的转化
- 方便数据库的迁移，不需要修改对象模型，只需要修改数据库的配置
缺点：
- 性能上存在问题，自动进行数据库关系的映射需要消耗系统资源
- 在处理多表联查、where条件复杂的查询时，ORM可能会生成效率低下的SQL
- SQL语句是ORM框架自动生成的，SQL调优不方便
- 因为返回的Object会很多成员变量和方法，会消耗更多内存

### 2. 原生SQL
优点
- 进行复杂查询时更加灵活
- 可以根据需要编写特殊的sql语句
缺点
- 需要对输入进行严格的检测
- 可能会有sql注入漏洞
- 不能使用orm方便的特性

## Django contenttype作用
[Django contenttypes 应用](https://blog.csdn.net/Ayhan_huang/article/details/78626957)
contenttypes是Django内置的一个应用，追踪项目中所有的app和model的对应关系，并记录在ContentType表中。
```sql
+----+-----------------------+--------------------+
| id | app_label             | model              |
+----+-----------------------+--------------------+
|  3 | admin                 | logentry           |
| 24 | album                 | album              |
| 25 | album                 | picture            |
|  5 | auth                  | group              |
|  4 | auth                  | permission         |
| 15 | blog                  | category           |
| 21 | blog                  | comment            |
```
比如一个model中，有一个ForeignKey需要关联多个表的，正常情况下，一个ForeignKey只能和一张表做关联，使用contenttypes中提供的特殊字段GenericForeignKey，可以解决上述的问题
- 在model中定义ForeignKey字段，关联到ContentType表，通常这个字段命名为'content_type'
- 在model中定义PositiveIntegerField字段，用来存储关联表中的主键，通常命名为'object_id'
- 在model中定义GenericForeignKey字段，传入上述两个字段的名字
```python
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class Electrics(models.Model):
    name = models.CharField(max_length=32)
    coupons = GenericRelation(to='Coupon')  # 用于反向查询，不会生成新的字段

class Foods(models.Model):
    name = models.CharField(max_length=32)
    coupons = GenericRelation(to='Coupon')

class Coupon(models.Model):
    name = models.CharField(max_length=32)
    
    content_type = models.ForeignKey(to=ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

## Django rest framework框架中有哪些组件
- 序列化组建serializer，对queryset序列化和对请求数据格式校验
- routers进行路由分发
```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
```
- 认证组建，写一个类注册到认证类，在authticate里编写逻辑
- 权限组件，写一个类注册到权限类，在has_permission里编写验证逻辑
```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
```
- 频率限制，写一个类注册到频率类，在allow_request/wait中编写认证逻辑
- 解析器，选择对数据解析的类
- 渲染器
- 分页
- 版本控制
- 缓存
```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


class UserViewSet(viewsets.ViewSet):

    # Cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
        content = {
            'user_feed': request.user.get_user_feed()
        }
        return Response(content)


class PostView(APIView):

    # Cache page for the requested url
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        content = {
            'title': 'Post title',
            'body': 'Post content'
        }
        return Response(content)
```

## django rest framework框架中的视图都可以继承哪些类
- View(object)
- APIView(View) 重新封装了request
- GenericView(views.APIView)封装了get_queryset,get_serializer
- GenericViewSet(ViewSetMixin, generics.GenericAPIView)重新了as_view
- ModelViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet))

## django rest framework框架的认证流程
- 用户请求走进来后,走APIView,初始化了默认的认证方法
- 走到APIView的dispatch方法,initial方法调用了request.user
- 如果我们配置了认证类,走我们自己认证类中的authentication方法
