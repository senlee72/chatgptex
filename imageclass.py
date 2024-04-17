# def my_decorator(func):
#     def wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper

# @my_decorator
# def say_hello(a, b, c, x=1, y=2, z=3):
#     return a+b+c+x+y+z

# a= say_hello(10, 20, 30, x=5, y=10, z=15)
# print(a)


def class_decorator(cls):
    class NewClass(cls):
        def new_method(self):
            print('This is a new method')
    
    return NewClass

@class_decorator
class MyClass:
    def orig_method(self):
        print("This is the orig method")


obj = MyClass()

obj.orig_method()
obj.new_method()