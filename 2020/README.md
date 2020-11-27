# python-asyncio-crud

从py3.6开始引入的类型注释开始和正式加入协程后,出现了很多优秀的异步web框架如sanic,fastapi,starlette等,此类能将类型注释和协程较自然的混合在一起的库是fastapi
在使用过程中,刚一上手就发现变量类型注释以及函数参数的类型注释真的很像go的味道, 变量:类型 = 值,然后再了解pydantic中各种校验类型的方式上尤其是model的使用,
那就更像了.

计算机科学领域的任何问题都可以通过增加一个间接的中间层来解决

python协程 = 事件循环 + 任务存储 + 回调

* Eventloop 是asyncio应用的核心, 是中央总控。Eventloop实例提供了注册、取消和执行任务和回调的方法。
* Future 是结果存储+回调管理器
* Coroutine 使用生成器技术来替代连续的多个回调
* Task 负责将Coroutine接口和Future、EventLoop接口对接起来, 同时它自己也是一个Future.

# 参考

https://www.cnblogs.com/lgjbky/p/12018406.html
https://www.uvicorn.org # 非常重要
https://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/WSGIquickstart.html

今天我们来说一个"套娃"的故事:

ASGI 服务器: 异步网关协议接口，一个介于网络协议服务和 Python 应用之间的标准接口，能够处理多种通用的协议类型，包括 HTTP，HTTP2 和 WebSocket。
ASGI 对于WSGI原有的模式的支持和WebSocket的扩展，即ASGI是WSGI的扩展。

uWSGI、uwsgi、wsgi:
wsgi：全称是Web Server Gateway Interface，WSGI不是服务器，python模块，框架，API或者任何软件，只是一种规范，描述web server如何与web application通信协议。
uwsgi：与WSGI一样是一种通信协议，是uWSGI服务器的独占协议
uWSGI：是一个web服务器，实现了WSGI协议、uwsgi协议、http协议等。

# fastapi   异步框架
fastapi.applications.FastAPI.__call__
fastapi.applications.FastAPI.add_api_route

# starlette  轻量级的 ASGI 框架/工具包 (类似werkzeug库是WSGI的工具库)
starlette.applications.Starlette.__call__
starlette.applications.Starlette.add_route
starlette.applications.Starlette.route
starlette.routing.Router
starlette.routing.Router.__call__

# uvicorn   基于 uvloop 和 httptools 构建的非常快速的 ASGI 服务器。
uvicorn.main.main
uvicorn.main.run
uvicorn.main.Server.run
uvicorn.config.Config.load:285:call = getattr(self.loaded_app, "__call__", None)

# asyncio   异步基础库,将异步分成了三个部分,避免回调嵌套
concurrent.futures.thread.ThreadPoolExecutor.submit
concurrent.futures.thread._worker

上面我们能看到很多回调__call__都是这个格式:
    async def __call__(self, scope: Scope, receive: Receive, send: Send)


Uvicorn使用ASGI规范与应用程序进行交互:

该应用程序应公开一个异步可调用方法，该方法带有三个参数：

    - scope -包含有关传入连接信息的字典。
    - receive -一个从服务器接收传入消息的通道。
    - send -将消息发送到服务器的通道。

可能使用的两种常见模式是基于函数的应用程序：

```函数
async def app(scope, receive, send):
    assert scope['type'] == 'http'
    ...
```

或基于实例的应用程序：

````类.__call__
class App:
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope["app"] = self
        await self.middleware_stack(scope, receive, send)

app = App()
```

wsgi规范与应用程序进行交互的格式:

    - environ 和 start_response 由 http server 提供并实现
    - environ 变量是包含了环境信息的字典
    - Application 内部在返回前调用 start_response
    - start_response也是一个 callable，接受两个必须的参数，status（HTTP状态）和 response_headers（响应消息的头）

两种常见模式:

``` 类.__call__
class App():
    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = Response('Hello world')
        return resp(environ, start_response)

    def __call__(self, environ, start_response):
        """The WSGI server calls the Flask application object as the
        WSGI application. This calls :meth:`wsgi_app` which can be
        wrapped to applying middleware."""
        return self.wsgi_app(environ, start_response)
```

```函数
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
```