# python2实现的web框架

## 简介

httppy是作者在经历过一段时间Django开发后，  
有感于Django的强大与实用以及一些令人诟病之处后出于学习目的开发的一套web框架。  
Django框架在实际的web开发中是非常快捷、实用的。  
对于大中小型的项目Django都能吃得开。功能完善，开发快捷。  
但是Django框架内部的耦合性非常强，这导致了在使用中对于具体项目的深度定制非常困难。  
比如Django的模板系统以及ORM在不少地方引人诟病，可如果想要享受Django带来的便利就必须忍受这些瑕疵。  
在此情况下作者参考了Django的许多设计概念，并在一些引人诟病处实现了自己的想法，从而开发了httppy框架。  


**httppy更多的只是一个用于学习的作品，而不是一个可以用作生产环境的工具。通过简单的代码去实现对HTTP协议的解析、封装，在这个过程中了解一个服务器的工作流程究竟是怎样的。**


框架命名为httppy原因有二

1. 最初是想简单的命名为web.py但是由于web.py这个标志性的名字已经被Aaron Swartz大神占用了只能放弃  
2. httppy这套框架不仅是应用层的框架，而是从socket层开始一步步向上在自己实现的http服务器基础上开发而来  

httppy框架的特色

1. 吸收了大量django的设计模式，在开发中可以参考django的开发范式快速开发。
2. 整套框架代码量非常少，结构清晰，实现的功能较齐全。易于阅读、学习、定制。
3. 使用多进程、线程池技术，性能强劲，足以支撑绝大多数小型个人站点的点击量。

httppy的不足

目前为止httppy完全由作者一人编写、维护。httppy没有经过什么项目的实战。因此httppy框架显得过于单薄。  
相对于成熟的框架存在非常多没有考虑到的场景，有待于日后的优化、升级。  
欢迎各位有兴趣的朋友来共同学习、维护httppy框架。


## 快速开始

让我们从一个hello world工程来快速领略httppy的使用吧

创建hello.py文件

    import httppy
    from httppy import web
    
    
    class Index(web.RequestHandler):
        def handle(self):
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

在demo目录中有一个示例工程展示了框架的使用方式


## 框架工作模式


    |-----------------------------------------------------------------------------------------------
    |                                        +-----------+
    |                                        |  Server() |
    |                                        +-----------+
    |                                              |
    |                                              v
    |                                        +-----------+
    |                                        |   bind()  |
    |                                        +-----------+
    |                                              |
    |                                              v
    |                                        +-----------+
    |                                        |  listen() |
    |                                        +-----------+
    |                                              |
    |                                              v
    |                                        +------------+    connect      +-----------+
    |            v---------------------------|  accept()  |<----------------|  Client() |
    |            |                           +------------+                 +-----------+
    |            |从线程池中找到一个          　继续等待下一个请求
    |            |空闲Handler处理connect            |           
    |            |connect                          |                               
    |            |客户端套接字连入                   |
    |            v----------------------------------                                         
    |   +-----------------+                                                             
    |   | SocketHandler() |                                                         
    |   +-----------------+                                                         
    |            |recv -> data 
    |            v在TCP套接字层面接受数据
    |   +-----------------+
    |   |   HttpHandler() |
    |   +-----------------+
    |            |parse_http -> Request 
    |            v在http协议层解析生成Request对象
    |+------------------------+
    ||  Web.RequestHandler()  |----v将request对象交给UrlRoute对象处理
    |+------------------------+    |
    |            |                 |    +--------------+
    |            |                 >--->|  UrlRoute()  |-v根据request url调用用户指定的RequestHandler
    |            |                      +--------------+ |
    |            |                                       |  +--------------------+
    |            |                                       >--|  RequestHandler()  |
    |            |                                          +--------------------+
    |            |                                                     |handler -> Response 
    |            |                                                     |用户对请求进行处理
    |            v-----------------------------------------------------<并生成Response对象作为响应
    |            |
    |            |
    |            |
    |            v
    |   +----------------+
    |   |  HttpHandler() |
    |   +----------------+
    |            |get_response -> result 
    |            v将Response对象转化为套接字数据
    |   +-----------------+
    |   | SocketHandler() |
    |   +-----------------+
    |            |sendall 
    |            |将数据发送给客户端
    |            v
    |-----------------------------------------------------------------------------------------------


1. Server层  
> 服务器绑定监听一个端口等待客户端连入  
> 当客户端连入后将连接转交给线程池中的空闲Handler处理  
2. SocketHandler层  
> 在套接字层recv客户端发来的数据  
> `self.recv() -> self.data`  
3. HttpHandler层  
> 根据http协议解析套接字接收到的数据  
> head body method url get post file ...  
> `self.parse_http() -> self.request`  
4. Web.RequestHandler层  
> 将self.request对象交给UrlRoute处理  
> `self.url_route.route(self.http_request)`  
5. UrlRoute  
> 根据传入的request url在用户预先写好的url匹配表中匹配  
> 实例化相应的RequestHandler对象 将request传给他  
6. RequestHandler  
> 用户继承对象并重载handle方法进行处理  
> 产生相应的Response对象  
7. HttpHandler层  
> 将Response解析为完整可发送的对象  
> `self.get_http_response(http_response)`  
8. SocketHandler层  
> sendall发送数据到客户端  
> 关闭连接  



## URL配置

url配置方法完全基于python自带的re正则模块  

    url = [
        (r'^/url1/$', handler1),
        (r'^/url2/$', handler2),
        ...
    ]

每条匹配规则写在一个元组中  
所有的url匹配规则写在一个list中  

支持re模块的分组功能
    
    (r'^/(?P<param1>[^/]+)/$', handler3)

该正则可以将 /xxx/ 形式的url中的xxx解析提取出  
并可以在RequestHandler中通过`self.request.url_param['param1']`访问  

httppy中不论传入的url是否使用 / 结尾 都会强制规范以 / 结尾  
如:  
> /  
/url1/  
/url2/url3/  

绝对不会出现  
> /url4  

这种不以 / 结尾的url  
因此在编写url时要特别注意`正则`的表达


## 静态文件

httppy自己实现了静态文件的处理  
可以通过配置url达到对静态文件的响应  

    from httppy.statichandler import static_handler
    url = [
        ...,
        (r'/static/(?P<path>.*)$', static_handler(os.path.join(os.getcwd(), 'static'))),
        ...,
    ]

以该模式配置url即可通过 /static/xxx 访问static目录下的文件

    os.path.join(os.getcwd(), 'static'))

此处是为了获取指定目录的绝对路径  
在实际使用中请获取绝对路径填入  
避免无谓的混淆  
如果有多个目录方式静态文件  
也可以编写多条对应到不同路径的静态文件url  

httppy实现的静态文件处理功能比较粗糙，仅适合`调试或者流量较小站点使用`  
更好的方案是使用`nginx`处理静态文件  
httppy仅处理动态的请求 


## 响应的生成

用户重载web.RequestHandler来对一个request进行处理、响应  
重载handle方法实际进行操作  
该对象具备两个重要的属性  

    self.request
    self.response

self.request可以提取解析后的请求 请查看源代码了解该对象所具备的属性  
self.response是返回给客户端的响应  
Response对象具备以下常用方法  

    set_header
    set_cookie
    set_status
    set_body
    redirect
    
有一些简单的http协议的了解对这些方法应该很容易理解
如set_body设置了html页面内容  
使用范例  

    self.response.set_body('Hello httppy!')
    self.response.set_header('Content-Type', 'text/html')
    self.response.set_cookie('key', 'value')
    self.response.set_status(404)
    self.response.redirect('/index/')

特别注意set_header的使用  
请一定注意使用驼峰风格来编写 Content-Type 而不是 content-type    
目前在httppy中是大小写敏感的的  
通常无需设置Content-Type默认为text/html  


## 模板系统

模板系统采用jinja2  
如果需要使用模板系统请自行安装jinja2  
httppy.template.py中对jinja2进行了一些简单的包装  

首先需要设置jinja2的工作目录

    from httppy import template
    template.render = template.get_template_render('template')

该语句设置工程下的template目录为默认工作路径  
建议你在任何时刻填写绝对路径以避免混淆  
当然，只要你足够了解python的规则，填写相对路径会更加简洁  

现在来使用模板系统

    from httppy.template import render
    class Template(web.RequestHandler):
        def handle(self):
            # template中的render对象用于进行模板渲染
            # 模板系统使用jinja2
            # template中仅仅是对jinja2的包装
            import datetime
            self.response.set_body(render.render('template.html', {'hello': 'world'}))

更多的内容请移步[jinja2文档](http://www.pythonfan.org/docs/python/jinja2/zh/templates.html)


## ORM

httppy框架没有对ORM进行整合  
如有必要请自行整合ORM  


## 服务器配置


    import httppy
    from httppy import web
    
    
    class Index(web.RequestHandler):
        def handle(self):
            self.response.set_body('Hello httppy!')

    url = [
        (r'^/index/$', Index)
    ]

    server_address = [
        ('', 7777),
    ]
    
    conf = {
        # 设定套接字超时时间
        'connect_timeout': 5,
        # 设定套接字监听队列长度
        'request_queue_size': 5,
        # 设定每条进程的线程池大小
        'thread_pool_size': 10,
    }
    
    manager = httppy.Manager(server_address, url, **conf)
    manager.server_start()

将服务器要绑定的(主机名、端口)以及配置好的url列表交给Manager类  
Manager负责完成框架的启动  
httppy框架的每个服务器在一个进程中运行，并维护一个进程池  
由于python GIL的限制，只能使用一个cpu核心  
因此在生产环境中应开启与cpu核心数一样多的进程  
这些工作Manager类都一并负责完成

    server_address = [
        ('', 7777),
        ('', 7778),
    ]

只需要在这里添加新的端口信息就可以开启相应的进程  

在生产环境中应开启多条进程占用多个端口  
并使用Nginx的负载均衡来进行反向代理  


## 推荐开发范式


目录结构
Project
> manage.py 主文件 程序入口  
> urls.py url配置文件  
> settings.py 框架配置文件  
> httppy/ httppy库  
> demoapp/ 一个典型的应用  
>> \__init__.py  
>> handler.py  
>> urls.py  

> static/ 静态文件目录  
> template/ 模板文件路径  

推荐在linux服务器上运行  
使用Nginx作为前端反向代理反向代理服务器  
Nginx完成负载均衡、处理静态文件请求  


----------------------
