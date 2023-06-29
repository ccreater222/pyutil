
import requests
import urllib3
from bs4 import BeautifulSoup
from multiprocessing import Pool
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def request(method: str="GET", url: str="", proxy: str="", *args, **kwargs)->requests.Response:
    method = method.lower()
    try:
        req_func = getattr(requests, method)
    except:
        return None
    kwargs["verify"] = False
    kwargs["allow_redirects"] = True
    kwargs["timeout"] = 3
    if proxy != "":
        kwargs["proxies"] = {
            "http": proxy,
            "https": proxy
        }
    try:
        r = req_func(url, *args, **kwargs)
        return r
    except Exception as e:
        return None


def response_get_title(r: requests.Response):
    bs = BeautifulSoup(r.text, 'html.parser')
    if bs.title:
        return bs.title.string
    return ""

def url_visitor(urlist: list[str], method='GET', thread_num: int = 8, req_params: dict = {}) -> list[requests.Response]:
    p = Pool(thread_num)
    res_list = []
    for url in urlist:
        res = p.apply_async(request, args=(method, url), kwds=req_params)  # 向进程池中添加任务
        res_list.append(res)
    p.close()
    for res in res_list:
        yield res.get()



