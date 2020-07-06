# Django

## Supervisor配置文件解析
- `unix_http_server`: UNIX socket配置，是supervisor用来管理进程的接口
- `inet_http_server`: supervisor Web服务器的配置，不需要Web服务器可以不开启
- `supervisord`: supervisord 的基础配置，包括日志和pid的文职
- `rpcinterface:supervisor`: 用来配置RPC接口，supervisorctl通过这个RPC来连接socket
- `supervisorctl`: supervisorctl命令配置，它配置的socket地址以及用户名密码应该和`unix_http_server`
一致
- `program:<程序名>`: 配置需要运行的程序启动命令，以及相关配置，如日志、环境变量、需要启动
的进程数等

## Django、Flask&Tornado框架对比
- Django：最全能的web开发框架，功能完备，可维护性高，开发速度快。但是使用笨重，性能一般
- Tornado：天生异步，性能高。但是框架提供的功能比较少。
- Flask：自由、灵活、扩展性高，有很多第三方插件。

## Django的生命周期
- 用户在浏览器中输入url后，浏览器会生成请求头和请求体，发送到Django后端
- url经过Django的wsgi，中间件，最后通过路由映射表，匹配对应的视图函数
- 视图函数根据请求返回相应的数据，Django把数据包装成HTTP的响应返回给前段
- 前段渲染数据

## Django的内置组件
- 认证组件、缓存、日志、邮件、分页、静态文件管理、消息框架、数据验证

## 列举Django中间件的方法，以及中间件的应用场景
- Django的中间件是一个类，在请求的到来和结束后，django会根据自己的规则在合适的时机执行中间件
中相应的方法
- 中间件在settings中的`MIDDLEWARE_CLASSES`变量配置
- 中间件的方法
    - `process_request(self, request)`方法在请求到来时候调用
    - `process_view(self, request, callback, callback_args, callback_kwargs)`在
    本次将要执行的View函数被调用前调用本方法
    - `process_template_respose(self, request, resposne)`使用render()之后执行
    - `process_exception(self, request, exception)`视图函数在抛出异常时调用，得到的
    Exception参数是被抛出的异常实例。
    - `process_response(self, request, response)`执行完视图函数后准备将数据返回给客户端前
    被执行
- 可以修改request和response对象的内容，在视图执行前做一些操作，判断浏览器来源，做一个拦截器
- 可以判断浏览器的来源是PC还是手机
- 可以做一个拦截器，一定时间内某个ip对网页第访问次数过多，可以加入黑名单拒绝服务

## 什么事FBV和CBV
- FBV是`function base views`基于函数视图，CBV是`class base views`基于类的视图
- FBV模式，URL匹配成功后，会直接执行对应的视图函数
- CBV模式，服务端通过路由映射表匹配成功后，自动去找dispatch方法，然后通过dispatch反射的方式
找到类中对应的方法执行。所有的类视图，都继承了View类，View类里有dispatch，负责分发。
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
- 请求一个页面的时候，Django创建了一个HttpRequest对象，包含了request数据。Django会加载对应
的视图，然后把request作为第一个参数传递到视图函数。
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
- extra(select=None, where=None, params=None, tales=None, order_by=None, select_params=None):
用户执行复杂的sql语句
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

## Django中三种sql语句的方法
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
- F: 操作表中的某一列值，允许Django不用获取对象放到内存中再对字段进行操作，而是直接执行原生
sql语句操作。
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
- bulk_create(): 需要注意，save()方法不会被调用，pre_save和post_save信号不会被发送。自增
字段也不会自增，无法创建多对多关系。
```python
Entry.objects.bulk_create([
    Entry(headline='This is a test'),
    Entry(headline='This is only a test'),
])
```
- bulk_update(): 无法更新主键，save()方法不会被调用，pre_save和post_save信号不会发送，
如果更新的内容有重复，只有第一个会执行。
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
- Form是自己定义的表单结构，需要继承Django的forms.Form类，然后像Model类一样，定义字段。保存数据
的时候，需要从POST里手动取出表单数据
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
- ModelForm是可以使用定义好的Model类，需要继承forms.ModelForm，然后在Meta类里，包含表单
要现实的字段，提示信息，错误信息等内容。保存数据时，不用手工去取数据，直接save即可
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