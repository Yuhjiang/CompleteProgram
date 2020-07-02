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

## 什么事FBV和CBV
- FBV是`function base views`基于函数视图，CBV是`class base views`基于类的视图