# encoding: utf-8
import threading

local = threading.local()
local.cache = {}

def put(key,value):
    local.cache[key] = value

def get(key):
    if key in local.cache.keys():
        return local.cache[key]
    return None

def remove():
    local.cache = {}
