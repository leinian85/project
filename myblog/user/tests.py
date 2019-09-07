from django.test import TestCase


# Create your tests here.

def check(func):
    def wrapper(*args, **kwargs):
        print("check:",args[0])
        func(*args, **kwargs)

    return wrapper

@check
def sum(a, b):
    return a + b


sum(3,4) # check: 3


def a(func):
    print('i\'m a!')

    def e():
        print(1)
        func()
        print(2)

    return e


def b(func):
    print('i\'m b!')

    def d():
        print('a')
        func()
        print('b')

    return d


@a
@b
def c():
    print('!!!!!')

c()
