# -*- coding: utf-8 -*-  
# @Date    : 2017-08-29 10:58:10 , @Author  : fengshaomin@bjsasc.com 

class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


a = Person('feng')
a.first_name = ''
print(a.first_name)
