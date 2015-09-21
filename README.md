# python实现的web框架

## 简介

httppy是作者在经历过一段时间Django开发后，
有感于Django的强大与实用以及一些令人诟病之处后出于学习目的开发的一套web框架。
Django框架在实际的web开发中是非常快捷、实用的。
对于大中小型的项目Django都能吃得开。功能完善，开发快捷。
但是Django框架内部的耦合性非常强，这导致了在使用中对于具体项目的深度定制非常困难。
比如Django的模板系统以及ORM在不少地方引人诟病，可如果想要享受Django带来的便利就必须忍受这些瑕疵。
在此情况下作者参考了Django的许多设计概念，并在一些引人诟病处实现了自己的想法，从而开发了httppy框架。

框架命名为httppy原因由二

1. 最初是想简单的命名为web.py但是由于web.py这个标志性的名字已经被Aaron Swartz大神占用了只能放弃
2. httppy这套框架不仅是应用层的框架，而是从socket层开始一步步向上在自己实现的http服务器基础上开发而来

httppy框架的特色

1. 吸收了大量django的设计模式，在开发中可以参考django的开发范式快速开发。
2. 整套框架代码量非常少，结构清晰，实现的功能较齐全。易于阅读、学习、定制。
3. 使用多进程、线程池技术，性能强劲，足以支撑绝大多数站点的点击量。

httppy的不足

目前为止httppy完全由作者一人编写、维护。httppy没有经过什么项目的实战。因此httppy框架显得过于单薄。
相对于成熟的框架存在非常多没有考虑到的场景，有待于日后的优化、升级。
欢迎各位有兴趣的朋友来共同壮大、维护httppy框架。
希望有朝一日httppy可以更加健壮、易用、稳定。能成为开发者快速进行web开发的利器。


## 快速开始

让我们从一个hello world工程来快速领略httppy的使用

创建hello.py文件

    import httppy
    from httppy import web
    
    
    class Index(web.RequestHandler):
        def handler(self):
            self.response.set_body('Hello httppy!')

    url = [
        (r'^/index/$', Index)
    ]

    server_address = [
        ('', 7777),
    ]
    
    manager = httppy.Manager(server_address, url)
    manager.server_start()

 
执行使用python2执行hello.py

    $python hello.py
    2015-09-21 20:19:04 socketserver.py[line:58] INFO Server start
    2015-09-21 20:19:04 socketserver.py[line:61] INFO bind:('0.0.0.0', 7777)

接下来在浏览器中打开 http://127.0.0.1:7777/index/ 就可以看到 Hello httppy! 的字样了


## 框架工作模式
一次请求的处理流程

    |            |connect 客户端套接字连入
    |            v
    |   +-----------------+
    |   | SocketHandler() |
    |   +-----------------+
    |            |recv -> data 在TCP套接字层面接受数据
    |            v
    |   +-----------------+
    |   |   HttpHandler() |
    |   +-----------------+
    |            |parse_http -> Request 在http协议层对解析http携带的内容 url get post file ... 存储在Request对象中
    |            v
    |+------------------------+
    ||  Web.RequestHandler()  |
    |+------------------------+
    |            |handler -> Response 用户对请求进行处理并生成成Response对象作为响应
    |            v
    |   +----------------+
    |   |  HttpHandler() |
    |   +----------------+
    |            |get_response -> result 将Response对象转化为套接字数据
    |            v
    |   +-----------------+
    |   | SocketHandler() |
    |   +-----------------+
    |            |sendall 将数据发送给客户端
    |            v



## URL配置
## 服务器配置
## 模板系统
## 静态文件
## ORM
## 推荐开发范式


目录结构
Project
>manage.py 主文件 程序入口

>urls.py url配置文件

>settings.py 框架配置文件

>httppy/ httppy库

>demoapp/ 一个典型的应用

>static/ 静态文件目录

>template/ 模板文件路径

----------------------


待完成
> 完善http响应的各种状态设置

> 编写完整的文档

> 完善README.md

> 优化多线程处理方案

> 进行各类设置的接口



