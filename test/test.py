f = open('mime.types')
s = f.read()

mime = {}

for i in s.splitlines():
    for j in i[:-1].split()[1:]:
        mime[j] = i[:-1].split()[0]

import json

print(json.dumps(mime, indent=4))
print(len(mime))