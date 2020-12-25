## 故事背景

这段时间在做一个nginx + uwsgi + python的项目,有个需求是需要在服务运行过程中可以改变配置并生效,可以理解为热重载. 之前这些配置都是写死在项目的配置文件中的基础配置,一般就是python项目中的config.py文件. 现在配置变更使用了开源的apollo作为管理端,需要python使用client对接apollo.

先看一份常见的python后台使用uwsgi的配置:
```
test@python:~/app$ cat uwsgi.ini
[uwsgi]
module = app
wsgi-file = app.py
master = true
processes = 4           # 多个work进程
enable-threads = true   # 允许启动多线程
#lazy-apps = true       # 后面再说
http = :3000
die-on-term = true
pidfile = ./uwsgi.pid
chdir = /home/test/app
disable-logging = true
log-maxsize = 5000000
daemonize = /home/test/app/log.log
```
这里给出python代码的demo app.py:

```
from flask import Flask, jsonify, request
from apollo import Config

cf = Config("test", "application")
print("----------key-----------")
print(cf.SQLALCHEMY_TRACK_MODIFICATIONS)    # 尝试获取一些配置
print(cf.LOG_NAME)
print("----------key-----------")

app = Flask(__name__)


@app.route('/')
def hello_world():
    key = request.values.get('key')
    new = getattr(cf, key)
    # 尝试实时获取配置
    return jsonify({'data': new, 'apo': cf.apo.get_value(key), "my": cf.SQLALCHEMY_POOL_SIZE})


application = app  # for uwsgi.ini
if __name__ == "__main__":
    app.run(port=5000)
```


再看看这个配置启动后的效果:

```
test@python:~/app$ ps -ef|grep uwsgi.ini
test      16224     1  0 14:36 ?        00:00:00 uwsgi --ini uwsgi.ini
test      16225 16224  0 14:36 ?        00:00:00 uwsgi --ini uwsgi.ini
test      16226 16224  0 14:36 ?        00:00:00 uwsgi --ini uwsgi.ini
test      16227 16224  0 14:36 ?        00:00:00 uwsgi --ini uwsgi.ini
test      16228 16224  0 14:36 ?        00:00:00 uwsgi --ini uwsgi.ini
test      16229 16224  0 14:36 ?        00:00:00 uwsgi --ini uwsgi.ini
test      16378 15998  0 14:39 pts/48   00:00:00 grep --color=auto uwsgi.ini
```

## 然后问题来了

每次在apollo后台变更配置时明明配置的localfile本地文件已经变更但是进程中的cache就是没变...查看了apollo开源说明中推荐的三种python client,发现实现方式都是大同小异,主要就是启动守护线程长链接pull服务端的接口,服务端有变更时接口就能访问通,进而触发这个守护线程的动作去更新cache和localfile,上面说了localfile已经有了更新的动作为啥cache没被更新呢? 带着疑问去看了这三个开源库的issues,然后发现[uwsgi+django项目中配置的apollo， 不能获取最新apollo数据](https://github.com/filamoon/pyapollo/issues/19) 嗯,看来是通病了...

## 验证猜想

翻了下其他语言上没啥类似问题,那会不会是python的特色,先来个手动多进程试试:
```
1. 执行python app.py
2. 修改app.py中的端口号
3. 执行python app.py
4. 重复2,3
5. 注意看打印的日志
6. 试着访问下设置的端口 curl "127.0.0.1:3000"
7. 修改apollo的配置
8. 看看日志,再执行curl "127.0.0.1:3000",看看获取的配置是不是最新的.
```
然后发现没啥问题啊,每个实例都能访问到最新的,日志中都打印了更新cache和localfile的日志.那么就排除了python的问题,聚焦到uwsgi的配置上看看吧,网上搜的话比较凌乱,一般搜官方文档好了,如这里[Python/WSGI应用快速入门](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/WSGIquickstart.html),然后就会看到左边有个**关于Python线程的注意事项**嗯,难道是我没加**enable-threads = true**导致的? 立马加上试试,效果还是不行,那继续看文档吧,翻看目录直到看到这句 **优雅重载的艺术**,下面摘抄文档中的一些关键语句:

### [Preforking VS lazy-apps VS lazy](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/articles/TheArtOfGracefulReloading.html#preforking-vs-lazy-apps-vs-lazy)
```
这是uWSGI项目具有争议的选择之一。

默认情况下，uWSGI在第一个进程中加载整个应用，然后在加载完应用之后，会多次 fork() 自己。这是常见的Unix模式，它可能会大大减少应用的内存使用，允许很多好玩的技巧，而在一些语言上，可能会让带给你很多烦恼。

尽管它的名声如此，但是uWSGI是作为一个Perl应用服务器 (它不叫做 uWSGI，并且它也并不开源) 诞生的，而在Perl的世界里，preforking一般是一种受到祝福的方式。

然而，对于许多其他的语言、平台和框架来说，这并不是真的，因此，在开始处理uWSGI之前，你应该选择在你的栈中如何管理 fork() 。

而从“优雅重载”的角度来看，preforking极大的提高了速度：只加载你的应用一次，而生成额外的worker将会非常快。避免栈中的每个worker都访问磁盘会降低启动时间，特别是对于那些花费大量时间访问磁盘以查找模块的框架或者语言。

不幸的是，每当你的修改代码时，preforking方法迫使你重载整个栈，而不是只重载worker。

除此之外，你的应用可能需要preforking，或者由于其开发的方式，可能完全因其崩溃。

取而代之的是，lazy-apps模式会每个worker加载你的应用一次。它将需要大约O(n)次加载 (其中，n是worker数)，非常有可能会消耗更多内存，但会运行在一个更加一致干净的环境中。

记住：lazy-apps与lazy不同，前者只是指示 uWSGI对于每个worker加载应用一次，而后者更具侵略性些 (一般不提倡)，因为它改变了大量的内部默认行为。

```

看来是默认配置导致了多进程多线程情况下,uwsgi加载完后第一个完整的work后,剩下**processes**中配置的work都是通过fork来的,看看uwsgi的启动日志也会发现的确只加载了一个app,每次操作也只有一个守护线程在监听和打印日志,那为啥fork来就不是完整的服务了呢,这就要说到unix fork的原理和实现了.

### 在unix/linux操作系统中，提供了一个fork()系统函数，它有这些特性:

```
0. fork()函数用于从一个已经存在的进程内创建一个新的进程，新的进程称为“子进程”，相应地称创建子进程的进程为“父进程”。使用fork()函数得到的子进程是父进程的复制品，子进程完全复制了父进程的资源，包括进程上下文、代码区、数据区、堆区、栈区、内存信息、打开文件的文件描述符、信号处理函数、进程优先级、进程组号、当前工作目录、根目录、资源限制和控制终端等信息，而子进程与父进程的区别有进程号、资源使用情况和计时器等。

1. 普通的函数调用，调用一次，返回一次，但是fork()调用一次，返回两次。因为操作系统自动把当前进程(父进程)复制了一份(子进程)，然后分别在父进程和子进程内返回。

2. 子进程永远返回0，父进程返回子进程的ID。

3. 一个父进程可以fork()出很多个子进程。因此，父进程要记下每个子进程的ID,而子进程只需要调用getppid()就可以拿到父进程的id。getpid()可以拿到当前进程id

4. 父进程、子进程执行顺序没有规律，完全取决于操作系统的调度算法。

5. 如果父进程有多个线程会不会复制父进程的多个线程呢？其实子进程创建出来时只有一个线程，就是调用fork()函数的那个线程。
```

也就是说 **uwsgi fork进程(不区分进程和线程)的时候只会把当前正在执行的app线程复制一份,而不会把随app线程初始化过程中产生的守护线程apollo-client也fork一份**,那么解决起来就简单了,配置下**lazy-apps = true**就可以了,每次fork都是一个真正完整的app进程包含了app线程和apollo-client线程.如果我还没说清楚的话,可以参考这里
[谨慎使用多线程中的fork](https://www.cnblogs.com/liyuan989/p/4279210.html)[fork多线程进程时的坑（转）](https://www.cnblogs.com/ajianbeyourself/p/8167746.html)

那么自然就想到既然cache是每个进程独立的,那就干脆去掉cache使用localfile,也很简单粗暴是可以完成多进程共享配置的功能,每次访问配置都做下文件IO操作,这里不是什么访问量大的服务的话可以这么操作,下面再说说其他方案.

### 使用缓存

重构apollo client中线程中的cache缓存的存储方式,比如切换为redis,同样是IO操作比每次都http直接查询apollo配置接口要好些,要是是远程redis-server那网络延时也不可忽略,进而考虑本地redis或者使用[uWSGI缓存框架](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/Caching.html)

```
使用缓存API，在应用中访问缓存
你可以通过使用缓存API，访问你的实例或者远程实例中的各种缓存。目前，公开了以下函数 (每个语言对其的命名可能与标准有点不同):

cache_get(key[,cache])
cache_set(key,value[,expires,cache])
cache_update(key,value[,expires,cache])
cache_exists(key[,cache])
cache_del(key[,cache])
cache_clear([cache])
如果调用该缓存API的语言/平台区分了字符串和字节 (例如Python 3和Java)，那么你必须假设键是字符串，而值是字节 (或者在java之下，是字节数组)。否则，键和值都是无特定编码的字符串，因为在内部，缓存值和缓存键都是简单的二进制blob。

expires 参数 (默认为0，表示禁用) 是对象失效的秒数 (并当未设置 purge_lru 的时候，由缓存清道夫移除，见下)

cache 参数是所谓的“魔法标识符”，它的语法是
```


好了,到这里这个问题到此解决了一半. 为什么说一半呢,因为这些配置都是普通配置并不是类似mysql,redis的配置信息,这些配置不会再修改配置后重新生成实例,也就没法使用最新的mysql或redis配置,那么怎么办呢? 下面说说重载服务.


## 重载服务

如何优化的重启服务?

### 命令重启uwsgi服务

再守护线程的监听函数最后建加上回调,回调命令函数的实现如下,pid_path是uwsgi启动后生成的pid文件地址.简单粗暴但有效.

```
# 重载uwsgi
def relaod_uwsgi(pid_path):
    """选用方案1"""
    print("------------relaod_uwsgi---------------")
    val = os.system('uwsgi --reload {}'.format(pid_path))
    print(val)
    if val:
        print("重启可能遇到了问题...")
```


### 另辟蹊径

```
py-auto-reload
argument: 必需参数

parser: uwsgi_opt_set_int

flags: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER

help: 监控python模块mtime来触发重载 (只在开发时使用)

py-autoreload
argument: 必需参数

parser: uwsgi_opt_set_int

flags: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER

help: 监控python模块mtime来触发重载 (只在开发时使用)

python-auto-reload
argument: 必需参数

parser: uwsgi_opt_set_int

flags: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER

help: 监控python模块mtime来触发重载 (只在开发时使用)

python-autoreload
argument: 必需参数

parser: uwsgi_opt_set_int

flags: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER

help: 监控python模块mtime来触发重载 (只在开发时使用)

py-auto-reload-ignore
argument: 必需参数

parser: uwsgi_opt_add_string_list

flags: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER

help: 自动重载扫描期间，忽略指定的模块 (可以多次指定)
```
这些配置是监控特定文件来重载uwsgi服务的,那么我们只要改下localfile的名字为py结尾,那差不多也是没问题的.


## 留下点东西
最后想说点私货,人类不可能想象出超越意识范围内的东西,比如做梦,梦中的东西肯定都是平时生活中鸡零狗碎的拼凑和伪装,代码也是.创新也是.

这里整理了一个采坑后贡献出来的python client demo,主要代码是[apollo-client-python](https://github.com/xhrg-product/apollo-client-python)中的,我在改了里面的http请求使用requests,然后做了点浅浅的封装.欢迎大家star!
这篇随记也归档到了这里[python-mini](https://github.com/aleimu/python-mini),也欢迎欢迎大家star!

## [最后：不要盲目地复制粘贴!](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/articles/TheArtOfGracefulReloading.html#id10)

```
请用脑子想想，试着将显示的配置调整以适应你的需求，或者创建新的配置。

每个应用和系统都是彼此之间不同的。

作出选择之前请进行实验。
```
上面那句不是我说的,是uwsgi文档说的.

