import re
def walk_obj(obj, regex):
    if type(regex) == str:
        regex = re.compile(regex)
    result = []
    if type(obj) == list:
        for v in obj:
            tmp = walk_obj(v, regex)
            result += tmp
    if type(obj) == dict:
        for k in obj:
            tmp = walk_obj(obj[k], regex)
            result += tmp
    if type(obj) == str and regex.match(obj):
        result.append(obj)
    return list(set(result))

def walk_obj_by_value(obj, regex):
    return walk_obj(obj, regex)

def walk_obj_by_key(obj, regex):
    if type(regex) == str:
        regex = re.compile(regex)
    result = []
    if type(obj) == list:
        for v in obj:
            tmp = walk_obj_by_key(v, regex)
            result += tmp
    if type(obj) == dict:
        for k in obj:
            if regex.match(k):
                result.append(obj[k])
            tmp = walk_obj_by_key(obj[k], regex)
            result += tmp
    return result