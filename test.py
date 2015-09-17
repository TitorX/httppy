class A:
    def __init__(self):
        self.name = '123'

    def get(self):
        return self.name


raw_input()
for i in xrange(10000):
    for j in xrange(10000):
        print(A().get())
raw_input()

