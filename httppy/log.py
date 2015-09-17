__author__ = 'titorx'

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%F %T',
)


socket_server_log = logging.getLogger('socket')

http_server_log = logging.getLogger('http')
