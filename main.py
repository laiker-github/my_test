#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys 
import update
import importlib

root_path = "Users"
  
def main():

    is_end = False

    while not is_end:
        s_operate = input("输入操作: ")
        if s_operate == "close":
            break
        Do_operate(s_operate)
        Loog()

def Do_operate(operate):
    if "update" in operate:
        do_update()


def do_update():
    # 代码热更新开始 
    lst = []
    for i in sys.modules.values():
        if not hasattr(i, "__file__"):
            continue
        if root_path not in i.__file__:
            continue
        name = getattr(i, "__name__", "")
        if "__" in name:
            continue
        if "update" in i.__file__:
            continue
        lst.append(i)
    for j in lst:
        do_update2(j)


def do_update2(mod):
    from types import FunctionType
    if not getattr(mod, "__name__"):
        return
    name = mod.__name__
    print("更新: " + name + mod.__file__)
    oldMoudle = __import__(name)
    oldMoudleData = {}
    attrList = dir(oldMoudle)
    for attrName in attrList:
	    oldMoudleData[attrName] = getattr(oldMoudle, attrName)

    importlib.reload(oldMoudle)
    newMoudle = __import__(name)

    # 全局变量等
    for attrName in dir(newMoudle):
        if attrName in oldMoudleData:
            print(attrName+"1")
            if isinstance(oldMoudleData[attrName], FunctionType) \
                or isinstance(oldMoudleData[attrName], int) \
                or isinstance(oldMoudleData[attrName], float) \
                or isinstance(oldMoudleData[attrName], str):
                pass    
            elif isinstance(oldMoudleData[attrName], type):
                print(attrName+"2")
                ReplaceClassFunc(getattr(newMoudle, attrName), oldMoudleData[attrName])
                setattr(newMoudle, attrName, oldMoudleData[attrName])
            else:
                print(attrName+"3")
                setattr(newMoudle, attrName, oldMoudleData[attrName])
        print("===========")
    
def ReplaceClassFunc(srcClass, desClass):
    for attrName in dir(srcClass):
        print("fun:" + attrName)
        attr = getattr(srcClass, attrName)
        from types import FunctionType
        if isinstance(attr, FunctionType) \
            or isinstance(attr, int) \
            or isinstance(attr, float) \
                or isinstance(attr, str):
            setattr(desClass, attrName, attr)


def Loog():
    update.start()

if __name__ == "__main__":
    
    print("程序开始运行...")
    main()
     

