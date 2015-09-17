import re

p = '''/(?P<name>[^/]+)/(?P<name1>[^/]+)/'''

s = '/index/hello/'

print(re.match(p, s).groupdict())