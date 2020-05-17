#coding:utf-8

import sys
sys.dont_write_bytecode = True
import time

def cost_time(func):
    """统计函数执行时间"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func()
        end_time = time.time()
        print("cost time: %.4fs"%(end_time - start_time))
    return wrapper
