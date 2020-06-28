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

