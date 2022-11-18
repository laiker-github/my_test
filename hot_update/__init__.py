#!/usr/bin/python
# -*- coding: UTF-8 -*-

""" 
代码热更 by xu.lai
"""

import importlib
import threading
import time
import os
import sys

from types import FunctionType

root_name = os.getcwd()
update_file_name = root_name + "\\hot_update\\update_file.txt"
update_file_log = root_name + "\\hot_update\\update_log.txt"

def start():
    CUpdate().start()

def get_now_time():
    timeStruct = time.localtime(time.time())
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

class CUpdate(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.update_file_io = open(update_file_name, "a+")
        self.update_file_log = open(update_file_log, "a+")
        self.pre_file_update_time = int(os.path.getmtime(update_file_name))

    def run(self):
        try:
            while True:
                time.sleep(1)
                if not self.check_is_update_file():
                    continue
                self.do_update()
        except:
            sys.exit()

    def check_is_update_file(self):
        now_update_time = int(os.path.getmtime(update_file_name))
        if self.pre_file_update_time >= now_update_time:
            return False
        self.pre_file_update_time = now_update_time
        return True

    def do_update(self):
        if not self.update_file_io:
            return
        self.update_file_io.seek(0, 0)
        line = self.update_file_io.readline()
        line_slip_list = line.split(",")
        for mod in line_slip_list:
            try:
                self.update_mod(mod)
            except Exception as err:
                print("更新失败: ", err)
                sys.exit()
        self.log("%s 更新文件: %s" %(get_now_time(), str(line_slip_list)))

    def log(self, msg):
        self.update_file_log.seek(0, 2)
        self.update_file_log.write(msg + "\n")
        self.update_file_log.flush()

    def update_mod(self, mod):
        if not mod:
            return
        name = mod
        oldMoudle = __import__(name)
        oldMoudleData = {}
        attrList = dir(oldMoudle)
        for attrName in attrList:
            oldMoudleData[attrName] = getattr(oldMoudle, attrName)
            
        importlib.reload(oldMoudle)
        newMoudle = __import__(name)

        for attrName in dir(newMoudle):
            if attrName not in oldMoudleData:
                continue
            if isinstance(oldMoudleData[attrName], FunctionType) \
                    or isinstance(oldMoudleData[attrName], int) \
                    or isinstance(oldMoudleData[attrName], float) \
                    or isinstance(oldMoudleData[attrName], str):
                pass    
            elif isinstance(oldMoudleData[attrName], type):
                self.ReplaceClassFunc(getattr(newMoudle, attrName), oldMoudleData[attrName])
                setattr(newMoudle, attrName, oldMoudleData[attrName])
            else:
                setattr(newMoudle, attrName, oldMoudleData[attrName])

    def ReplaceClassFunc(self, newClass, oldClass):
        for attrName in dir(newClass):
            attr = getattr(newClass, attrName)
            if isinstance(attr, FunctionType) \
                    or isinstance(attr, int) \
                    or isinstance(attr, float) \
                    or isinstance(attr, str):
                setattr(oldClass, attrName, attr)
