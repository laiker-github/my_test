#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys 
import update
import importlib

  
def main():

    is_end = False

    while not is_end:
        s_operate = input("输入操作: ")
        if s_operate == "close":
            sys.exit()
            break
        Loog()


def Loog():
    update.start()

if __name__ == "__main__":
    import hot_update
    hot_update.start()
    print("程序开始运行...")
    main()

