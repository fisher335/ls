#coding:utf-8
import os,sys
import ConfigParser

def parserConf(path):
    # type: (object) -> object
    a = ConfigParser.ConfigParser()
    a.read(path)
    # print a.get('config','Name')
    a.optionxform = str
    d = {}
    # print a.sections()
    for i in a.sections():
        for j in  a.options(i):
            # print j ,a.get(i,j)
            d[j]= a.get(i,j)
    return d
    
if __name__ == '__main__':
    d = parserConf('PtNetDiskJunit_zywx.properties')
    print d
    sys.exit()