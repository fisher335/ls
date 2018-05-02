# -*- coding: utf-8 -*-  
# @Date    : 2017-08-29 09:33:23 , @Author  : fengshaomin@bjsasc.com 
def sort_fun(name):
    return name[3]

def main():
    names = ['David Beazley', 'Brian Jones','Raymond Hettinger', 'Ned Batchelder']
    c = sorted(names, key=lambda x: x[0])
    d = sorted(names, key=sort_fun)
    print(c)
    print(d)


if __name__ == '__main__':
    main()