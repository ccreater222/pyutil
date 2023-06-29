import json
from obj import walk_obj
from network import request, response_get_title, url_visitor
if __name__ == "__main__":
    with open("url.json", "r") as f:
        data = json.loads(f.read())
    urls = []
    for domain in walk_obj(data, r".*\.woa.com\.?$"):
        domain = domain.strip(".*")
        urls += [f"http://{domain}", f"https://{domain}"]

    for r in url_visitor(urls, thread_num=32,
                         req_params={"proxy": "socks5://127.0.0.1"}):
        if r == None:
            continue
        msg = f"{r.url} [{r.status_code}] [{response_get_title(r)}]"
        with open("result.txt", "a") as f:
            f.write("\n" + msg)
        print(msg)