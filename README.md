# python实现的http服务器

基于TCP套接字实现
使用线程技术 每一个连接由一个线程来处理 处理后关闭连接释放资源

等待完善
> Socket server
>> 开启管理
>> 关闭管理
>> 多进程管理
>> 线程数量管理
>> 超时处理
>> 错误处理
>> 线程池

> HTTP server
>> HTTP内容解析
>>> 对HTTP报文主体进行解析
>>> POST 解析
>>> COOKIE 解析
