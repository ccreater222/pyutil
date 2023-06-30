from multiprocessing import Pool

def worker(func, args_list, kwargs_list, thread_num: int = 8) -> list:
    p = Pool(thread_num)
    res_list = []
    for i in range(len(args_list)):
        args = args_list[i]
        kwargs = kwargs_list[i]
        res = p.apply_async(func, args=args, kwds=kwargs)
        res_list.append(res)
    p.close()
    for res in res_list:
        yield res.get()
