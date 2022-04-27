

class A:

    def __init__(self):
        print('I am A')
        var_a = 'test'


class B:

    def __init__(self):
        print('I am B')


class C(A, B):

    def __init__(self):
        A.__init__(self)
        B.__init__(self)

class D(A, B):
    def __init__(self, A=A):
        print(A.var_a)