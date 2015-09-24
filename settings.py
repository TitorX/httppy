# coding=utf-8

# 设置模板系统 #############################################
from httppy import template
template.render = template.get_template_render('template')
###########################################################


conf = {
    # 设定套接字超时时间
    'connect_timeout': 5,
    # 设定套接字监听队列长度
    'request_queue_size': 5,
    # 设定每条进程的线程池大小
    'thread_pool_size': 10,
}

# 要启动的服务器配置
# 每个服务器一个进程 每个进程一个线程池
# 推荐使用Nginx对多个服务器进行负载均衡
# 进程数与CPU核数相同最佳
server_address = [
    ('', 7777),
    ('', 7778)
]
